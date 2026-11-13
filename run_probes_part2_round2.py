#!/usr/bin/env python3
"""Part 2 round 2: four holdouts, longer texts."""
import json
import os
import sys
import time

BASE = os.path.expanduser("~/workspace/anthropic-residency/followup")
sys.path.insert(
    0, os.path.expanduser("~/workspace/custom-connectors/custom.neuronpedia/bin")
)
from np_activation import get_activation  # noqa: E402

PROBES = [
    ("s4", 6515, "supra shoes the seals, nowhere, supra shoes the speculation in our store. supra shoes on sale, supra shoes for men, supra shoes for women, supra shoes cheap, supra shoes online. welcome to our supra shoes shop, we provide supra shoes with high quality and low price. supra shoes the seals, nowhere, supra shoes the speculation in fashion. if you want to buy supra shoes, please come to our supra shoes outlet, supra shoes discount, supra shoes wholesale, supra shoes the seals nowhere supra shoes."),
    ("d5", 3349, "Building an Inclusive Workplace\n\nKeynote: The Business Case for Belonging\n\nOur panelists discussed engagement across every level of the organization.\n\nScale Your Investment: leaders advised participants to \"start small, measure what works, and grow the programs that move people.\"\n\nBroad Reach\n\nResearch done through mobile apps has been proven to reach employees in every region. Sessions continue through the afternoon with breakout discussions and networking."),
    ("b5", 3070, "How do I gain reputation on this site? I have answered several questions but my reputation is still low. As mentioned, in itself, chasing reputation, even if it is the only motivation, is a poor reason to answer. You earn reputation when other users upvote your posts. Users with high reputation can vote, comment, and moderate. The reputation system is designed to reward useful answers over time."),
    ("w4", 7196, "The case drew national attention for months. Even if it were not so severe, and even if the letter was not authentic, the reaction revealed something real about the town. It's not as bad as what happened to Tawana Brawley, one attorney argued, but the pattern of accusation and denial, of very low probability claims and very high impact consequences, left the community divided long after the verdict."),
]

OUT = os.path.join(BASE, "probe-results-part2-round2.json")


def main():
    results = {}
    for pid, idx, text in PROBES:
        att = get_activation(idx, text)
        rec = {"index": idx, "text": text, "ok": att["ok"],
               "max_activation": att.get("max_activation")}
        if att["ok"]:
            resp = att["response"]
            toks, vals = resp["tokens"], resp["values"]
            order = sorted(range(len(vals)), key=lambda i: -vals[i])[:3]
            rec["top_tokens"] = [
                {"token": toks[i], "value": round(vals[i], 2)} for i in order
            ]
        results[pid] = rec
        print(f"{pid} idx{idx}: max={rec['max_activation']} top={rec.get('top_tokens')}")
        time.sleep(0.3)
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
