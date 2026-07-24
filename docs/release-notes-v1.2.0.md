# App Icon Studio v1.2.0

Version 1.2.0 makes the workflow simpler and more faithful to the image the user approved.

## What changed

- A finished 1024 × 1024 image plus static QA is now the default final deliverable.
- Layers, Icon Composer, and Xcode changes are optional post-approval routes, not automatic steps.
- The skill selects the least complex route that satisfies the request.
- Every optional decomposition must match the approved image at full size and 32 px.
- Integrated lighting, glow, painterly material, glass, fur, and shared reflections default to a flattened image.
- Mood Lantern now serves as an explicit failure case: technically valid alpha layers can still produce a visually inferior icon.
- The repository social preview now shows one complete finished icon rather than an exploded construction diagram.

## Evidence boundary

The new workflow and static validators are directly tested. Existing Quiet Tide Icon Composer, Xcode, and Simulator evidence remains valid for that case study. Mood Lantern’s separated proof remains rejected and has not been imported into Icon Composer, Xcode, Simulator, a physical device, or App Store review.
