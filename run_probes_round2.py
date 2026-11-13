#!/usr/bin/env python3
"""Round 2 probes. Predictions in probe-predictions-round2.md."""
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
    ("r1", 2081, "The court cited the earlier ruling (Colo. 2000)). In contrast, the principles underlying the statute pointed the other way, as later cases confirmed."),
    ("r2", 2081, "The trail wound through the pines for nearly a mile before it reached the river. Maria walked slowly, listening to the water over the stones. She had come here every summer since she was a child, first with her father and later on her own. The cabin stood where it always had, past the bend, its porch sagging a little more each year. She set her pack down by the door and looked out at the hills. Nothing about the place had changed, and that was the point."),
    ("r3", 2081, "Signaling in immune cells ([@bib0190]). Due to the importance of JAK-STAT signaling, the pathway has been studied extensively in recent years."),
    ("r4", 2625, "func decodeMessage<D: Decoder>(decoder: inout D) throws { if lhs.unknownFields != rhs.unknownFields { return } }"),
    ("r5", 2625, "The BRCA1 gene encodes a protein that repairs damaged DNA in human cells. Mutations in this gene disrupt homologous recombination and raise the risk of breast and ovarian cancer. In this study, we sequenced tumor samples from 214 patients and identified 31 distinct variants. Several variants clustered in the RING finger domain, a region critical for the protein's ubiquitin ligase activity. These findings suggest that variant position, alongside variant type, shapes clinical risk."),
    ("r6", 2625, "Q:\n\nnatural language query processing\n\nI have a NLP (natural language processing application) running that gives me a tree of the parsed sentence."),
    ("r7", 2580, "Hamlet is a tragedy by William Shakespeare. The play tells the story of a prince who delays avenging his father's murder."),
    ("r8", 2580, "Pride and Prejudice is a novel by Jane Austen. It tells the story of Elizabeth Bennet, her four sisters, and the proud Mr. Darcy."),
    ("r9", 2580, "This novel will appeal to fans of Shakespeare and Dickens."),
]

OUT = os.path.join(BASE, "probe-results-round2.json")


def main():
    results = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            results = json.load(f)
    for pid, idx, text in PROBES:
        if pid in results and results[pid].get("max_activation") is not None:
            print(f"{pid}: already scored {results[pid]['max_activation']}")
            continue
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
        else:
            rec["error"] = att.get("error")
            rec["status"] = att.get("status")
            if att.get("status") in (401, 403):
                print(f"{pid}: authorization failure, stopping.")
                with open(OUT, "w") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                return 3
        results[pid] = rec
        with open(OUT, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"{pid} idx{idx}: max={rec['max_activation']} top={rec.get('top_tokens')}")
        time.sleep(0.3)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
