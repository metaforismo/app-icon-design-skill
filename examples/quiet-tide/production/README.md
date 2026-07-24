# Quiet Tide production reconstruction

This directory turns the image-generated concept into intentional, editable geometry and a real Icon Composer document.

## Artifacts

- `QuietTide.icon/` — document saved by Apple Icon Composer 1.6; three SVG layers in one group
- `../layers/` — editable, unmasked 1024 × 1024 SVG sources
- `fixture/` — minimal SwiftUI application and XcodeGen specification that compiles the `.icon`
- `evidence/` — Composer appearance captures and iOS Simulator observations

The `QuietTideFixture.xcodeproj` file is generated locally and intentionally ignored. Recreate it with:

```bash
cd fixture
xcodegen generate --spec project.yml
xcodebuild -quiet \
  -project QuietTideFixture.xcodeproj \
  -scheme QuietTideFixture \
  -sdk iphonesimulator \
  -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath ../../../../../work/quiet-tide-derived \
  CODE_SIGNING_ALLOWED=NO build
```

## Design delta from the concept master

The reconstruction deliberately removes the generated bitmap's irregular shading and turns the mark into three stable shapes. The wave uses a single even-odd path, the sun is a true circle, and the backdrop is a full-canvas gradient with no baked platform mask. Icon Composer owns glass, shadow, translucency, and appearance rendering.

## Status

- **Validated:** source SVGs import; `QuietTide.icon` is saved by Icon Composer; Default, Dark, Mono, and watchOS circular previews were observed; the fixture compiles with Xcode; the app installs and launches; the icon appears on an iOS 26.5 Simulator Home Screen.
- **Prepared:** editable SVGs, `.icon`, XcodeGen fixture, appearance captures, and Simulator screenshots are versioned.
- **Not tested:** physical iPhone, iPad, Mac, Apple Watch, earlier OS fallback appearance, signed archive, App Store upload/review, Product Page Optimization, or conversion.

See [evidence.md](evidence.md) for versions and commands.
