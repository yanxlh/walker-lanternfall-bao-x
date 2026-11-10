# Reported A color-ramp r2 CPU result

### A color-ramp r2: reported headless CPU rerun — 9 November 2026

The following figures are transcribed from the two supplied screenshots. Units are ms/frame; parentheses show the range of trial means.

| Condition | Off mean (trial range) | On mean (trial range) | Delta | CPU budget |
|---|---:|---:|---:|---:|
| Empty-scene control | 0.0089 (0.0086–0.0093) | — | — | — |
| Idle game | 0.0581 (0.0578–0.0584) | 0.0620 (0.0618–0.0622) | +0.0039 | — |
| A r2, 32 live bursts | 0.1641 (0.1631–0.1649) | 0.2112 (0.2099–0.2157) | +0.0471 | 1.0 |
| B, continuous movement | 0.0582 (0.0580–0.0586) | 0.0650 (0.0646–0.0658) | +0.0068 | 0.25 |
| Celebration, 4 live bursts | 0.0901 (0.0851–0.0912) | 0.1065 (0.1035–0.1095) | +0.0164 | 0.4 |

All three effect CPU deltas are below budget. The supplied report states that A reached its 32-burst cap, B emitted through each 300-frame trial, and the celebration reached its four-burst cap. A's on-trial means span 0.0058 ms (approximately 0.006 ms) across five trials. The empty-scene control is below every game condition.

For comparison, A's earlier CPU deltas were +0.0222 ms in the October 29 r1 comparison and +0.0379 ms in the November 9 r1 rerun; the r2 result is +0.0471 ms. These separate runs do not isolate the color-ramp change from machine load or other timing variation, so their difference is not established as the cost of r2.

Evidence scope: the screenshots are saved in `evidence/assignment-6/cost/a-color-r2-reported-20261109/`. They report that the raw run remained in a temporary copy; raw logs, per-trial JSON, exact invocation, and source hash were not supplied with these images. This is a reported result with screenshot evidence, not a newly reproduced benchmark or a claim that its raw logs are archived. A r2 GPU timing has not been rerun. All existing A GPU figures remain r1 measurements; the expectation of similar GPU cost after a color-only change remains a prediction.


Screenshots: `cpu-results.png` and `cpu-comparison-and-limits.png`.
