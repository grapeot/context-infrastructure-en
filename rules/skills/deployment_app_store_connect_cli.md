# Release to App Store Connect with Apple Command-Line Tools

## Metadata

- **Type**: Deployment
- **Applicable Scenarios**: Archive, export, and upload an iOS app to App Store Connect from the command line with a non-beta Xcode release
- **Output**: An auditable `.xcarchive`, App Store `.ipa`, upload result, and final version metadata
- **Created**: 2026-07-31

## Goal and Boundaries

Use only tools shipped by Apple to turn a releasable shared Xcode scheme into a build accepted by App Store Connect. Adapt flags to the project, but preserve an evidence chain across source revision, build configuration, signing identity, artifact metadata, and remote delivery state.

This skill does not add a custom CLI, manage screenshots or store copy, change pricing, submit for review, or treat a successful upload as an App Store release.

- Local inspection, build, test, archive, and IPA export with `destination=export` are safe preparation steps.
- `destination=upload` and `altool --upload-*` create a remote build. Obtain explicit authorization before using them.
- Do not enroll external TestFlight testers, submit App Review, or change store metadata without separate authorization.
- Never place Apple ID passwords, app-specific passwords, API private keys, issuer IDs, team IDs, or provisioning-profile UUIDs in source control, logs, or this skill.

## Acceptance Criteria

- `DEVELOPER_DIR` explicitly selects the intended stable Xcode and the recorded `xcodebuild -version` matches it.
- The target is a shared scheme whose Release configuration builds for `generic/platform=iOS`; repository-required builds and tests pass.
- The `.xcarchive` succeeds and its bundle identifier, marketing version, build number, signing team, and minimum OS version match the release intent.
- An export with `method=app-store-connect` succeeds. Its summary reports Apple Distribution or Cloud Managed Apple Distribution, a valid App Store provisioning profile, and `get-task-allow=false`.
- The final IPA is inspected for `CFBundleShortVersionString`, `CFBundleVersion`, and `MinimumOSVersion`; project settings alone are not accepted as evidence.
- The upload command reports `Upload succeeded` or an equivalent accepted state, and App Store Connect begins processing the package.
- If the task requires a processed TestFlight-selectable build, processing must also complete. `Uploaded package is processing` is not completion.

## Apple-Provided Tools

- `xcode-select`: inspect or switch the active developer directory.
- `xcodebuild`: list schemes, build, test, archive, export, and upload.
- `xcrun altool`: validate, upload, and query status with an App Store Connect API key or app-specific password.
- `codesign`, `plutil`, and `unzip`: verify signatures and final IPA metadata.

## Release Method

### Pin Stable Xcode

```bash
export DEVELOPER_DIR="/Applications/Xcode.app/Contents/Developer"
xcode-select -p
xcodebuild -version
```

Use the actual path if stable Xcode is installed elsewhere. When `Xcode-beta.app` is also present, do not rely on an ambiguous global selection and do not delete the beta installation merely to make the release command work.

### Inspect the Project and Signing Context

```bash
xcodebuild -project <App.xcodeproj> -list
xcodebuild \
  -project <App.xcodeproj> \
  -scheme <SharedScheme> \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  -showBuildSettings
security find-identity -v -p codesigning
```

Check at least `PRODUCT_BUNDLE_IDENTIFIER`, `MARKETING_VERSION`, `CURRENT_PROJECT_VERSION`, `IPHONEOS_DEPLOYMENT_TARGET`, `DEVELOPMENT_TEAM`, and `CODE_SIGN_STYLE`. Automatic Signing can use Cloud Managed Apple Distribution during export, so the absence of a locally visible Apple Distribution identity does not prove that export is impossible. Let a non-uploading export decide.

### Archive

```bash
xcodebuild archive \
  -project <App.xcodeproj> \
  -scheme <SharedScheme> \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  -archivePath <output/App.xcarchive> \
  CODE_SIGN_STYLE=Automatic \
  DEVELOPMENT_TEAM=<TEAM_ID>
```

Use a new output path for retries, or remove an old archive only after confirming it is no longer needed for audit or rollback.

### Export for the App Store

Create a temporary `ExportOptions.plist`. Do not commit it to a public repository:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>destination</key><string>export</string>
  <key>method</key><string>app-store-connect</string>
  <key>signingStyle</key><string>automatic</string>
  <key>teamID</key><string>TEAM_ID</string>
  <key>uploadSymbols</key><true/>
</dict>
</plist>
```

```bash
xcodebuild -exportArchive \
  -archivePath <output/App.xcarchive> \
  -exportPath <output/export> \
  -exportOptionsPlist <output/ExportOptions.plist>
```

Xcode may use `manageAppVersionAndBuildNumber` to replace the source build number with the next value accepted by App Store Connect. Treat `DistributionSummary.plist` and the exported IPA as authoritative, and record any difference between source and upload build numbers. If source-controlled versioning is required, disable managed versioning explicitly and increment the project build number before archiving.

### Verify the Final IPA

```bash
unzip -p <App.ipa> Payload/<AppName>.app/Info.plist \
  | plutil -extract CFBundleShortVersionString raw -
unzip -p <App.ipa> Payload/<AppName>.app/Info.plist \
  | plutil -extract CFBundleVersion raw -
unzip -p <App.ipa> Payload/<AppName>.app/Info.plist \
  | plutil -extract MinimumOSVersion raw -
```

Also inspect `DistributionSummary.plist`. If any metadata differs from the release intent, correct the project and repeat build, test, archive, and export. Do not upload the wrong artifact.

### Upload

After explicit authorization, change the export option `destination` to `upload` and run:

```bash
xcodebuild -exportArchive \
  -archivePath <output/App.xcarchive> \
  -exportPath <output/upload> \
  -exportOptionsPlist <output/UploadOptions.plist>
```

With a dedicated App Store Connect API key, Apple's `altool` is another supported path:

```bash
xcrun altool --validate-app -f <App.ipa> \
  --api-key <KEY_ID> --api-issuer <ISSUER_ID>
xcrun altool --upload-app -f <App.ipa> \
  --api-key <KEY_ID> --api-issuer <ISSUER_ID>
```

Keep the private key in an Apple-supported private-key search directory or inject it from a controlled environment. Never place `.p8` contents in shell history.

## Known Pitfalls

### A New Project Defaults to the Latest OS

Xcode may set `IPHONEOS_DEPLOYMENT_TARGET` to the newest installed SDK even when the product supports older releases. Archive still succeeds, but device coverage shrinks silently. Verify both project settings and the IPA's `MinimumOSVersion`.

### Archive Success Does Not Mean Upload Readiness

An archive commonly uses an Apple Development identity. App Store export performs the Apple Distribution or Cloud Managed Apple Distribution re-signing and binds the App Store provisioning profile. Export validation is a separate required gate.

### No Local Distribution Certificate Does Not Necessarily Block Export

Automatic Signing can use the Xcode account session and a cloud-managed certificate. Do not stop solely because `security find-identity` omits Apple Distribution; try a non-uploading `destination=export` first.

### The Source and IPA Build Numbers Can Differ

Managed versioning may query App Store Connect and select the next build number during export. Release records and retries must read the final IPA instead of guessing from `CURRENT_PROJECT_VERSION`.

### Upload Success Is Not Processing Success

`Upload succeeded` means Apple accepted the package. Report it as “uploaded and processing.” If the endpoint is a TestFlight-selectable build, wait for processing to finish and report any later rejection.

## Output Specification

The final report must include the Xcode path and version; source revision or worktree state; scheme, configuration, and destination; bundle identifier, marketing version, final build number, and minimum iOS version; archive and IPA paths; distribution certificate and profile types without private identifiers; status for build, test, archive, export, upload, and processing; and any intentionally unperformed TestFlight or App Review actions.
