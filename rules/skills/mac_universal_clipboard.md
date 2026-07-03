# Mac Universal Clipboard Reset Skill

## Purpose

Use this skill when the user says Universal Clipboard, Handoff clipboard, or copy/paste syncing between Mac and iPhone/iPad is broken. The typical pattern is that iPhone and iPad still sync with each other, while anything involving the Mac fails. On macOS beta builds, this often means the Mac-side Continuity daemons are alive but holding stale state.

## Triggers

Trigger on phrases such as: "Mac Universal Clipboard not working", "clipboard not syncing", "iPhone copy Mac paste not working", "iPad and Mac cannot copy paste", "Handoff clipboard broken", "Universal Clipboard stopped syncing", or equivalent wording.

## Fast Fix

If the user has authorized local Mac troubleshooting, run:

```bash
defaults delete ~/Library/Preferences/com.apple.coreservices.useractivityd.plist ClipboardSharingEnabled 2>/dev/null; \
defaults write ~/Library/Preferences/com.apple.coreservices.useractivityd.plist ClipboardSharingEnabled 1; \
killall useractivityd 2>/dev/null; \
killall sharingd 2>/dev/null; \
killall pboard 2>/dev/null; \
sleep 2; \
pgrep -fl 'useractivityd|sharingd|pboard'
```

Expected result: `useractivityd`, `sharingd`, and `pboard` appear again after launchd restarts them. Ask the user to test both iPhone/iPad -> Mac and Mac -> iPhone/iPad copy/paste.

## Why This Works

Universal Clipboard on Mac depends on three layers:

1. `pboard` manages local pasteboard state.
2. `useractivityd` manages Handoff / Continuity activity state, including the Universal Clipboard preference and shared pasteboard blobs.
3. `sharingd` manages nearby-device discovery and the sharing transport.

When iPhone and iPad still sync with each other but the Mac is isolated, Apple ID and iOS-side Handoff are probably fine. Rewriting the Mac-side `ClipboardSharingEnabled` preference and restarting these daemons is cheaper than rebooting or signing out of iCloud.

## Optional Diagnostics

Use diagnostics only if the fast fix fails or the user wants root-cause evidence.

```bash
sw_vers
defaults read ~/Library/Preferences/com.apple.coreservices.useractivityd.plist ClipboardSharingEnabled 2>/dev/null
pgrep -fl 'pboard|useractivityd|sharingd|bluetoothd'
ls -la ~/Library/Group\ Containers/group.com.apple.coreservices.useractivityd/shared-pasteboard/ 2>/dev/null
/usr/bin/log show --predicate 'process == "useractivityd"' --last 30m --style compact 2>/dev/null | tail -30
/usr/bin/log show --predicate 'process == "sharingd"' --last 30m --style compact 2>/dev/null | tail -30
```

Use `/usr/bin/log` rather than bare `log` in zsh, because `log` can resolve to a shell builtin or function in some environments.

## Escalation

If the fast fix does not work:

1. Have the user toggle Handoff off and on in System Settings -> General -> AirDrop & Handoff, and on iOS/iPadOS in Settings -> General -> AirPlay & Handoff.
2. Boot the Mac into Safe Mode once, then restart normally. This clears system caches and has historically restored broken Continuity state after macOS updates.
3. Consider deleting the Keychain item named `handoff-own-encryption-key`, then restart Handoff. This resets the Mac's local Handoff identity key.
4. Treat iCloud sign-out/sign-in as the last resort. It can trigger iCloud Drive, Photos, and Keychain resync.

For macOS beta builds, assume this may be an OS regression after the first reset fails. Avoid repeatedly applying heavier local changes when the symptoms match a beta Continuity bug.
