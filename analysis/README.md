# Analysis

Independent fact-check of this repository's README, experiment plan and example script against the authors' released code and data.

- [review.md](review.md): the full review. It contains claim-by-claim tables, exact replacement wording, the theory and mathematical checks, a novelty comparison, an audit of the experiment plan, and a proposed falsifying experiment.
- `scripts/`: the computations the review cites. They need numpy and a checkout of [galilai-group/prh-proof](https://github.com/galilai-group/prh-proof); the review used commit a2b9949.

```bash
git clone https://github.com/galilai-group/prh-proof
export PRH_PROOF=$PWD/prh-proof
python3 analysis/scripts/numbers_check.py     # headline ratios, seed statistics, FLOP estimate
python3 analysis/scripts/math_independent.py  # four-scene example and partial-observability checks
python3 analysis/scripts/two_coarsenings.py   # two partially observed modalities sharing one factor
```

The paper text itself could not be accessed during the review. Paper section numbers and theorem wording are therefore marked as unresolved in the review.
