# App Store icon experimentation

Current-source snapshot: 2026-07-23.

## What Apple currently supports

Product Page Optimization can test up to three treatments for an iOS or iPadOS product page. Treatments may change app icons, screenshots, and previews.

Important current constraints:

- The app must be Ready for Distribution.
- Treatments appear on iOS 15 and iPadOS 15 or later.
- Product Page Optimization is not available for custom product pages or Apple Watch/iMessage product pages.
- Alternate icon assets used by a treatment must be included in the current app binary and configured through the supported Xcode workflow.
- App Analytics starts showing the test after at least five first-time downloads are attributed.
- Apple uses statistical analysis and may mark a treatment Performing Better or Performing Worse at 90% confidence.
- Applying a treatment ends the running test.

Re-check App Store Connect Help before execution.

## Design a useful hypothesis

Test one meaningful variable:

- metaphor: literal utility versus abstract identity
- emotional signal: calm versus energetic
- silhouette: emblem versus character
- contrast strategy: dark field versus light field

Do not call three hue changes three product hypotheses.

Keep constant:

- product-page screenshots and previews when the icon is the variable
- production quality
- semantic promise
- localization scope
- release behavior when possible

## Prepare alternate icons

1. Create each alternate icon through the current Icon Composer or asset-catalog workflow.
2. Add each source to the Xcode project.
3. Configure alternate app icon sets so Xcode emits the correct `CFBundleIcons` entries.
4. Build and verify every icon locally.
5. Upload a build containing all treatment icons.
6. Configure treatments in App Store Connect.

Do not submit a bitmap in App Store Connect that is absent from the binary when Apple requires it there.

## Read results honestly

Record:

- control and treatment definitions
- traffic allocation
- localization
- start/end date
- impressions and first-time downloads
- estimated conversion rate and lift
- confidence or inconclusive status
- concurrent release or metadata changes

Do not stop early because a graph looks favorable. Apple recommends waiting until a treatment is declared better or worse with at least 90% confidence before applying it. Do not invent a universal 14-day minimum.

The icon can influence attention and expectation, but do not claim that Liquid Glass, a palette, or a stylistic refresh directly improves ranking without measured evidence.

