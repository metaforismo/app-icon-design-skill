# App-icon visual language and originality

## Contents

- [Reference-set taxonomy](#reference-set-taxonomy)
- [What transfers across styles](#what-transfers-across-styles)
- [Direction scorecard](#direction-scorecard)
- [Category collision map](#category-collision-map)
- [Originality safeguards](#originality-safeguards)
- [Common failure modes](#common-failure-modes)

## Reference-set taxonomy

A broad reference set commonly contains these families:

| Family | Strength | Risk | Layer strategy |
| --- | --- | --- | --- |
| Tactile object metaphor | Immediate utility and emotional familiarity | Too much micro-detail or nostalgia | backdrop, object body, key control/accent |
| Minimal geometric mark | Durable recognition and tint resilience | Generic stock-logo collision | backdrop, main mass, negative-space/accent |
| Expressive mascot | Warmth, memorability, community identity | Juvenile tone or emoji similarity | backdrop, body, face, optional accent |
| Layered translucent form | Native material presence and depth | Glow-first concept with weak silhouette | backdrop, 1-2 material groups, opaque anchor |
| Flat emblem or monogram | Strong small-size performance | Letter dependence and localization issues | backdrop, emblem |
| Dark chrome or metal | Premium technical signal | Low contrast and trend dependence | dark backdrop, metal symbol, restrained highlight |
| Functional UI/object miniature | Communicates workflow quickly | Forbidden UI screenshot or illegible controls | reduce to one object and one action cue |
| Character ensemble | Rich personality | Multiple competing focal points | simplify to one group silhouette |

Use the taxonomy to diversify concepts. Do not combine every family in one icon.

## What transfers across styles

The most reliable properties are:

- one dominant silhouette
- a focal hierarchy visible before surface detail
- meaningful negative space
- controlled edge complexity
- optical rather than purely mathematical centering
- a palette that distinguishes the mark from its background
- an identity anchor that survives monochrome treatment
- a structure that can be redrawn intentionally

Depth, glass, gloss, grain, metal, and glow are treatments. They cannot rescue an ambiguous symbol.

## Direction scorecard

Score 0-2 for each:

| Criterion | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Product fit | unrelated | category-adjacent | specific to promise |
| 32px recognition | unclear | partly readable | immediate |
| Ownability | generic/colliding | some distinct detail | distinctive silhouette |
| Appearance resilience | depends on one palette/effect | needs adjustments | anchor survives mono/dark |
| Layer feasibility | inseparable/noisy | requires cleanup | <=4 intentional groups |
| Cross-mask resilience | clipped/off-center | needs platform override | works in rounded and circular grids |
| Brand longevity | trend-only | balanced | durable with optional treatment |

Use the score as a discussion aid, not an automatic winner. A slightly lower-scoring direction may fit the brand better.

## Category collision map

Before generation, inspect current category neighbors when web research is allowed. Record patterns without downloading or redistributing third-party art:

| Neighbor | Metaphor | Silhouette | Dominant palette | Composition | Collision to avoid |
| --- | --- | --- | --- | --- | --- |

Then state the three most crowded metaphors, the common color and silhouette families, one underused territory that still fits the product, and the proposed recognition anchor. Compare candidates in monochrome: a palette change does not resolve a structural collision.

Treat generic sparkles, folded ribbons, infinity loops, chat bubbles, gradient stars, and orbit marks as high-risk in AI or creative-tool categories unless the design adds an ownable structural idea.

## Originality safeguards

- Search category neighbors when the user authorizes web research.
- Compare silhouettes in monochrome, not only full-color renders.
- Avoid reproducing another app’s distinctive negative space, character face, color arrangement, or object composition.
- Do not use another developer’s icon, product name, or brand without approval.
- Do not reproduce Apple hardware in the icon.
- Treat Apple Design Resources as licensed production aids; do not republish templates in the skill repository.
- Record which user-owned elements must remain.
- If a generated mark resembles a known logo, discard or materially redesign it.

## Common failure modes

- App name or instruction text inside the icon
- A screenshot miniaturized into the tile
- An outer rounded-square tile floating on a second background
- Borders aligned to the system mask
- Too many independent symbols
- Thin orbital lines, tiny sparkles, and fake labels
- Reflection and blur stronger than the recognition anchor
- Near-black watchOS background blending into the display
- Different silhouettes for every appearance
- “A/B variants” that only change hue and test no meaningful hypothesis
