# Proposed experiment plan

Status: planned. No neural experiments in this plan have been run. The only completed computation is the four-scene scalar sanity check in `examples/identifiability_sanity_check.py`.

## Central question

Can independently trained encoders align the information they actually share while preserving useful information unique to each observation?

Separate two questions:

1. Under what assumptions is a common representation identifiable at all?
2. Given an identifiable shared component, can a practical training recipe recover it more reliably or cheaply?

Neither follows automatically from an improvement in nearest-neighbor overlap.

## Stage 1: controlled finite worlds

Construct scenes with known factors, such as shape, color, position and background. Generate two modalities with separately controlled observation functions. Use distinct nuisance variables per observation.

Vary one mechanism at a time:

- Observability: every factor visible, a subset visible, or ambiguous observations.
- Positive structure: within-scene only, a known relationship between scenes, or controlled incorrect links.
- Encoder dimension relative to the number of recoverable factors.
- Nuisance persistence across positive pairs.
- Number of observations per scene.

Begin with closed-form spectral solutions before neural training. Compute eigengaps, principal angles, best orthogonal alignment errors, and factor-recovery scores. Report degeneracy rather than choosing a favorable basis within a tied eigenspace.

The four-scene example establishes one boundary case. The next useful check is whether adding a specified relation between scenes creates a separated shared eigenspace, and whether lossy observations preserve or destroy it.

Do not assume the raw observation space can be inverted when testing partial observability. Specify what each modality can recover and whether the shared information is nontrivial.

## Stage 2: reproduce a small neural baseline

Use the authors' released code and record its exact commit and dependencies before training. Begin with the 33M text configuration and frozen image features on human-caption data. Follow the released split and fitting protocol for the initial replication.

Record:

- Dataset versions, hashes and scene-level split assignments.
- Model configuration, initialization and checkpoint-selection rule.
- Token counts, actual view counts, optimizer steps and samples processed.
- Precision, batch size, gradient accumulation and regularization scaling.
- Wall time, measured peak memory and hardware/software versions.
- Training seeds and failed or collapsed runs.

Check the training stack and measure a short run on the DGX Spark before projecting runtime. Do not transfer GPU-hour estimates from other hardware without measurement.

## Stage 3: a minimal robustness intervention

First introduce controlled missing facts and incorrect pairs. Start with synthetic labels as an oracle for overlap, then remove access to those labels to assess a practical estimator.

Compare:

| Arm | Purpose |
| --- | --- |
| Original good-view JEPA | Main reference |
| Simple pair filtering or weighting | Tests whether a complex architecture is necessary |
| Shared/private representation baseline | Controls for an already established design |
| Proposed overlap-aware method | Candidate intervention |
| Oracle overlap version | Diagnostic reference, not a deployable comparison |

Keep parameter budgets comparable or report their differences explicitly. Isolate weights, shared/private capacity, and any auxiliary objective in separate ablations.

Avoid circular evaluation: do not use the test image encoder or test pairs to construct training weights. If a pretrained text or vision-language teacher supplies overlap scores, disclose that dependency and include it in cost and supervision comparisons. Report oracle and teacher-free settings separately.

Independently trained modalities are the target setting. If a variant requires cross-modal paired training, label it as a separate supervised setting rather than attributing its results to independent training.

## Stage 4: fair evaluation

Use scene-disjoint splits. Fit all maps, thresholds and rank selections on training or validation data only. Freeze model and layer choices before final test evaluation.

At minimum, compare three seeds. Prefer five when variance is large. Report individual runs, mean, variability, and the number of failures. Estimate uncertainty at the scene level so multiple captions of one scene are not treated as independent examples.

Evaluate:

- Retrieval at ranks 1 and 5, with candidate-set size stated.
- Neighborhood alignment and an additional geometry metric.
- Best-rotation error with fitting and evaluation samples kept separate.
- Recovery of shared factors and factors visible to only one modality.
- Transfer to held-out combinations and a separate dataset.
- Robustness as missing information and incorrect-pair rates increase.
- Calibration of any predicted overlap or reliability score.

Run matched-token and matched-FLOP studies separately; they answer different questions. Give baselines comparable tuning budgets. Include attention-mask and language-objective controls if making claims against next-token prediction.

## Decision criteria

Continue to larger training only if:

1. The original small baseline is reproducible within reasonable variability.
2. A controlled failure mechanism appears under incomplete or unreliable views.
3. The proposed intervention improves that mechanism across seeds.
4. Gains survive simple baselines, cost accounting, and held-out evaluation.
5. Improvements retain useful modality-specific information.
6. A focused related-work review identifies the actual new contribution.

An equal-cost negative result is useful: it may show that simple filtering suffices, that alignment and information preservation trade off, or that stronger assumptions are needed. No publication outcome or performance gain is guaranteed.
