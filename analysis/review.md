# Independent review of sumit-ai-ml/le-jepa

Reviewed: README.md, docs/experiment_plan.md and examples/identifiability_sanity_check.py at commit 125c19c. The review itself changed none of those files; it was added to this folder afterwards.

Compared against: the authors' code and released data, galilai-group/prh-proof at commit a2b9949, including `prh/theory.py`, `prh/metrics.py`, `prh/views.py`, `prh/models.py`, `train.py`, `evaluate.py`, `tables.py`, `figures.py`, `docs/reproduce.md`, `docs/data.md`, `paper/data/*.csv` and `paper/runs.csv`.

**Status labels used throughout**

- **V** means a verified fact: read in the authors' code or data, or computed and run in this review.
- **D** means a deduction: it follows from verified facts but was not stated by the authors or checked against the paper text.
- **U** means unresolved: it needs the paper text or a source that could not be reached.

Theorem numbers are the ones in the docstrings of `prh/theory.py`. They may not match the paper's numbering.

---

## 1. What could and could not be checked

- **The paper text was unreachable.** arxiv.org and every mirror tried were blocked by this session's network policy. One attempt to reach archived copies was refused by the session's permission system and was not retried. Paper section numbers, equation numbers, appendix letters and the exact wording of theorem hypotheses are therefore **U**. Every number below was checked against the authors' released data instead. The authors' `docs/reproduce.md` maps each paper figure and table to the script and CSV that produce it, and section numbers are cited from that index. Allowing arxiv.org under the environment's network settings would let these items be closed.
- **Literature was checked at abstract level.** The sources were web-search listings plus cloned code and READMEs of M3-JEPA, lejepa-identifiability (Lean proofs), cave_umwelten, platonic-rep, stable-pretraining and unpaired-rosetta. Full texts of Yao et al. 2024, Daunhawer et al. 2023, FactorCL, DeCUR, CoMM, Gröger et al. 2026 and Koepke et al. 2026 were not read.
- **What was executed:**
  - the repository's script;
  - the authors' finite-world theory tests without the torch-dependent Prop. 3 test: 36 passed;
  - three scripts written for this review: `scripts/numbers_check.py`, `scripts/math_independent.py` and `scripts/two_coarsenings.py` in this folder;
  - a verification workflow of 16 agents. Five fact-checkers produced 103 findings, and each finding was attacked by two independent verifiers. 83 survived both, 19 were contested by one verifier, and 1 was refuted. I adjudicated the contested ones and say so where it matters.
- **What was not executed:** any neural training or evaluation. The session has no GPU, no torch and no datasets.

---

## 2. Overall assessment

The repository is careful and mostly accurate. Its headline numbers match the authors' data exactly. Its main hedges are correct: "not a counterexample", "not a measured compute reduction" and "no established novelty".

Its weaknesses are of four kinds.

1. **The headline numbers are under-specified.** The 42× figure uses a 0.005 tolerance, and the matched JEPA score is 0.109, not the 0.184 headline. The 14× figure counts the texts available per item, not the tokens processed. The WIT score is a maximum over layer pairs taken on the scored pairs. The section citation is probably wrong. One disclosure is paraphrased as something the authors do not say.
2. **The theory is read as all-or-nothing.** The repository omits the authors' Thm. 2–4, which bound what happens when the assumptions fail. It also presents "relations between scenes" as an open question, but the world kernel π(z, z′) is the authors' own primitive and already encodes them.
3. **The mathematical example is correct but weakly tested.** The script hard-codes the spectral claims and its loss function is a tautology. The README omits that the failure needs an embedding dimension k below |Z| − 1. On its own the example is the tie case that the authors' code already flags. It becomes useful only when tied to the question of what defines the "state" kernel on real data.
4. **The novelty boundary and the plan point at the wrong places.** The novelty boundary relies on M3-JEPA, a weak anchor, while the closest existing theory is understated: Yao et al. 2024 and Daunhawer et al. 2023, plus the paired shared/unique self-supervised learning literature. The plan has these gaps:
   - no bad-view or next-token arm in its main comparison;
   - no primary endpoint or power analysis;
   - no FLOP definition;
   - no rule for teacher-written training texts;
   - no instance of the decisive case.

**The strongest direction** is partial observability with a modality-private factor that persists across one modality's views. The authors' constructions never build this case, because every observation determines its state. My computations and two independent verifier scripts agree on the population-level answer. Two independently trained spectral JEPAs agree only on the intersection of their leading eigenspaces. They align on a shared factor exactly when that factor ranks within the top k of both modalities' spectra. The open research question is whether trained LeJEPAs follow this prediction. Section 9 gives a cheap experiment that could falsify it.

---

## 3. Claim-by-claim table

### README.md

| # | Location | Claim | Verdict | Evidence | Correction |
|---|---|---|---|---|---|
| 1 | L3, L99 | Title, authors, arXiv:2610.39302v1, 29 Oct 2026 | Verified, with a caveat | **V**: title and authors from the authors' README L1, L4 and BibTeX L166–170. **D**: the id and date come from consistent secondary listings. **U**: the "v1" suffix and exact date need arXiv. | None |
| 2 | L13 | "agreement between text representations and DINOv2 image representations on WIT" | Incomplete | **V**: the benchmark is WIT-1024 of Huh et al. 2024 (`docs/data.md` L29–30). The image model is DINOv2 ViT-B/14 (`tables.py` L52, `reproduce.md` L32). The score is mutual 10-NN after 0.95-quantile clipping and L2 normalisation, maximised over all text-layer and image-layer pairs on the same 1,024 scored pairs (`prh/metrics.py` `prh_score` L83–104). The size of DINOv2 matters: with DINOv2-g the scores become .203, .169 and .166 (`llm_scale.csv`). | Name WIT-1024, ViT-B/14 and the max over layer pairs. See section 4. |
| 3 | L15 | "Mutual 10-nearest-neighbor alignment, higher is better" | Verified | **V**: `metrics.py` `mutual_knn`. Chance is about k/N ≈ 0.01. | Optionally state the chance level. |
| 4 | L17 | "Their 109M good-view JEPA, 0.184" | Correct but incomplete | **V**: this is the mean of three BERT-B seeds at 940M images, .191, .181 and .179 (`scaling.csv` rows 39, 47, 45; `phase_real.csv` .1837). The backbone has 108.9M parameters without the pooler (`models.py` L18, L67); the ~6.7M LeJEPA projector is not counted. **V**: a fourth 940M run at twice the effective SIGReg weight scored .121 (authors' README L39; `reproduce.md` L156–159; `runs.csv` L127). | Say "three-seed mean" and footnote the .121 run. Do not average the four runs: the .121 run used a different effective setting. |
| 5 | L18–19 | Qwen2.5-72B .154, Llama-3-70B .151 | Verified | **V**: `references.csv` and `llm_scale.csv`. These are the authors' own evaluations of frozen models. With CLIP ViT-H as the image model the scores are .230 for the JEPA against .210 and .206 (authors' README L40). | Optional note: "authors' evaluation of frozen models". |
| 6 | L21 | "alignment scores, not general-intelligence or reasoning scores" | Correct but understated | **V**: the table holds no downstream task result. **V**, abstract level: Koepke et al. 2026 (arXiv 2604.18572; `cave_umwelten` README) report that mutual k-NN agreement falls sharply as the gallery grows from 1,024 items toward millions. Gröger, Wen and Brbić 2026 (arXiv 2602.14486) argue that max-over-layer aggregation inflates raw scores. | Add the protocol and these two limits. |
| 7 | L21 | "approximately 42 times fewer samples" | Arithmetic verified; definition missing | **V**: 900M / 21.6M = 41.7. The comparison is good-view JEPA against next-token prediction, both on BERT-B. The rule in `figures.py` teaser L536–542 takes the fewest-sample good run with WIT ≥ NTP − 0.005. That run is 2.16M images × 10 epochs, scoring .109 against NTP's .111. Without the tolerance the ratio is 22.5×, at 40M samples. The matched level is .109, not .184. The two arms also differ: lr 1e-4 on 1 GPU against lr 2e-4 on 8 × 256 (`runs.csv` L32 vs L132), and 2.16M against 940M unique images. | See section 4. |
| 8 | L21 | "14 times fewer text tokens" | Arithmetic verified; ambiguous | **V**: `tables.py` `PER_SAMPLE` gives good 128.4 and NTP 42.8 tokens per item. 21.6M × 128.4 against 900M × 42.8 gives 13.9×. This counts the tokens of the texts an item draws from. The good arm actually encodes 8 cropped views, 2 global and 6 local (`views.py` L49–57, `train.py` defaults). **D**: the ratio of tokens actually processed is about 11×. | State the counting rule. See section 4. |
| 9 | L21 | "not a measured 42-fold compute reduction" | Correct | **V**: no FLOP figure exists in the authors' data. GPU-hours are reported only per arm at 940M. **D**: training FLOPs differ by about 6.6× if padded views are counted (every view is padded to 64 tokens, `views.py`) and 14.6× if only useful tokens are counted. Attention scores, the projector and SIGReg are ignored in both estimates (`numbers_check.py`). | Add the estimate, labelled as an estimate. |
| 10 | L21 | "paper, Sections 4.2–4.3" | Probably incorrect | **D**: the authors' index places the 42× figure in Fig. 1 (`reproduce.md` L39) and the WIT and language-model tables under "Sec. 4.4, 4.5, appendix" (L58, L136). Sec. 4.3 is MSR-VTT (L118). The index also lists 4.4 under the Flickr heading, so it is not fully consistent. **U** against the paper. | Cite Fig. 1 and the WIT and language-model tables, with section numbers marked as taken from the authors' index. |
| 11 | L23 | "The theorem assumes injective observations" | Correct for Thm. 1; direction should be explicit | **V**: `theory.py` L96 "g injective"; L155 says (state, nuisance) → observation is injective; Thm. 4 indexes observations by a single-valued `state[x]` (L208–216). In every construction each observation determines one state. An observation compatible with several states is never modelled. A many-to-one probe of `render()` returns mass 0.589 instead of 1. | "each observation is a rendering of exactly one world state" |
| 12 | L23 | "population optima" | Verified | **V**: every object in `theory.py` is an exact expectation. No finite-sample statement exists. | None |
| 13 | L23 | "solutions unique up to rotation; its spectral specialization requires an eigengap" | Misframed for the released model; **U** for the paper | **V**: under E h = 0 and E hhᵀ = I, the minimiser of the squared-loss JEPA is always the top-k eigenspace (Prop. 1; `test_theory.py` L41–53). It is unique up to rotation iff μ_k > μ_{k+1} (`theory.py` L45). In the code these are one condition, not two. **U**: the paper may state Thm. 1 for a general loss with uniqueness as a hypothesis. The authors' change-of-variables lemma is loss-general (`test_theory.py` L31–37). The verifiers split on this point. | Merge into one clause: "an eigengap μ_k > μ_{k+1}, which is what makes the minimiser unique up to rotation". |
| 14 | L23 | Assumptions listed as caveats only | Understated | **V**: the theory has a quantitative half for when the assumptions fail, and the repository never mentions it:<br>• Thm. 2 is a Davis–Kahan bound, 2√2/δ · min(√k‖E‖op, ‖E‖HS), for mismatched kernels (`theory.py` L88–92). It held in 300 of 300 re-run cases.<br>• Thm. 3 is a lower bound, 2(k − tr C^{1/2}), on cross-modal error from kept nuisance (L180–194).<br>• Thm. 4 is a coverage bound in η and ε that covers random wrong pairs through `mixed_views` with weight `move` (L219–247, L270–275).<br>The repository's robustness proposals, README L77 and plan L51, re-raise what these bound. | Add one sentence on Thm. 2–4. See section 4. |
| 15 | L23 | "disclose captioning-teacher influence" | Verified | **V**: `docs/data.md` L41–42, citing "paper, Sec. 6", and `text_sources.csv`. | None |
| 16 | L23 | "disclose ... unequal hyperparameter tuning" | Fact verified; disclosure **U** | **V**: the sweep in `ablations.csv` contains only good-view variants plus single bad-view and NTP reference rows (`reproduce.md` L110). The controls reuse the good arm's lr, clipping and batch at every scale (`runs.csv`). **U**: whether the paper itself calls this a limitation. | Describe the fact and mark the disclosure as unchecked. |
| 17 | L23 | "disclose ... regularization selection using WIT" | Mischaracterized | **V**: the authors describe a weight-matching rerun. SIGReg is computed per GPU at revision ab836bf, so seeds 1–2 were rerun at λ .01 on 256 per GPU to match seed 0's effective weight, and the .121 run is reported separately (`reproduce.md` L156–159; authors' README L39). **D**: job ids and dates show the .121 run finished before the reruns were launched. **U**: whether the paper calls this selection. Separately, **V**: the robustness sweep is scored on Flickr test R@1, and the authors disclose one test-selected column in it, best epoch (`reproduce.md` L18–19). | See section 4. |
| 18 | L23 | "without invalidating the controlled view comparisons" | Defensible; needs the data | **V**: within each text source both arms read the same texts (`data.py` `pick`), so the comparisons are controlled. **V**: on human captions the gap is large. Flickr R@1 is about .25 against .13 for bad views and .12 for NTP. MSR-VTT gives .066–.068 against .036–.043. **V**: at web scale the gap depends on the text source (`text_sources.csv`):<br>• LLaVA recaptions only, 50M images: good mean .096 against bad .092;<br>• alt-text plus text-only paraphrase, 2.24M images: good .058–.061 against bad .054–.056;<br>• all three texts, 2.24M images: good .095–.115.<br>The verifiers split; the wording keeps "controlled" and qualifies the cause. | See section 4. |
| 19 | L23 | "Section 2, conclusion and Appendix C" | Partly verified | **V**: Sec. 2 is the theory (`reproduce.md` L65). The captioner discussion is in Sec. 6 (`data.md` L42). The SIGReg matter is in "paper, appendix" (`reproduce.md` L159). **U**: the letter C. | Keep the appendix citation and mark the letter as unverified. |
| 20 | L9 | "establish a reproducible failure case" | Under-specified | **V**: the authors already release failure cases for unreliable views: nuisance-keeping bad views (WIT .088/.085/.088 against .191/.181/.179 at 940M), kernel mismatch (Thm. 2) and low coverage (`coverage_sweep.csv`). The case they lack is many-to-one observations. | Name the missing case. See section 4. |
| 21 | L27–34 | Direction 1, items 1–4 | Overstated as open | **D**, abstract level:<br>• items 1–2 are proved for paired contrastive training (Daunhawer et al. 2023; Yao et al. 2024);<br>• item 3 has paired designs (FactorCL, DeCUR, CoMM);<br>• item 4 exists at the level of model pairs (Schnaus et al., arXiv 2503.24129 and 2610.09411; `unpaired-rosetta`).<br>**V**: Thm. 3 implies that private information kept inside the k aligned dimensions costs at least 2(k − tr C^{1/2}). The authors measure the related scene-explained fraction on real encoders: .805 good, .649 bad and .609 NTP at k = 32 (`nuisance_fraction.csv`). | Separate nuisance from persistent private factors and cite the prior work. See section 4. |
| 22 | L36 | Theoretical target "has not been proved here" | True, but pieces exist | **V** numerically, **D** as interpretation: take the shared coarse label as Thm. 3–4's "state" and a modality's extra detail as "nuisance". The authors' functions then bound deterministic coarsenings, and the bound is tight in factor worlds (`two_coarsenings.py`; verifier script `part_d.py`). The lifted kernel π₂(gz, gz′)·p(z)p(z′)/(p₂(gz)p₂(gz′)) is a valid world kernel, so Thm. 2 applies, but it was usually vacuous: 6.4, 38 and 120 against a ceiling of 2k. | Restate the target as the gap between these pieces. See section 4. |
| 23 | L42 | "original illustrative calculation" | Acceptable | **V**: this four-scene instance appears nowhere in the authors' code. The mechanism is the tie case of Prop. 1. | Optional: "an instance of the tie case Prop. 1 excludes". |
| 24 | L47–55 | h1, h2, means 0, variance 1, min over signs of the MSE = 2 | Verified exactly | **V**: corr(h1, h2) = 0, so min over q of E(h1 − q h2)² = 2 − 2\|corr\| = 2 for both signs. The authors' `rotation_distance` gives √2, the root of the MSE. | None |
| 25 | L50 | Scene-only encoders reach zero loss | Verified, and stronger | **V**: under π = diag(p) every centred, unit-variance encoder has zero loss. This holds for 400 random encoders and is the actual content of the example. | Say "every whitened encoder". |
| 26 | L58 | "kernel is the identity, so it has no gap" | Verified; omits the condition on k | **V**: S = D^{-1/2} π D^{-1/2} = I, and all four eigenvalues equal 1, including the constant one, because the scenes are disconnected. **V**: the degeneracy needs k < \|Z\| − 1. At k = 3, any two whitened encoders are rotations of each other, with residual 2.8e-13. At k = 1, random pairs cover the whole range [0, 2]. **V**: the authors' code flags exactly this tie: `coverage_bound` returns inf (`theory.py` L242), and `test_theory.py` L80 skips gaps below 1e-9. | Add the k condition. See section 4. |
| 27 | L58 | "It is not a counterexample to the stated theorem" | Correct against Prop. 1 as encoded; **U** against the paper | **V**: the gap condition fails, so the theorem as encoded does not apply. **V**: the example does contradict the authors' informal summary (their README L10–12: "same embedding up to one rotation when their positive pairs are two observations of the same world state", with no gap mentioned) whenever k < \|Z\| − 1. | Keep, and add the informal-summary sentence. |
| 28 | L60 | "The research question is which additional structure ... makes the common geometry identifiable" | Overstated as open | **V**: the theory is stated for a general world kernel π(z, z′) (`theory.py` L2–5). `random_world` and `class_world` kernels have gaps and give exact agreement (`test_theory.py` L56–66, L242–253). A 6-cycle kernel ties at k = 1 and has a gap at k = 2. **D**: what remains open is what supplies cross-scene mass when positives are two captions of one image. If the state is the image, π is diagonal and the tie is generic, so identification would have to come from a coarser notion of state or from the encoder's inductive bias. | See section 4. |
| 29 | L62–68 | "standard-library-only calculation"; "expected result" | Prints as stated; verifies less than it implies | **V**: L43–44 hard-code `[1, 1, 1, 1]` and `0`, and no assert touches them. **V**: `same_scene_loss` (L24) subtracts each value from itself, so it returns 0 for any input and the assert at L49 cannot fail. | Compute the kernel and its loss. See section 4 for code. |
| 30 | L74 | "Equal tuning budgets and independent validation/test sets" | Half already done; half real | **V**: the Flickr protocol already fits means, rotation and whitening on non-test rows (`metrics.py` L51–79). A no-test-pair variant exists: `align --val-only --split 507`. **V**: the tuning asymmetry is real (row 16). **V**: the WIT headline has no held-out selection set, because its layer maximum is taken on the scored pairs. | See section 4. |
| 31 | L75 | "Matched-token and matched-FLOP comparisons" | Correct; needs definitions | **V**: the 42× comparison also changes the number of unique images, from 940M to 2.16M. The authors' scaling law separates samples M from unique images N (`tables.py` L82–89). | Add a matched-unique-image arm and a FLOP rule. |
| 32 | L76 | "Human versus generated captions" | Largely already done | **V**: `text_sources.csv` (row 18 numbers). **V**: the authors have no matched-image comparison of human and generated captions of the same images. | See section 4. |
| 33 | L77 | "Controlled omission of facts and corruption of pair identities" | Synthetic half exists; real half new | **V**: wrong pairs are modelled synthetically (`mixed_views`, `thm4_tightness`). On real data the authors mix good with bad views through `--good-views Q` (`phase_grid.csv`, 145 runs). No released run trains on mislabelled pairs: a grep of `runs.csv` finds none, and `--shuffle` is an evaluation-only control. | See section 4. |
| 34 | L78 | Unseen combinations | Not done by the authors | **V**: their only transfer test is COCO-5k with a rotation fitted on Flickr (`bench_coco.csv`). | None |
| 35 | L79 | "Causal-attention JEPA and bidirectional language baselines" | Correct gap; more confounds | **V**: no causal JEPA or masked-LM run exists (`runs.csv`). The JEPA arms use bidirectional attention with [CLS] pooling and a 768→512→2048→2048→512 BatchNorm–ReLU projector. NTP uses causal attention with mean pooling and no projector (`models.py` L45–47, L74–79; `lejepa.py` L232–245). Partial controls exist: last-token pooling (`evaluate.py` L488) and NTP on caption pairs (`runs.csv` L12–13, L86). | Add pooling and projector to the list of confounds. |
| 36 | L85 | Small encoder, frozen image features, human captions | Verified feasible | **V**: the 33M model is BERT-S at width 384 with 33.0M parameters. The authors' quick start is "one GPU, about two hours", with a good-view text run at about 1 GPU-hour and expected R@1 ≈ .25. | Name the fitting protocol (plan row 6). |
| 37 | L89 | DGX Spark: measure before projecting | Correct | Not checkable here. | None |
| 38 | L93 | "Shared/private information separation is already explored by M3-JEPA" | A weak anchor, though not false | **V**: M3-JEPA's README (L40, L62) claims its gating "disentangles ... modality-specific and shared components". **V**: in its code (`src/models/MMoE.py` L46–71) one gate routes over shared experts, with modality-specific input and output projections. It fine-tunes pretrained DINOv2 and Llama-3-8B with LoRA, trained on paired COCO batches with InfoNCE plus prediction. Its representations are not split into shared and private parts. The verifiers split on whether the sentence is wrong. | Cite FactorCL, DeCUR and CoMM for shared/unique representation learning, and describe M3-JEPA accurately. |
| 39 | L93 | Yao et al. 2024 "provides related identifiability theory" | Understated | **D**, abstract level: it proves that contrastive learning with one encoder per view identifies, up to a smooth bijection, the latents shared by any subset of views, when each view mixes a subset of the latents. That is direction 1's items 1–2 for paired training. | See section 4. |
| 40 | L93 | Klindt, LeCun and Balestriero 2026 "relevant theoretical comparison" | Correct | **V** (lejepa-identifiability README and Lean headers): it covers a single encoder with Gaussian Ornstein–Uhlenbeck positives and an invertible observation map. Whitened minimisers are rotations (Thm. 4.1), the Gaussian is the unique latent law with this property, and an approximate bound has a spectral-gap denominator (Prop. 4.3). | Optional expansion. |
| 41 | L97–105 | Sources | Incomplete | **V**: the README uses the LeJEPA objective (L58) and the Huh et al. benchmark and metric (L13–19) but cites neither. | Add LeJEPA (arXiv 2511.08544) and Huh et al. 2024 (arXiv 2405.07987), plus section 7's list. |

### docs/experiment_plan.md

| # | Location | Claim | Verdict | Evidence | Correction |
|---|---|---|---|---|---|
| 1 | L3 | Only the four-scene check has been computed | Verified | **V** | None |
| 2 | L7–14 | Central question and two sub-questions | Well posed; decisive case missing | **V**, run by me and by a verifier: when a modality-private factor outranks the shared factor at the chosen k, the two good-view spectral solutions have canonical correlation 0 although the shared information exists. With the shared factor leading, the correlation is 1. Neither Stage 1 as written nor Stage 3 on Flickr constructs this case. | Add it as the first Stage 1 world. |
| 3 | L18–26 | Five axes to vary | Four of five already exist | **V**:<br>• positive structure: `class_world`, `random_world` and `mixed_views` `move`;<br>• k against the spectrum: `spectral_solution` and `coverage_bound`;<br>• nuisance persistence: `bad_views` keep and Thm. 4's η;<br>• observations per scene: `line_alignment`, swept in `coverage_sweep.csv` and `phase_diagram.csv`.<br>Only observability, meaning many-to-one renderings, is absent. | Reuse the existing constructions and mark observability as the new axis. |
| 4 | L28 | Eigengaps, principal angles, best orthogonal error, factor recovery; report degeneracy | Sound | **V**: for whitened codes, squared rotation distance = 2 Σ (1 − cos θᵢ). Principal angles refine the distance rather than adding an independent metric. **V**: the authors' `spectral_solution` silently returns the eigensolver's basis at a tie, so reporting degeneracy improves on their code. | Keep. |
| 5 | L30 | "next useful check: a relation between scenes creates a separated eigenspace" | First half already done | **V**: `test_theory.py` L56–66 and L242–253. **V**: lossy observations are absent from the released constructions. | Keep only the lossy-observation half. |
| 6 | L36 | "Follow the released split and fitting protocol" | Ambiguous | **V**: two released protocols give different expected values. With the rotation fitted on 1,014 validation pairs, good-view R@1 is .248/.260/.230, bad-view .133 and NTP .118 (`ablations.csv` L2–4, L52–53). With the 30k-pair rotation (`--pairs flickr-all`), good-view R@1 is .354/.340/.344 (`scaling.csv` L20–22). | Name the protocol and its expected values. |
| 7 | L40 | Record dataset versions and splits | Missing a leakage check | **V**: the authors ship `python -m prh.data overlap` and `evaluate.py wit --drop` to find benchmark items in the training corpus (`data.py` L506–551). No dropped score appears in `paper/data`. **D**: this matters only once Recap texts are used. | Add the overlap check for any web-text run. |
| 8 | L45 | Record failed or collapsed runs | Undefined | **V**: the authors define collapse as last-epoch R@1 below .05 (`reproduce.md` L116). Collapses occur at λ .005 and .05 without clipping, at λ .1, at lr 1e-3, with 2+2 views and at 30% masking (`ablations.csv`). | Define collapse and preregister how collapsed seeds are handled. |
| 9 | L55–61 | Stage 3 arms | Unfair baselines by omission | **V**: the table has no bad-view JEPA, which is the authors' only control that isolates views. It has no NTP arm, although L85 requires one for claims against NTP. Also missing are a frozen sentence-encoder reference (all-mpnet-base-v2: WIT .118, COCO-5k .156), a random-initialisation floor (`random-bert-s`) and a paired upper bound (CLIP text tower, Flickr R@1 .489 through the 30k rotation). The shared/private baseline is undefined. | Add the arms. See section 4. |
| 10 | L65 | "do not use the test image encoder or test pairs to construct training weights" | Too narrow | **V**: the authors' robustness sweep is scored on test R@1, and one column, best epoch, is test-selected and disclosed as such. L71 covers part of this. The verifiers split. | Extend the rule to checkpoints, collapse rules and layers, and select against a different frozen reference. |
| 11 | L65–67 | Teacher rule and "independently trained" | Hidden supervision not covered | **V**: two of Recap's three texts per image are LLaVA-LLaMA-3 recaptions (`data.py` L50–51). **D**: even with human captions, deciding which captions are views of one another uses the image. "Independently trained" therefore means that no network or gradient sees both modalities. It does not mean the training data are free of pairing information. | See section 4. |
| 12 | L71 | Scene-disjoint splits; freeze layer choices | Partly redundant; deviates from the benchmark | **V**: the Karpathy split is already image-level, and only the first caption of each image is scored (`evaluate.py` L61, L123). **V**: freezing the layer choice departs from the PRH protocol, which takes a maximum over layer pairs. | Report both the protocol score and a fixed-layer score. |
| 13 | L73 | Three seeds, five "when variance is large" | Underpowered | **V**: within-arm seed standard deviations range from .0015 to .0087, pooled .0049 (`scaling.csv`). With 3 seeds per arm, a two-sided t-test at α .05 and power .8 detects only about 3.07 sd: about .015–.020 on WIT and about .046 Flickr R@1. Five seeds detect about 2.02 sd. | State the minimum detectable effect before running. |
| 14 | L73 | Scene-level uncertainty | Partly misdirected | **V**: the headline metrics already use one caption per image. The dependence that matters is benchmark sampling. The authors handle it with 200 subsets of 800 of the 1,024 pairs and paired difference intervals (`metrics.py` L107–130). | Report seed variance and benchmark-sampling variance separately. |
| 15 | L75–83 | Evaluation list | No primary endpoint | **V**: seven metric groups across five or more arms, with no rule for which metric decides. The authors preregistered predictions for 176 runs (`phase_law_predictions.csv`). Most metrics are already implemented: `metrics.alignment`, `prh_score`, `unbiased_cka`, `scene_explained`, `rotation_error`, `prh_subsample`. | Preregister one primary metric per hypothesis. |
| 16 | L79 | Best-rotation error | Incomplete for NTP arms | **V**: next-token cross-entropy has a GL(k) symmetry (`test_theory.py` L122–131). A non-orthogonal map gives rotation distance 2.211 that drops to 1.4e-13 after whitening. The authors report wR@1 and wR@5 for this reason (`metrics.py` L62–63). | Add whitened alignment for every NTP or language-model arm. |
| 17 | L85 | Matched-token and matched-FLOP | No accounting rule | **V**: 8 views each padded to 64 tokens, plus projector and SIGReg, against one causal pass plus a 30,522-way tied softmax. Tokens counted as texts read are not tokens processed. | See section 4. |
| 18 | L89–96 | Decision criteria | Not operational | **D**: "reasonable variability", "failure", "cost accounting" and "useful information" are not quantified. Criterion 6 gates all the others but comes last. | See section 4. |

---

## 4. Exact replacement wording

### README.md

**L9, second sentence.**
> The first priority is to establish a reproducible failure case that the authors' release does not already contain: observations that are many-to-one functions of the scene, with a private factor that persists across one modality's views. Their released failure cases concern unreliable views, namely nuisance-keeping bad views, kernel mismatch and low coverage. Then test whether a minimal intervention improves useful transfer at comparable cost.

**L13.**
> The authors report the following agreement on the WIT-1024 benchmark of Huh et al. (2024) between text representations and frozen DINOv2 ViT-B/14 image representations. The score is mutual 10-nearest-neighbour overlap on 1,024 image–caption pairs, taking the best of all text-layer and image-layer pairs; chance is about 0.01.

**L17.**
> | Their 109M good-view JEPA, mean of three seeds (0.179–0.191) | 0.184 |

**Note below the table.**
> Language-model rows are the authors' own evaluations of frozen pretrained models. A fourth 940M-scale good-view run at twice the effective SIGReg weight scored 0.121; the authors report it separately and exclude it from the mean.

**L21.**
> These are alignment scores, not downstream-task, general-intelligence or reasoning scores, and mutual k-NN agreement on a 1,024-item gallery is known to fall as the gallery grows (Koepke et al., 2026). The sample-efficiency figure compares the good-view JEPA with next-token prediction on the same 109M encoder. The good-view JEPA reaches 0.109 after 21.6M training samples, within the authors' 0.005 tolerance of next-token prediction's 0.111 after 900M samples: about **42 times fewer samples**. Counted as the authors count tokens, as the tokens of the texts each training item draws from, this is about **14 times fewer text tokens**; the good-view JEPA actually encodes eight cropped views per item. The two runs also differ in learning rate, batch size and number of unique images. The authors report no FLOP count. Our estimate from their view settings, not a measurement, is that training compute differs by roughly 7 to 15 times, depending on whether padded view tokens are counted. Sources: paper Fig. 1 and the WIT and language-model tables, which the authors' docs/reproduce.md places in Sec. 4.4–4.5 (section numbers not checked against the paper text); [authors' repository](https://github.com/galilai-group/prh-proof).

**L23.**
> The exact-agreement theorem assumes that each observation is a rendering of exactly one world state, that the encoders are exact population minimisers, and that the positive-pair operator has an eigengap μ_k > μ_{k+1}. In the whitened squared-loss form encoded in the authors' prh/theory.py, the minimiser is always the span of the top-k eigenfunctions, and the gap is exactly what makes it unique up to rotation. The theory also bounds what happens when these assumptions fail. Thm. 2 bounds misalignment by the mismatch between the two modalities' positive-pair kernels divided by the gap. Thm. 3 lower-bounds cross-modal error by the nuisance an encoder keeps. Thm. 4 bounds the effect of arbitrary positives, including a fraction of wrong pairs. The robustness proposals below should be read relative to these bounds.
>
> The authors document three further points. Two of Recap's three texts per image are written by an image captioner, and they measure the effect. Their hyperparameter sweep covers only the good-view recipe, while the controls reuse its learning rate, clipping and batch size. A fourth 940M-scale run at twice the effective SIGReg weight scored 0.121, and the other two headline seeds were rerun at seed 0's effective weight. Whether the paper describes these as limitations has not been checked against its text. Within each text source both arms read the same texts, so the view comparisons remain controlled. At web scale, however, the good-versus-bad gap is large only when alt-text and captioner recaptions are mixed. The human-caption Flickr30k and MSR-VTT comparisons are the cleanest evidence for good views. Sources: paper Sec. 2 (theory) and Sec. 6 (text sources), per the authors' documentation, and the paper's appendix on the SIGReg weight (appendix letter not verified).

**L27–34.**
> Consider a scene containing a red car beside a tree. One caption says "a parked vehicle"; another says "a tree beside the road." They describe the same scene while exposing different facts.
>
> Forcing two representations to agree entirely may discard information present in only one view. Two cases must be kept apart. Information that varies between observations of one scene is a nuisance in the authors' Thm. 3, which proves that an encoder keeping it inside the k aligned dimensions pays at least 2(k − tr C^{1/2}) in cross-modal error. Information that persists across one modality's observations but is invisible to the other belongs to that modality's world state. The authors' constructions never build this case, because every observation determines its state. Reading the shared factor as the state in their Thm. 3–4 predicts that agreement is confined to the intersection of the two modalities' leading eigenspaces and fails when a private factor outranks the shared one at the chosen dimension. The proposed extension would:
>
> 1. Identify the information recoverable from both views. This is proved for paired contrastive training (Daunhawer et al., 2023; Yao et al., 2024) and is open for encoders trained without cross-modal pairs.
> 2. Align only that shared component.
> 3. Preserve information present in only one view outside the aligned dimensions. Shared/unique designs exist for paired training, for example FactorCL, DeCUR and CoMM.
> 4. Estimate, per observation and without paired training, when observations are too ambiguous to support confident alignment. Model-pair-level alignability predictors already exist (Schnaus et al., 2025–2026).

**L36.**
> The theoretical target is a finite-world guarantee about agreement on the shared information when each modality's observation is a many-to-one function of the world state, with explicit dependence on the information each view loses, on the eigenvalue ordering of shared and private factors, and on finite data. Pieces exist. Yao et al. (2024) give population identifiability of latents shared by subsets of views under paired contrastive training. Klindt et al. (2026) give an approximate single-encoder bound. The authors' Thm. 2–4, applied to the kernel that a many-to-one rendering induces on world states, already give gap-dependent bounds, although these are often vacuous. Such a guarantee has not been proved here.

**L42.**
> The following small calculation, an instance of the tie case that Prop. 1's eigengap condition excludes, shows why that condition matters.

**New paragraph after the display at L55.**
> The degeneracy is not specific to scalar encoders. For any embedding dimension k below |Z| − 1, here 3, every centred, whitened k-dimensional encoder has zero loss. Two such encoders are rotations of each other only if they span the same subspace, and these subspaces form a family of dimension k(|Z| − 1 − k). Only at k = |Z| − 1 do all whitened encoders coincide up to rotation. Real encoders have k far below the number of scenes.

**L58.**
> With uniform scenes and same-scene positives only, the positive-pair kernel is diag(p). The normalised operator is therefore the identity, and all four eigenvalues equal 1. The gap μ_k − μ_{k+1} of Prop. 1 is zero for k = 1 and k = 2, so the minimiser is not unique up to rotation. The authors' perturbation bounds are vacuous here, and their code returns infinity for exactly this tie. The example lies outside the gap condition as encoded in the authors' prh/theory.py. **It is not a counterexample to that condition**, and it is not an experiment on the full LeJEPA objective. It does contradict an informal reading of the result in which two observations of the same state suffice without a gap.

**L60.**
> It shows that same-scene positives alone fix nothing across scenes. In the authors' theory, relations between scenes are the off-diagonal mass of the world kernel π(z, z′), and the eigengap of that kernel is the identifiability condition; temporal transitions are one such kernel. The open question is empirical and definitional. When positives are two captions of one image, what supplies the cross-scene relations: near-duplicate captions across images, a coarser notion of state than the image, or the encoder's inductive bias? And is the resulting gap large relative to the mismatch between the two modalities' kernels?

**L68**, to go with the script change below.
> Expected result: each mean is 0, each variance is 1, the kernel loss is 0 for both encodings and for a random centred unit-variance encoding, all eigenvalues of the normalised kernel are 1, and the best orthogonal alignment MSE is 2.

**L76.**
> | Human versus generated captions of the same images, at matched scale | The authors' text-source table already shows a captioner effect: with alt-text plus a text-only paraphrase, good views score 0.058–0.061 against 0.054–0.056 for bad views at 2.24M images, versus 0.095–0.115 with captioner recaptions. What remains open is a matched-image comparison and human captions at scale. |

**L77.**
> | Controlled omission of facts, and corruption of pair identities on real captions | How robust is the method to incomplete or unreliable views, and does degradation follow the authors' Thm. 2 and Thm. 4 bounds? The authors test wrong pairs synthetically and sweep the good-view fraction on real data. A real-data wrong-pair curve and controlled fact deletion would be new. |

**L79.**
> | Causal-attention JEPA, a bidirectional masked-LM baseline, and matched pooling and projector | Which effects come from the attention pattern, the objective, the pooling ([CLS] versus mean), the projector, or the views? The authors already isolate views with the bad-view JEPA and have last-token-pooling and next-token-on-caption-pairs controls. |

**L93.**
> Shared/unique representation learning is established for paired multimodal training, for example FactorCL (Liang et al., NeurIPS 2023), DeCUR (Wang et al., ECCV 2024) and CoMM (Dufumier et al., ICLR 2025). [M3-JEPA (ICML 2025)](https://proceedings.mlr.press/v267/lei25b.html) aligns pretrained encoders on paired data through a mixture-of-experts predictor whose gating it describes as separating modality-specific and shared information. [Yao et al. (ICLR 2024)](https://arxiv.org/abs/2311.04056), generalising Daunhawer et al. (ICLR 2023) and von Kügelgen et al. (NeurIPS 2021), prove that when each view is a nonlinear mixture of a subset of the latents, contrastive learning with one encoder per view identifies the shared latents up to a smooth bijection. [Klindt, LeCun and Balestriero (2026)](https://arxiv.org/abs/2605.26379) prove linear identifiability for a single LeJEPA encoder under Gaussian Ornstein–Uhlenbeck positives and an invertible observation map. In the works checked so far, all train on paired data or on a single modality; we have not found an analysis of independently trained encoders whose observations are many-to-one functions of a shared state, which is not evidence that none exists.

**Additions to the Sources list.**
> - Balestriero and LeCun, *LeJEPA*, arXiv:2511.08544
> - Huh, Cheung, Wang and Isola, *The Platonic Representation Hypothesis*, ICML 2024, arXiv:2405.07987
> - Daunhawer et al., *Identifiability Results for Multimodal Contrastive Learning*, ICLR 2023, arXiv:2303.09166
> - von Kügelgen et al., *Self-Supervised Learning with Data Augmentations Provably Isolates Content from Style*, NeurIPS 2021
> - Liang et al., *Factorized Contrastive Learning*, NeurIPS 2023; Wang et al., *DeCUR*, ECCV 2024; Dufumier et al., *CoMM*, ICLR 2025
> - Koepke et al., arXiv:2604.18572, and Gröger, Wen and Brbić, arXiv:2602.14486, on the limits of the mutual-kNN protocol

### examples/identifiability_sanity_check.py

Replace `same_scene_loss` and the two hard-coded entries with computed quantities:

```python
import random

P = [0.25] * 4
PI = [[P[i] if i == j else 0.0 for j in range(4)] for i in range(4)]   # same-scene positives only


def jepa_loss(encoding, pi=PI):
    """Population squared-loss JEPA objective: sum over pairs of pi(z, z') (h(z) - h(z'))^2."""
    return sum(pi[i][j] * (encoding[i] - encoding[j]) ** 2 for i in range(4) for j in range(4))


def normalized_kernel(pi=PI, p=P):
    return [[pi[i][j] / (p[i] * p[j]) ** 0.5 for j in range(4)] for i in range(4)]


def whitened(values):
    c = mean(values)
    s = variance(values) ** 0.5
    return [(v - c) / s for v in values]

# in main():
S = normalized_kernel()
assert S == [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]   # S is the identity
eigenvalues = [S[i][i] for i in range(4)]       # a diagonal matrix's eigenvalues are its diagonal entries
random_encoding = whitened([random.gauss(0, 1) for _ in range(4)])
result["kernel_losses"] = [jepa_loss(first), jepa_loss(second), jepa_loss(random_encoding)]
result["normalized_scene_kernel_eigenvalues"] = eigenvalues
result["eigengap_after_first_nonconstant_eigenvalue"] = eigenvalues[1] - eigenvalues[2]
assert all(isclose(v, 0.0, abs_tol=1e-12) for v in result["kernel_losses"])   # every whitened encoder is a minimiser
```

Optionally add a contrast case that gives the kernel off-diagonal mass, for example a 2×2 factor kernel. There the two encodings have different losses and only the top eigenfunction is optimal.

### docs/experiment_plan.md

**L20–26.**
> Vary one mechanism at a time. Four of these axes are already implemented in the authors' prh/theory.py and should be reused rather than rebuilt: positive structure, including controlled incorrect links (`class_world`, `random_world`, `mixed_views` with its `move` weight); encoder dimension against the eigengap (`spectral_solution`, `coverage_bound`); nuisance persistence (`bad_views`, Thm. 4's η); and observations per scene (`line_alignment`). The new axis is observability. Every released construction maps each observation to one state, so subset-visible and ambiguous observations need a new construction: an emission matrix O_m[z, x] = P(x | z) per modality, the observation kernel W_m = O_mᵀ π O_m, and comparison by canonical correlations when the two modalities recover different numbers of directions.

**L30.**
> The four-scene example is the tie case of Prop. 1. The authors' tests already show that a world kernel with off-diagonal mass and a gap gives exact agreement. The new check is lossy, many-to-one observations. Build first the world in which a modality-private factor persists across that modality's views and outranks the shared factor at the chosen k. The spectral prediction there is zero agreement on the shared factor, which becomes exact once k reaches the shared factor's rank in both modalities.

**L36.**
> Use the authors' released code and record its exact commit and dependencies; their runs used stable-pretraining at ab836bf, PyTorch 2.11 and bf16. Begin with the 33M BERT-S text configuration and frozen DINOv2 ViT-B/14 features on Flickr30k human captions, with the released Karpathy split. Name the fitting protocol. The primary protocol is `evaluate.py align`, with rotation and whitening fitted on the 1,014 validation pairs and scored on the 1,000 test pairs; the authors' three good-view seeds give R@1 .248, .260 and .230, against bad-view .133 and next-token .118. Report the 30k-pair variant (`--pairs flickr-all`, .354, .340, .344) as secondary.

**Add to the L38–45 record list.**
> - For any run on web texts: the overlap between the training corpus and every evaluation set (`python -m prh.data overlap`), and `evaluate.py wit --drop` scores alongside the undropped scores.
> - Failed or collapsed runs, with collapse defined in advance (the authors use last-epoch Flickr R@1 below .05) and a preregistered rule for how collapsed seeds enter summary statistics.

**Add to the L55–61 table.**
> | Bad-view JEPA, spans of one caption | Isolates views from objective and architecture; the authors' control |
> | Next-token prediction, same encoder | Language-objective control required by Stage 4 |
> | Frozen all-mpnet-base-v2, and random-initialisation BERT-S | External reference and floor |
> | CLIP text tower, paired | Upper bound of paired training; the authors report Flickr R@1 .489 through the 30k rotation |
>
> Define the shared/private baseline as an unpaired design, for example an embedding split into shared and private blocks with SIGReg on each and invariance only on the shared block. Paired designs such as FactorCL or DeCUR belong in the separate supervised setting of L67.

**L65.**
> Avoid circular evaluation. Do not use the test image encoder or test pairs to construct training weights, to select hyperparameters, checkpoints or layers, or to define collapse. Select on validation pairs only, for example with the authors' `align --val-only --split 507`, and where possible against a different frozen reference from the one reported: select on DINOv2-S and report DINOv2-B, -L and -g. If a pretrained text or vision-language teacher supplies overlap scores or wrote the training texts, as Recap's LLaVA recaptions were, disclose that dependency and include it in cost and supervision comparisons. Report oracle, teacher-written-text and human or text-only-paraphrase settings separately.

**L67, append.**
> "Independently trained" means that no network or gradient sees both modalities. The grouping of captions into good views is itself derived from the image and therefore carries paired information; state this wherever results are attributed to independent training.

**L71.**
> Use the released Karpathy split, which is already image-level: each image's five captions stay in one split, and only the first caption of each image is scored. Fit all maps, thresholds and rank selections on training or validation pairs only. The authors' WIT protocol selects the best text-layer and image-layer pair on the 1,024 scored pairs. Report that protocol for comparability, and separately report a fixed-layer score with the layer chosen on a disjoint set.

**L73.**
> State the minimum detectable effect before running. With three seeds per arm, a two-sided test at α = .05 and power .8 detects only about three within-arm standard deviations. From the authors' seed spreads that is about .015–.020 mutual 10-NN on WIT and about .045 Flickr R@1. Use five seeds whenever the expected effect is below these values. Report training-seed variability and benchmark-sampling variability separately; for the latter, use the authors' intervals from 200 subsets of 800 of the 1,024 WIT pairs, with paired differences between arms. Resample at the image level wherever several captions of one image enter a metric.

**After L75, before the list.**
> Preregister one primary metric per hypothesis and treat the rest as secondary, reported without selecting on them:
> - failure: Flickr R@1 or mutual 10-NN against the private-factor or incorrect-pair rate;
> - intervention: whitened R@1 on the shared-factor probe;
> - retention: linear decodability of the private factor, or the authors' scene-explained fraction.

**L79.**
> - Best-rotation error, with fitting and evaluation samples kept separate. For every next-token or language-model arm, also report the error after whitening both sides (the authors' wR@1 and wR@5), since Prop. 3 identifies those embeddings only up to an invertible linear map. Report CKA alongside mutual k-NN.

**L85.**
> Run matched-token, matched-unique-image and matched-FLOP studies separately; they answer different questions. Count FLOPs as forward plus backward over every view, eight for the default recipe, at the padded view length of 64, plus projector and SIGReg, against one causal pass plus the tied softmax head. Report tokens both as texts read, which is the authors' 128.4 against 42.8 per sample, and as view tokens processed. Give every arm the same number of preregistered configurations, selected on validation pairs only. Include attention-mask, pooling and language-objective controls if making claims against next-token prediction.

**L89–96.**
> Continue to larger training only if, in this order:
> 1. A focused related-work review names the contribution and the experiment that would refute it.
> 2. The Flickr good-view baseline is reproduced at the recorded commit within a preregistered tolerance of the authors' three-seed mean (R@1 .246 through the 1,014-pair rotation), with bad-view near .13 and next-token near .12.
> 3. A preregistered failure metric degrades as the private-factor rate, missing-fact rate or incorrect-pair rate increases, by more than the minimum detectable effect.
> 4. The intervention recovers at least half of that degradation across five seeds, at no more than 1.1× the baseline's training FLOPs and with the same tuning budget as the baselines.
> 5. Private-factor decodability does not fall below the baseline's.
> 6. The result holds on a held-out dataset.

---

## 5. Theory interpretation

- **Injectivity.** This is **V** in the code. Thm. 1 renders each state as one observation through an injective g (`theory.py` L96). Thm. 3 makes (state, nuisance) → observation injective, so a state has many observations (L155). Thm. 4 needs only a single-valued `state[x]` (L208–216). The real content is that the state is a function of the observation. Saying "injective observations" is acceptable, but the direction should be explicit. Partial observability of the state is outside every construction. That is the repository's genuine opening.
- **Population optima.** This is **V**. Every statement concerns exact minimisers under exact expectations, and no finite-sample result exists in the code. The repository is right to list this as a gap.
- **Uniqueness up to rotation and the eigengap.** In the released model these are one condition, **V**. Prop. 1 says the whitened squared-loss minimiser is always the top-k eigenspace, unique up to rotation iff μ_k > μ_{k+1}. Thm. 2 and Thm. 4 divide by the gap and return nan or inf at a tie. Whether the paper states Thm. 1 more abstractly, with uniqueness as a hypothesis and the spectral case as a specialization, is **U**. The repository's wording fits that reading, so it is not wrong, just less precise than it could be.
- **Criticisms that overlook what the authors address:**
  1. Robustness to wrong pairs and to nuisance is bounded by Thm. 2–4 and tested synthetically (`mixed_views`, `thm4_tightness`, `coverage_sweep.csv`).
  2. "Relations between scenes" is the kernel π itself.
  3. The tie case is flagged in code, where `coverage_bound` returns inf.
  4. The captioner dependence is measured (`text_sources.csv`).
  5. Human-caption controls exist (Flickr30k, MSR-VTT).
  6. Validation/test separation exists for Flickr.
  7. Whitened alignment for next-token models exists (wR@1).
  8. Four of the plan's five Stage 1 axes are implemented.
- **Criticisms that hold:**
  1. Many-to-one observations are not modelled.
  2. No finite-sample theory exists.
  3. The WIT layer maximum is taken on the scored pairs.
  4. Bad-view and NTP arms reuse the good arm's hyperparameters.
  5. NTP differs from JEPA in attention, pooling and projector at once.
  6. The web-scale good-versus-bad gap depends on captioner text.

---

## 6. The mathematical example, derived and run

**Derivation.** This is **V**, by hand and in `math_independent.py`.

- With p uniform on four scenes and same-scene positives only, π = diag(p).
- The normalised operator is S = D^{-1/2} π D^{-1/2} = I₄, so all eigenvalues equal 1.
- The objective Σ π(z, z′)(h(z) − h(z′))² is 0 for every h.
- Under E h = 0 and E h² = 1, both h1 and h2 are minimisers, and E h1 h2 = 0.
- Hence E(h1 − q h2)² = 2 − 2q·0 = 2 for q = ±1.
- In general, the squared distance after the best orthogonal map is 2k − 2 Σ σᵢ(E h1 h2ᵀ) = 2 Σ (1 − cos θᵢ) over the principal angles.

**Dependence on k.** This is **V**.

| k | Squared rotation distance between two random whitened encoders |
|---|---|
| 1 | anywhere in [0, 2] |
| 2 | up to 2 |
| 3 = \|Z\| − 1 | 2.8e-13 (always a rotation) |

The README omits this condition.

**Relation to the theorem.** This is **V** against the code and **U** against the paper. The example is the gap-zero case of Prop. 1, so Thm. 1's hypothesis fails and the authors' bounds return nan or inf. It is not a counterexample to the theorem as encoded. It is a counterexample to the authors' informal README summary, which mentions no gap.

**Is it a useful research question, or just failure outside the assumptions?** On its own it is failure outside the stated assumptions, and the authors' code already marks the case (**D**). It points to a useful question in one way. If the state of the real-data theory is the image, so that good views are two captions of one image, then π is diagonal over images and the tie is generic at realistic k. Identification must then come from somewhere the population theory does not model: a coarser notion of state, cross-image caption structure, or the encoder's inductive bias. How the paper defines state on real data is **U**.

**Passing assertions are not verification here.** The repository's asserts cannot fail on the spectral claims, because those values are hard-coded and the loss function is a tautology. The independent derivation above confirms the claims. The script does not.

**Partial-observability extension.** This is **V** in `math_independent.py` and `two_coarsenings.py`, and a verifier reproduced it independently with `private_outranks.py` and `part_d.py`.

| World | k | Result |
|---|---|---|
| 2×2 factor world (shape stays with probability .95, colour .6), modality 2 sees shape only | 1 | Agreement with the full modality is exact: distance 0, cosine 1. |
| Same world, modality 2 sees colour only | 1 | Squared distance 2, cosine 0: complete failure although colour is shared information. |
| Three binary factors; A sees f1, f2; B sees f2, f3; private f1 slower than shared f2 | 1 | A encodes f1, B encodes f2: cosine 0, squared distance 2. |
| Same | 2 | Principal cosines [1, 0]: aligned on f2, private on the second dimension. The squared distance of 2 is exactly the authors' Thm. 3 bound when f2 is read as the state. |
| Shared f2 is the slowest factor | 1 | Exact agreement. |
| Shared f2 is the fastest factor | 1 | Both modalities encode their private factor: cosine 0. |
| Coupled, non-product world | 1 | Cosine .77; the reassigned Thm. 3 lower bound of .46 is close to the actual squared distance of .47. |

Conclusion, **D**: alignment is confined to the intersection of the two leading eigenspaces. Its exact population condition is that the shared factor ranks within the top k of both modalities' coarse spectra. The authors' Thm. 3–4, with roles reassigned, give tight lower bounds in these worlds, while Thm. 2 through the lifted kernel is valid but usually vacuous.

---

## 7. Novelty

Everything in this section is at abstract level unless marked otherwise.

| Work | Setting | Overlap with the proposal |
|---|---|---|
| Balestriero and LeCun 2026 (code **V**) | Independently trained JEPAs, finite-world spectral theory | Thm. 1–4: exact agreement under a gap; bounds for kernel mismatch, nuisance and wrong pairs. No many-to-one observations. |
| Klindt, LeCun and Balestriero 2026 (Lean code **V**) | Single LeJEPA encoder, Gaussian OU positives, invertible map | Linear identifiability; uniqueness of the Gaussian; approximate gap bound. Nicollier et al., arXiv 2609.21656, extends this to other latent geometries. |
| Yao et al., ICLR 2024 | Paired contrastive training, views mixing subsets of latents | Block-identifies latents shared by any subset of views, which is direction 1's items 1–2. |
| Daunhawer et al., ICLR 2023; von Kügelgen et al., NeurIPS 2021 | Paired multimodal or augmented views | Shared content identifiable; modality-specific latents discarded. |
| FactorCL (NeurIPS 2023), DeCUR (ECCV 2024), CoMM (ICLR 2025), Wang et al. (CVPR 2022) | Paired multimodal self-supervised learning | Shared/unique representation designs, which is direction 1's item 3. |
| M3-JEPA, ICML 2025 (code **V**) | Pretrained, paired encoders with a mixture-of-experts predictor | Gating described as separating modality-specific and shared information. Not a representation split, and not independently trained. |
| HaoChen et al. 2021; Johnson et al. 2023; Zhou et al., ICLR 2024 | Spectral contrastive learning | Eigenfunction view of positive-pair graphs; mitigation of wrong edges. |
| Tosh, Krishnamurthy and Hsu 2021 | Multi-view redundancy | When views share the information relevant to a task. |
| Schnaus et al. 2025–2026; vec2vec (2025) | Pair-free alignment of independent models | Alignability predictors at the level of model pairs. |
| Huh et al. 2024; Koepke et al. 2026; Gröger et al. 2026 | Platonic Representation Hypothesis measurement | The benchmark and its known limits. |

**What could be new.** These are **D**, conditional on the full texts above, which were not read.

1. **A finite-world statement** for independently trained spectral JEPAs with many-to-one renderings: agreement equals the intersection of leading eigenspaces, under an exact eigenvalue-ordering condition, with tight bounds. This is close to a corollary of the authors' Thm. 3–4 under relabelling. Its value would be the explicit condition and the counting argument, so it would be a modest result.
2. **An empirical test** of whether trained LeJEPAs with SIGReg, finite data and nonlinear capacity follow this spectral prediction on real captions. This is the most informative unknown.
3. **A pair-free, per-observation estimator** of which embedding directions are shared.
4. **Real-data wrong-pair and fact-deletion curves** compared with the Thm. 4 bound.

No search result is offered as evidence of absence. The novelty checker ran 27 queries and I ran further ones; neither establishes that the gap is real.

---

## 8. Experiment plan audit

| Risk | Finding | Severity |
|---|---|---|
| Leakage | The Flickr split is already image-level, which is fine. Web-text runs need the authors' overlap and `--drop` check. | Medium, only once Recap is used |
| Circular evaluation | The WIT protocol selects layers on the scored pairs. The authors' sweep is scored on test R@1. The plan's rule covers only training weights. | Medium |
| Unfair baselines | No bad-view or NTP arm in Stage 3. The shared/private baseline is undefined. Tuning budgets are not operationalised. Rotation-only alignment under-measures NTP. | High |
| Hidden teacher supervision | Captioner-written texts are not covered by the teacher rule. The grouping of captions by image is itself paired information. | Medium |
| Compute mismatch | No FLOP rule. Tokens counted as texts read are not tokens processed. The unique-image count also changes. | Medium |
| Statistics | Three seeds detect only about 3 sd. No primary endpoint. No multiple-comparison control. Collapse is undefined. Seed and benchmark-sampling variance are not separated. | High |
| Do the experiments test the hypotheses? | Not yet. Stage 1 never builds the case where a private factor outranks the shared one, which is where the hypothesis bites. Stage 3 on Flickr has no private persistent factor. The decision criteria are not falsifiable as written. | High |

---

## 9. Strongest research direction and the smallest falsifying experiment

**Direction.** Study cross-modal alignment of independently trained JEPAs when each modality observes a many-to-one function of the world state, and one modality has a private factor that persists across its own good views. This is the one axis the authors' constructions do not build. The population-level answer is already computable: agreement is confined to the intersection of the leading eigenspaces (section 6). That makes the question concrete and falsifiable: do trained LeJEPAs follow this spectral prediction?

**Hypothesis H.** A text-private factor that persists across a caption's good views, but is invisible to the image encoder, displaces shared directions from the aligned subspace according to its spectral rank. Cross-modal alignment therefore drops sharply once the number of persistent private directions approaches the embedding dimension, even though all shared information is still present. The prediction has two parts: a small drop while M − 1 is well below k, and a collapse toward chance once M − 1 exceeds k, where M is the number of code values and k the embedding dimension.

**Smallest falsifying experiment.** It needs about 12 runs of roughly 1 GPU-hour each on the authors' hardware; DGX Spark throughput has not been measured.

1. **Setup.** Use the authors' Flickr30k quick start: `train.py --modality text --caption-views`, BERT-S, frozen DINOv2 ViT-B/14, and `evaluate.py align` with the rotation fitted on the 1,014 validation pairs and R@1 among the 1,000 test captions.
2. **Intervention.** For every image, train and test alike, draw a code c uniformly from M values, each mapped to one rare wordpiece token. Insert that image's token into all five of its captions, interleaved every two words so that local crops of 15–50% of the caption keep it. Measure the realised persistence, the fraction of view pairs that both contain the token, and report it.
3. **Arms.** M ∈ {1, 64, 1024, 4096}, three seeds each. M = 1 is a control with the same interleaving using one constant token, so the arms differ only in information, not in format. The comparison points are the backbone width of 384 and the projector output of 512.
4. **Preregistered primary endpoint.** Test R@1 through the validation-fitted rotation. Secondary endpoints: wR@1, mutual 10-NN, and retention, measured as the accuracy of a linear probe that decodes c from frozen text embeddings of held-out images.
5. **Falsification.**
   - H is falsified if R@1 at M = 4096 stays within the minimum detectable effect of the M = 1 control (about .046 R@1 for three seeds) while c is decodable well above chance. A trained LeJEPA would then accommodate persistent private factors without displacing shared ones at realistic dimension. Direction 1's premise would fail in this regime, and an overlap-aware method would have nothing to fix, which is plan decision criterion 2.
   - If R@1 drops but c is not decodable, the mechanism is noise rather than displacement, and H is also not supported.
6. **Confirmatory follow-up, only if H survives.** Repeat at M = 256 with projector widths 128 and 512. H predicts that the drop threshold moves with k.

Before any GPU run, the same sweep can be computed in a finite world with an M-valued private code, using the scripts in this folder's `scripts` directory. That computation gives the population prediction to compare against, but it cannot falsify H for trained networks.
