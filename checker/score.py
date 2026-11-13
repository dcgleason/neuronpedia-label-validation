#!/usr/bin/env python3
"""Scorer for the Neuronpedia label checker.

Lifted from scaleup/run_scaleup.py: same activation endpoint, same
max-activation extraction. Adds a disk cache keyed by
source + index + sha256(text) so a prompt is never scored twice, and a
rolling-window rate limiter for the documented 1000 requests / 60 min.

Credentials, in order: (1) NEURONPEDIA_API_KEY from the environment or
a .env file (see envkeys.py and .env.example), sent directly as the
x-api-key header — this is the route a fresh clone uses; (2) the
custom.neuronpedia connector's surrogate flow, when Muse's internal
credential plumbing happens to be installed (it is not required, and
its absence never breaks the import).

Usage as a module:
    from score import get_activation, Scorer
    v = get_activation("12-gemmascope-res-16k", 1657, "Tom fixed the sink.")
    # -> float max activation, or raises AuthError / RateLimitError
"""
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import envkeys  # noqa: E402

# Muse-internal credential plumbing (the custom.neuronpedia
# connector's surrogate flow). OPTIONAL fallback: it exists only inside
# Muse's own environment, so the import must never be a requirement.
try:
    sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
    from dynamic_credentials import (  # noqa: E402
        DynamicCredentialError,
        add_surrogate_to_request,
        read_json_response,
    )
except ImportError:  # a fresh clone lands here; that is fine
    class DynamicCredentialError(RuntimeError):
        """Placeholder for when the Muse credential plumbing is absent."""

    add_surrogate_to_request = None
    read_json_response = None

API_URL = "https://www.neuronpedia.org/api/activation/new"
HOST = "www.neuronpedia.org"
MODEL_ID = "gemma-2-2b"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

# Documented limit is 1000 requests / 60 min. Stay under it.
RATE_LIMIT_CALLS = 950
RATE_LIMIT_WINDOW_S = 3600
PAUSE_S = 0.3  # courtesy pause between uncached calls


class AuthError(RuntimeError):
    """401/403 from the API: stop everything, the credential is the problem."""


class RateLimitError(RuntimeError):
    """Still rate limited after one wait-and-retry."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused, verify the endpoint")


def extract_max(obj):
    """Max of the first all-numeric `values` list found (same as run_scaleup)."""
    if isinstance(obj, dict):
        vals = obj.get("values")
        if isinstance(vals, list) and vals and all(
            isinstance(v, (int, float)) for v in vals
        ):
            return max(vals)
        for v in obj.values():
            found = extract_max(v)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = extract_max(v)
            if found is not None:
                return found
    return None


def _cache_path(source, index, text):
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{source}__{index}__{digest}.json")


NO_KEY_MESSAGE = (
    "No Neuronpedia credential available. Get a free Neuronpedia API "
    "key at neuronpedia.org (create an account, then copy the key "
    "from the account / API section), then either export it:\n"
    "  export NEURONPEDIA_API_KEY=\"your-key\"\n"
    "or copy .env.example to .env in this folder and paste the key "
    "there. (Inside Muse's own environment, the custom.neuronpedia "
    "connector credential is used as a fallback.)"
)


def _read_response(response):
    if read_json_response is not None:
        return read_json_response(response)
    return json.loads(response.read().decode("utf-8"))


def _post_activation(source, index, text):
    """One raw API call. Returns the parsed response dict.

    Auth order: (1) NEURONPEDIA_API_KEY via envkeys (real environment
    or .env), sent directly as the x-api-key header; (2) the Muse
    connector surrogate flow, when that plumbing is installed; (3) on
    an interactive terminal, a one-time paste prompt via envkeys;
    otherwise a clear AuthError saying how to supply a key.
    """
    body = {
        "feature": {"modelId": MODEL_ID, "source": source, "index": str(index)},
        "customText": text,
    }
    headers = {"Content-Type": "application/json"}
    api_key = envkeys.get_key("NEURONPEDIA_API_KEY")
    use_surrogate = False
    if api_key:
        headers["x-api-key"] = api_key
    elif add_surrogate_to_request is not None:
        use_surrogate = True
    else:
        api_key = envkeys.require_key(
            "NEURONPEDIA_API_KEY",
            what_for="to score activations against the Neuronpedia API",
            where_to_get="neuronpedia.org (free account, API section)",
        )
        if api_key:
            headers["x-api-key"] = api_key
        else:
            raise AuthError(NO_KEY_MESSAGE)
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers=headers,
        method="POST",
    )
    if use_surrogate:
        add_surrogate_to_request(
            request, "custom.neuronpedia", allowed_hosts=[HOST]
        )
    with urllib.request.build_opener(NoRedirect()).open(
        request, timeout=60
    ) as response:
        return _read_response(response)


class Scorer:
    """Stateful scorer with cache, rate limiting, and 401/403 stop."""

    def __init__(self, cache_dir=CACHE_DIR, pause=PAUSE_S):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.pause = pause
        self._call_times = deque()
        self.n_api_calls = 0
        self.n_cache_hits = 0

    def _wait_for_window(self):
        now = time.time()
        while self._call_times and now - self._call_times[0] > RATE_LIMIT_WINDOW_S:
            self._call_times.popleft()
        if len(self._call_times) >= RATE_LIMIT_CALLS:
            sleep_s = RATE_LIMIT_WINDOW_S - (now - self._call_times[0]) + 5
            print(
                f"score: {len(self._call_times)} calls in window; "
                f"sleeping {sleep_s:.0f}s to respect the rate limit.",
                flush=True,
            )
            time.sleep(max(sleep_s, 1))
            self._wait_for_window()

    def get_activation(self, source, index, text):
        """Max activation of (source, index) on text. Float; cached."""
        path = _cache_path(source, index, text)
        path = os.path.join(self.cache_dir, os.path.basename(path))
        if os.path.exists(path):
            with open(path) as f:
                self.n_cache_hits += 1
                return json.load(f)["max_activation"]
        self._wait_for_window()
        try:
            parsed = _post_activation(source, index, text)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise AuthError(
                    f"Neuronpedia API returned HTTP {e.code} for "
                    f"{source}/{index}. Stopping: check NEURONPEDIA_API_KEY "
                    "(see .env.example) or the connector credential "
                    "before retrying."
                ) from e
            if e.code == 429:
                print("score: HTTP 429, waiting 60s and retrying once.", flush=True)
                time.sleep(60)
                try:
                    parsed = _post_activation(source, index, text)
                except urllib.error.HTTPError as e2:
                    if e2.code in (401, 403):
                        raise AuthError(
                            f"Neuronpedia API returned HTTP {e2.code} on retry."
                        ) from e2
                    raise RateLimitError(
                        f"Neuronpedia API still returned HTTP {e2.code} after "
                        "a 60s wait. Stopping."
                    ) from e2
            else:
                raise
        except DynamicCredentialError as e:
            raise AuthError(f"credential plumbing failed: {e}") from e
        value = extract_max(parsed)
        if value is None:
            raise RuntimeError(
                f"no activation values in API response for {source}/{index}"
            )
        self._call_times.append(time.time())
        self.n_api_calls += 1
        with open(path, "w") as f:
            json.dump(
                {"source": source, "index": str(index), "text": text,
                 "max_activation": value},
                f,
            )
        if self.pause:
            time.sleep(self.pause)
        return value


_DEFAULT = Scorer()


def get_activation(source, index, text):
    """Module-level convenience wrapper around a shared default Scorer."""
    return _DEFAULT.get_activation(source, index, text)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Score one prompt and print the max activation.")
    ap.add_argument("--source", default="12-gemmascope-res-16k")
    ap.add_argument("--index", required=True)
    ap.add_argument("--text", required=True)
    args = ap.parse_args()
    print(get_activation(args.source, args.index, args.text))
