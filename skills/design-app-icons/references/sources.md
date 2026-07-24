# Sources and claim boundaries

Last checked: 2026-07-24. The repository release ledger is maintained at `docs/source-manifest.yaml`; the installed skill retains the primary URLs below. The scheduled workflow checks availability but cannot prove that page content or platform behavior is unchanged.

## Primary Apple sources

- [Human Interface Guidelines — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons/) — design principles, masks, platform matrix, color spaces, and 2026 change log.
- [Creating your app icon using Icon Composer](https://developer.apple.com/documentation/xcode/creating-your-app-icon-using-icon-composer) — preparation, import, four-group limit, appearances, material controls, Xcode integration, and earlier-release behavior.
- [Icon Composer](https://developer.apple.com/icon-composer/) — current tool capabilities, including refraction and updated specular highlights.
- [Apple Design Resources](https://developer.apple.com/design/resources/) — current app-icon templates and grids. Link to these; do not redistribute Apple templates.
- [Configuring your app icon using an asset catalog](https://developer.apple.com/documentation/xcode/configuring-your-app-icon/) — asset-catalog sizes, dark/tinted variants, tvOS/visionOS stacks, and App Store icon wells.
- [Configuring your app to use alternate app icons](https://developer.apple.com/documentation/xcode/configuring-your-app-to-use-alternate-app-icons) — alternate `.icon` files and Xcode configuration.
- [WWDC25: Say hello to the new look of app icons](https://developer.apple.com/videos/play/wwdc2025/220/) — design-system intent and appearance overview.
- [WWDC25: Create icons with Icon Composer](https://developer.apple.com/videos/play/wwdc2025/361/) — authoring walkthrough.
- [WWDC26 Design guide](https://developer.apple.com/wwdc26/guides/design/) — 2026 Icon Composer positioning.
- [App Store Connect — Product Page Optimization overview](https://developer.apple.com/help/app-store-connect/create-product-page-optimization-tests/overview-of-product-page-optimization/) — eligibility, treatment count, and platform constraints.
- [Configure test treatments](https://developer.apple.com/help/app-store-connect/create-product-page-optimization-tests/configure-test-treatments/) — icon-in-binary requirement.
- [Product Page Optimization analytics](https://developer.apple.com/help/app-store-connect-analytics/acquisition/product-page-optimization) — analytics availability and confidence model.
- [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) — metadata consistency and third-party icon/brand restrictions.

## Secondary inspiration

- [MobileAction: Apple Liquid Glass design in iOS 26](https://www.mobileaction.co/blog/apple-liquid-glass-design/) — useful workflow and ASO hypotheses; not authoritative for Xcode formats, current 2026 platform behavior, safe-zone percentages, review outcomes, ranking effects, or test duration.
- User-supplied icon reference set — used to derive broad visual families only. The source images are not bundled or redistributed.

## Corrections retained in this skill

The secondary article and supplied text contained claims that must not be repeated as current Apple facts:

- Icon Composer creates `.icon`, not `.iconset`, `.icns`, or a renamed asset folder.
- Current Apple Design Resources list iOS 27/iPadOS 27 templates; always use the latest grid rather than freezing an iOS 26 template.
- The current HIG gives exact platform sizes but does not prescribe a universal “central 70%” safe zone.
- Icon Composer exposes Default, Dark, and Mono authoring modes; Clear/Tinted light/dark are Mono preview options.
- Apple documents up to four Icon Composer groups.
- Apple does not guarantee App Review approval for following a checklist.
- Apple does not prescribe a universal 14-day Product Page Optimization test.
- A style refresh does not prove higher ranking, tap-through, or conversion.
