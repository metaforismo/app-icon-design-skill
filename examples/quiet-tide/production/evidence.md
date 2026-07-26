# Quiet Tide evidence ledger

Validation date: 2026-07-24

Build revalidation: 2026-07-26

## Environment

- macOS host with Xcode 26.6 (build 17F113)
- Apple Icon Composer 1.6 (build 99.1), bundled with Xcode
- iPhone Simulator runtime: iOS 26.5
- device: `AgentKeys-Screenshots`
- fixture bundle identifier: `design.appiconskill.quiettidefixture`

## Directly observed

1. Imported `01-backdrop.svg`, `02-sun.svg`, and `03-wave.svg` into Icon Composer.
2. Reordered the full-canvas backdrop behind the identity mark.
3. Disabled glass effects on the backdrop and kept material rendering on the wave and sun.
4. Saved the document as `QuietTide.icon`; its package contains `icon.json` and the three SVG assets.
5. Observed Default, Dark, Mono, and watchOS circular previews in Icon Composer.
6. Generated the fixture project with XcodeGen.
7. Compiled the `.icon` through `actool` in a successful Xcode simulator build with exit code 0.
8. Installed and launched the fixture, returned to the Home Screen, and observed the compiled Quiet Tide icon.

On 2026-07-26, the existing `.icon` was recompiled successfully with Xcode 26.6 (17F113) for the generic iOS Simulator destination. An initial sandboxed run could not access CoreSimulator services and caused `actool` to fail opening the icon; the scoped non-sandboxed rerun completed with exit code 0. No new Simulator screenshot or physical-device observation was made during this revalidation.

## Evidence files

- `evidence/composer-default.png`
- `evidence/composer-dark.png`
- `evidence/composer-mono.png`
- `evidence/composer-watchos-default.png`
- `evidence/simulator-app.png`
- `evidence/simulator-home.png`

The Home Screen evidence is tightly cropped to avoid redistributing unrelated installed-app artwork.

## Boundaries

The Composer captures validate the named preview modes on this tool version; they do not prove rendering on physical displays or motion response. The Simulator capture validates the compiled icon in one runtime and wallpaper context. No physical device, signed archive, App Store, review, experiment, ranking, or conversion outcome was tested.
