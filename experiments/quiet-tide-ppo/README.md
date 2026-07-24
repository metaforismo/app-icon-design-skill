# Quiet Tide Product Page Optimization plan

This is a prepared experiment design, not a completed App Store test. It keeps the product promise stable and varies one identity hypothesis at a time.

## Hypothesis

For people encountering a calm-focus app for the first time, a simplified wave-and-sun symbol will communicate the product category more quickly than a more abstract glass composition.

## Variants

| Variant | Controlled change | Rationale |
| --- | --- | --- |
| A — reconstructed identity | Current SVG/Composer wave embracing a sun | Baseline production direction |
| B — flatter utility signal | Same silhouette with no depth and higher value contrast | Tests whether immediate legibility matters more than material richness |
| C — warmer emotional signal | Same silhouette and geometry; warmer sun and softer backdrop | Tests emotional warmth without changing the metaphor |

Do not compare unrelated levels of craft. All variants must be exported and reviewed at equivalent quality and included in the submitted binary when App Store Connect requires alternate icons.

## Decision record

- Primary outcome: App Store conversion rate for the test treatment.
- Guardrails: sufficient impressions, a stable test window, no simultaneous metadata or pricing change, and no interpretation before App Store Connect reports enough evidence.
- Falsifier: if the clearer/warmer variant does not outperform the baseline with meaningful evidence, retain the baseline and record the negative result.
- Stop condition: use App Store Connect’s experiment controls and product owner decision; do not invent a universal sample threshold.

Use [experiment.yaml](experiment.yaml) to record the configuration and [result-template.md](result-template.md) after the test.

## Status

- **Prepared:** hypothesis, controls, decision fields, and result template.
- **Not tested:** alternate icon binary inclusion, App Store submission, live traffic, statistics, or conversion lift.
