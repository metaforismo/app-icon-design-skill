# Mood Lantern

![Mood Lantern concept](concept-master.png)

This concept is intentionally documented as a whole-image example. Its shared glow and body shading make it a poor candidate for automatic layer separation.

## Brief

- Fictional product: emotion journal
- Promise: notice and reflect on feelings
- Direction: expressive mascot
- Recognition anchor: lantern body with one warm core

## Why it works

The silhouette communicates “lantern” without a second prop. Large eyes and a small mouth establish calm curiosity, and the core glow ties the character to reflection and inner state.

## Risks

- The face can drift toward generic emoji grammar.
- The handle, cap, rings, eyes, mouth, body, and light create too many literal parts.
- The warm light occupies a large area and can erase the body in clear or tinted appearances.
- The body’s shading is too continuous to import as editable vector layers.

## Production decision

For a concept-only request, keep the whole image as the authoritative artwork. Its warm core, shell, face, and reflected light form one integrated rendering.

For a shipping iOS icon, do not send this bitmap directly into layer production. Create a simpler frontal, vector-native `Composer-adapted production concept`, preserve the lantern silhouette and warm-core anchor, and return to the approval gate. Do not claim that an automatically separated proof preserves this image.

A faithful Composer-oriented reinterpretation could use four groups only after re-approval:

1. background fill in Icon Composer
2. unified lantern silhouette including handle and base
3. face as a single opaque group
4. core window as a restrained translucent group

Removing a ring, reducing eye highlights, flattening the face, or shrinking the core changes the design. Treat that work as a new concept, not a mechanical reconstruction.

## Status

- **Validated:** original concept dimensions and static image inspection.
- **Prepared:** whole-image concept, reproducible prompt, and a proposed four-group adaptation plan requiring visual approval.
- **Not tested:** Icon Composer import, Xcode, Simulator, device, App Store, or conversion.
