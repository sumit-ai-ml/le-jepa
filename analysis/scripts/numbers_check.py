"""Recompute the headline ratios and seed statistics from the authors' CSVs; estimate FLOP ratios."""
import csv
import statistics as st
from pathlib import Path

import os
D = Path(os.environ.get("PRH_PROOF", "prh-proof")) / "paper" / "data"  # checkout of galilai-group/prh-proof
rows = list(csv.DictReader(open(D / "scaling.csv")))
f = lambda **kw: [float(r["wit"]) for r in rows if all(r[k] == v for k, v in kw.items()) and r["wit"]]  # noqa: E731
good940 = f(objective="good", encoder="BERT-B", images_M="940.0")
ntp940 = f(objective="ntp", encoder="BERT-B", images_M="940.0")
bad940 = f(objective="bad", encoder="BERT-B", images_M="940.0")
good216 = f(objective="good", encoder="BERT-B", images_M="2.16")
for name, v in (("good BERT-B 940M", good940), ("ntp BERT-B 940M", ntp940), ("bad BERT-B 940M", bad940), ("good BERT-B 2.16M", good216)):
    print(f"{name}: seeds {v} mean {st.mean(v):.4f} sd {st.stdev(v):.4f}")
print("match rule of figures.py teaser: good run with fewest samples and wit >= ntp - 0.005 ->", st.mean(good216), ">=", st.mean(ntp940) - 0.005)
print("samples ratio 900e6 / 21.6e6 =", 900 / 21.6)
per = {"good": 128.4, "ntp": 42.8}
print("tokens: good 21.6e6 x 128.4 = %.3e ; ntp 900e6 x 42.8 = %.3e ; ratio = %.2f" % (21.6e6 * per["good"], 900e6 * per["ntp"], (900e6 * per["ntp"]) / (21.6e6 * per["good"])))
pr = list(csv.DictReader(open(D / "phase_real.csv")))
for r in pr:
    if r["encoder"] == "BERT-B" and r["images_M"] in ("2.16", "940.0"):
        print("phase_real:", r["model"], r["objective"], "samples", r["samples"], "tokens", r["tokens"], "wit", r["wit"], "seeds", r["seeds"])
# --- FLOP estimate (deduction) ---
width, layers, vocab = 768, 12, 30522
body = layers * (4 * width ** 2 + 2 * width * 4 * width)      # non-embedding params of BERT-B
emb = vocab * width
print(f"BERT-B params: body {body/1e6:.1f}M + embeddings {emb/1e6:.1f}M = {(body+emb)/1e6:.1f}M (authors say 109M)")
w2 = 384
print(f"BERT-S params: body {(12*(4*w2**2+2*w2*4*w2))/1e6:.1f}M + emb {(vocab*w2)/1e6:.1f}M = {(12*(4*w2**2+2*w2*4*w2)+vocab*w2)/1e6:.1f}M (authors say 33M)")
fwd_tok = 2 * body                     # FLOPs per token, forward, ignoring attention scores (<=64 tokens)
head_tok = 2 * width * vocab           # tied softmax head per position
train = 3                              # forward + backward ~ 3x forward
mean_len = 42.8
# padded execution: every text view is a 64-token tensor (prh/views.py TextView._frame pads to max_len)
jepa_padded = 8 * 64 * fwd_tok * train
ntp_padded = 64 * (fwd_tok + head_tok) * train
# 'useful token' accounting: 2 global views of U(.5,1) x len, 6 local of U(.15,.5) x len, +2 specials each
jepa_useful = (2 * (0.75 * mean_len + 2) + 6 * (0.325 * mean_len + 2)) * fwd_tok * train
ntp_useful = (mean_len + 2) * (fwd_tok + head_tok) * train
print(f"per-sample FLOPs, padded execution: JEPA {jepa_padded:.3e}  NTP {ntp_padded:.3e}  JEPA/NTP = {jepa_padded/ntp_padded:.2f}")
print(f"per-sample FLOPs, useful tokens:    JEPA {jepa_useful:.3e}  NTP {ntp_useful:.3e}  JEPA/NTP = {jepa_useful/ntp_useful:.2f}")
print(f"total training FLOPs ratio NTP(900M)/JEPA(21.6M): padded {900e6*ntp_padded/(21.6e6*jepa_padded):.1f}x ; useful-token {900e6*ntp_useful/(21.6e6*jepa_useful):.1f}x ; samples 41.7x ; tokens 13.9x")
