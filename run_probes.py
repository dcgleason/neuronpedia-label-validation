#!/usr/bin/env python3
"""Follow-up probes for five silent pilot features.

Predictions were written to probe-predictions.md before this ran.
Results save incrementally to probe-results.json.
"""
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
    # idx 14719 colors
    ("c1", 14719, "The color of the first wire is red, and the color of the second wire is black."),
    ("c2", 14719, "Red, green, blue, and yellow are all colors."),
    ("c3", 14719, "She painted the kitchen walls a soft green color."),
    ("c4", 14719, "Set the background color to #FF0000 and the text color to white."),
    ("c5", 14719, "tft.add_text(0, 0, COLOR_MENU_TEXT, label);"),
    ("c6", 14719, "The walls were painted red and green."),
    ("c7", 14719, "Colorado is a state in the western United States."),
    # idx 2081 punctuation
    ("p1", 2081, "The meeting ended early. Then everyone went home for the night."),
    ("p2", 2081, "The meeting ended early"),
    ("p3", 2081, "She sold the car on Tuesday. The buyer paid in cash."),
    ("p4", 2081, "The report was complete.\n\nQuarterly Results\n\nSales rose in every region last year."),
    ("p5", 2081, "He paused... then continued speaking."),
    ("p6", 2081, "Did the meeting end early? Yes, it ended at noon."),
    ("p7", 2081, "\"The meeting is over.\" She stood up and left."),
    ("p8", 2081, "The trial period lasted six weeks. It ended in June."),
    # idx 2625 genetics
    ("g1", 2625, "The results were clear.\n\nVale de Lua \u2013 Moon Surface on Earth\n\nThe valley terrain is all covered with rock formations."),
    ("g2", 2625, "The results were clear.\n\nGenetics and Molecular Biology\n\nThe study of genes examines how traits pass from parents to children."),
    ("g3", 2625, "The BRCA1 mutation affects DNA repair in the cell. Researchers used PCR to amplify the gene, then sequenced the alleles to identify the inherited variant."),
    ("g4", 2625, "The experiment worked.\n\nQ:\n\nHow do I sequence a DNA sample in the lab?"),
    ("g5", 2625, "The valley terrain is all covered with rock formations and intricate labyrinths created by nature."),
    # idx 2580 literature
    ("l1", 2580, "This dark fantasy novel will appeal to fans of Angela Carter and Emma Donoghue. The book follows a young witch through a haunted forest, and this limited hardcover edition is illustrated by Kathleen Jennings."),
    ("l2", 2580, "Fans of Angela Carter and Emma Donoghue will enjoy this book."),
    ("l3", 2580, "Shakespeare wrote Hamlet around 1600, while he was living in London. The play remains his most studied tragedy, and scholars still debate why the prince delays avenging his father's murder."),
    ("l4", 2580, "Alien Brigade is a light-gun game released for the Atari 7800. Similar in style to Operation Wolf, it tells the story of a soldier fighting an alien invasion."),
    ("l5", 2580, "This biology textbook covers cell structure and genetics in twelve chapters, with review questions at the end of each chapter, and will appeal to students of introductory biology."),
    # idx 18 food
    ("f1", 18, "Five out of the top 10 altered functions were categorized as 'cell death and survival' where these gene sets were predicted to be activated."),
    ("f2", 18, "Cell death and survival are important topics in biology."),
    ("f3", 18, "Cal Poly San Luis Obispo College of Architecture and Environmental Design"),
    ("f4", 18, "He graduated with two B.S. degrees in Aerospace Engineering and Mechanical Engineering from the College of Engineering, Architecture, and Technology."),
    ("f5", 18, "The food festival served fish, burgers, and fresh bread."),
    ("f6", 18, "Food is served at noon in the cafeteria."),
    ("f7", 18, "Environmental design students study architecture and urban planning."),
    ("f8", 18, "She studied mathematics at a large public university in Oklahoma."),
]

OUT = os.path.join(BASE, "probe-results.json")


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
        print(f"{pid} idx{idx}: max={rec['max_activation']} "
              f"top={rec.get('top_tokens')}")
        time.sleep(0.3)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
