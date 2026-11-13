#!/usr/bin/env python3
"""Part 2 probes: the remaining 12 silent features.
Predictions in probe-predictions-part2.md. Results save incrementally."""
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
    ("a1", 1029, "In Chinese mythology, Chang'e flew to the moon and lives there still."),
    ("a2", 1029, "Tianxiang was a famous general of the Song dynasty, honored as a god."),
    ("a3", 1029, "return \"@TianxiangCard=\" .. id .. \"->\" .. name"),
    ("a4", 1029, "The Xiang River flows through Hunan province in China."),
    ("a5", 1029, "Zeus and Hera ruled from Mount Olympus."),
    ("b1", 3070, "As mentioned, in itself, chasing reputation, even if it is the only motivation, is a poor reason to answer."),
    ("b2", 3070, "His reputation grew with every answer he posted on the forum, and users upvoted his posts."),
    ("b3", 3070, "The quarterback signed the franchise tag on Tuesday."),
    ("b4", 3070, "Reputation, reputation, reputation. The site runs on reputation points."),
    ("d1", 3349, "Scale Your Investment: our speaker advised participants to start small and grow.\n\nBroad Reach\n\nResearch done through mobile apps has been proven effective."),
    ("d2", 3349, "Our commitment to diversity and inclusion: we welcome employees of every background."),
    ("d3", 3349, "The company values diversity and inclusion in hiring."),
    ("d4", 3349, "Agenda:\n\nWelcome\nKeynote\nBreakout Sessions\nClosing"),
    ("e1", 3580, "He is survived by his loving wife of 42 years, Margaret, and his two sons."),
    ("e2", 3580, "George is preceded in death by his father and his brother."),
    ("e3", 3580, "Funeral services will be held Saturday at the First Baptist Church. He was a devoted husband, father, and grandfather."),
    ("m1", 5072, "Reperfusion injury occurs when blood flow returns to tissue after a period of ischemia."),
    ("m2", 5072, "The patient presented with positional vertigo and was treated for radiation-induced fibrosis."),
    ("m3", 5072, "Chronic overuse syndromes of the elbow joint may lead to lateral epicondylitis."),
    ("u1", 5158, "<button class=\"btn btn-primary\" type=\"submit\">Submit</button>"),
    ("u2", 5158, ".btn-default { color: #333; background-color: #fff; }"),
    ("u3", 5158, "Click the btn to continue."),
    ("u4", 5158, "Press the button to continue."),
    ("s1", 6515, "supra shoes, supra shoes on sale now, buy supra shoes at the best price, supra shoes the seals, nowhere"),
    ("s2", 6515, "nike shoes, nike shoes on sale now, buy nike shoes at the best price"),
    ("s3", 6515, "Shoes, shoes, shoes. The store sells shoes of every kind."),
    ("w1", 7196, "The jury found that the company had discriminated against Black employees in promotions over a ten-year period."),
    ("w2", 7196, "In its findings, the commission concluded that the remarks constituted severe and pervasive harassment."),
    ("w3", 7196, "It's not as bad as what happened in the Brawley case, the attorney argued."),
    ("q1", 7623, "How do I reset my router?\n\nI have tried unplugging it and it still blinks red. Please answer me! Answers: 2"),
    ("q2", 7623, "How can I get NBA 2K9 for PS2? Please answer me!"),
    ("q3", 7623, "Frequently asked questions\n\nQ: Where is my order?\nA: It ships in two days."),
    ("t1", 8630, "The singer joins the show this week to talk about her new album and the tour."),
    ("t2", 8630, "Sosa joins Team LeftJab Boxing Radio to talk about last weekend's fight."),
    ("t3", 8630, "In this episode, the host talks with a jazz pianist about their collaboration."),
    ("t4", 8630, "She released a new album on Friday."),
    ("n1", 8743, "They won't explore the boundaries of their fields, or see the technical trends coming."),
    ("n2", 8743, "Take the money or leave it; the choice is yours, or walk away entirely."),
    ("n3", 8743, "Neither the manager nor the employees were told about the change."),
    ("n4", 8743, "It was not the only factor, or even the main one necessarily."),
    ("v1", 14520, "Sufficient; and the Administration has always been best executed, and the Publick Liberty best preserved, under such forms."),
    ("v2", 14520, "In Arizona, you know there is water when you see large trees."),
    ("v3", 14520, "The government of the people, by the people, for the people, shall not perish from the earth."),
]

OUT = os.path.join(BASE, "probe-results-part2.json")


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
