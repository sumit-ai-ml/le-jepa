# JEPA Alignment under Partial Observability

Research review and proposed follow-up to Randall Balestriero and Yann LeCun's **Proving and Improving the Platonic Representation Hypothesis with JEPAs** ([arXiv:2610.39302v1](https://arxiv.org/html/2610.39302v1), 29 October 2026).

Prepared on 5 November 2026. This repository records a research assessment, proposed experiments, and a small mathematical sanity check. Neural training experiments have **not** been reproduced here, and the proposed method has no measured performance or established novelty yet. This is an independent research notebook, not the authors' implementation.

## Assessment

There is a credible follow-up study in understanding how independently trained models align when their observations reveal incomplete or unreliable information. The first priority is to establish a reproducible failure case, then test whether a minimal intervention improves useful transfer at comparable cost.

## What the headline establishes

The authors report the following agreement between text representations and DINOv2 image representations on WIT:

| Text encoder | Mutual 10-nearest-neighbor alignment, higher is better |
| --- | ---: |
| Their 109M good-view JEPA | 0.184 |
| Qwen2.5-72B | 0.154 |
| Llama-3-70B | 0.151 |

These are alignment scores, not general-intelligence or reasoning scores. The sample-efficiency comparison is approximately **42 times fewer samples and 14 times fewer text tokens**, not a measured 42-fold compute reduction. Sources: [paper, Sections 4.2–4.3](https://arxiv.org/html/2610.39302v1#S4), [authors' repository](https://github.com/galilai-group/prh-proof).

The theorem assumes injective observations, population optima, and solutions unique up to rotation; its spectral specialization requires an eigengap. The authors disclose captioning-teacher influence, unequal hyperparameter tuning, and regularization selection using WIT. These qualify interpretation without invalidating the controlled view comparisons. Source: [paper, Section 2, conclusion and Appendix C](https://arxiv.org/html/2610.39302v1).

## Research direction 1: incomplete views

Consider a scene containing a red car beside a tree. One caption says "a parked vehicle"; another says "a tree beside the road." They describe the same scene while exposing different facts.

Forcing their entire representations to agree may discard useful details. The proposed extension would:

1. Identify information recoverable from both views.
2. Align that shared component.
3. Preserve information present in only one view.
4. Estimate when observations are too ambiguous to support confident alignment.

The theoretical target is a guarantee about recovery of shared information, with explicit dependence on information missing from each view, finite data, and the assumptions needed to identify a common geometry. Such a guarantee has not been proved here.

A possible application is medical imaging: a scan and a report can share some findings while each contains information absent from the other. This is a research motivation, not a validated clinical claim.

## Research direction 2: when is common geometry identifiable?

The following original illustrative calculation shows why the uniqueness condition matters.

Take four equally likely scenes and two scalar encodings:

$$
h_1=(-1,-1,1,1),\qquad h_2=(-1,1,-1,1).
$$

Both encodings have zero mean and unit variance. Suppose positive pairs connect independent observations of exactly the same scene, and each encoder depends only on scene identity. Both then achieve zero within-scene squared prediction loss.

In one dimension, the orthogonal group is $O(1)=\{-1,+1\}$. Neither sign aligns the two encodings:

$$
\min_{q\in\{-1,+1\}}\frac14\sum_{i=1}^{4}(h_{1,i}-q h_{2,i})^2=2.
$$

The normalized scene-level positive kernel is the identity, so it has no gap after the first nonconstant eigenvalue. The example lies outside the theorem's uniqueness assumption. **It is not a counterexample to the stated theorem**, and it is not an experiment on the full LeJEPA training objective.

It demonstrates that grouping observations by scene does not by itself specify relationships between different scenes. The research question is which additional structure—relations between scenes, temporal transitions, or restrictions on the encoder—makes the common geometry identifiable.

Run the standard-library-only calculation:

```bash
python3 examples/identifiability_sanity_check.py
```

Expected result: each mean is 0, each variance is 1, each same-scene loss is 0, and the best orthogonal alignment MSE is 2.

## Research direction 3: stronger experimental controls

| Proposed experiment | Question it resolves |
| --- | --- |
| Equal tuning budgets and independent validation/test sets | Does an improvement survive fair model selection? |
| Matched-token and matched-FLOP comparisons | What is the actual efficiency advantage? |
| Human versus generated captions | How much does the result depend on a captioning teacher? |
| Controlled omission of facts and corruption of pair identities | How robust is the method to incomplete or unreliable views? |
| Unseen combinations of objects, attributes and relations | Does alignment retain distinctions needed for compositional transfer? |
| Causal-attention JEPA and bidirectional language baselines | Which effects come from the attention pattern, objective, or views? |

These controls should test a specific mechanism rather than merely expand the benchmark list. Existing experiments should be checked before claiming any added evaluation is new.

## Recommended starting point

Start with a small text encoder, frozen image features, and human captions. Reproduce the original good-view baseline before testing an overlap-aware version. Include simple filtering and shared-subspace baselines. Use at least three training seeds and evaluate both cross-modal transfer and retention of information unique to a view.

Success means stronger robustness or transfer at comparable cost without erasing useful information. A higher alignment score alone is insufficient. The detailed staged protocol is in [docs/experiment_plan.md](docs/experiment_plan.md).

The authors provide a single-GPU starting experiment in their [repository](https://github.com/galilai-group/prh-proof). Compatibility and throughput on a DGX Spark should be measured before estimating larger training costs.

## Novelty boundary

Shared/private information separation is already explored by [M3-JEPA (ICML 2025)](https://proceedings.mlr.press/v267/lei25b.html). [Multi-View Causal Representation Learning with Partial Observability (ICLR 2024)](https://arxiv.org/abs/2311.04056) provides related identifiability theory. [When Does LeJEPA Learn a World Model?](https://arxiv.org/abs/2605.26379) is another relevant theoretical comparison.

Simply adding shared/private heads, weighting pairs, or stating that views are incomplete would not establish novelty. A defensible contribution must specifically advance independently trained encoders under incomplete views, through a new result or a convincing empirical mechanism. The literature check so far is preliminary, not an exhaustive novelty review.

## Sources

- Balestriero and LeCun, *Proving and Improving the Platonic Representation Hypothesis with JEPAs*: https://arxiv.org/html/2610.39302v1
- Original implementation and reproduction instructions: https://github.com/galilai-group/prh-proof
- Lei et al., *M3-JEPA: Multimodal Alignment via Multi-gate MoE based on the Joint-Embedding Predictive Architecture*: https://proceedings.mlr.press/v267/lei25b.html
- Yao et al., *Multi-View Causal Representation Learning with Partial Observability*: https://arxiv.org/abs/2311.04056
- Klindt, LeCun and Balestriero, *When Does LeJEPA Learn a World Model?*: https://arxiv.org/abs/2605.26379

No original-paper text, datasets, model weights, or third-party source files are bundled here.
