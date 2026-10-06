# NetSpeedTray - ZeroFlagLabs Fork Notes

Last updated: 6 October 2026

## Purpose

This fork contains my personal NetSpeedTray build plus several fixes and features
developed against the upstream project:

https://github.com/erez-c137/NetSpeedTray

The personal build is maintained on:

`zeroflaglabs-modified`

## Current Personal Release

Version: `2.1.7.2`

Tag: `v2.1.7.2`

Release source commit:

`fa89206410d509f4c5a1cc17b83bb9a71967d5b8`

The release contains:

- `NetSpeedTray-2.1.7.2-x64-Setup.exe`
- `NetSpeedTray-Portable-2.1.7.2.zip`
- `checksums.txt`

The installer is locally built and unsigned.

## Changes Included

### RAM / VRAM label alignment

Branch:

`ram-vram-label-fix`

Keeps RAM and VRAM labels stationary when the displayed memory value changes
width.

Submitted upstream as PR #326.

### Configurable section spacing

Branch:

`section-spacing-option`

Adds configurable spacing between the visual widget sections.

Also includes:

- Network alignment inside its reserved layout slot
- Correct Network Position 1 / 2 / 3 behaviour in stacked hardware layout

Not currently submitted upstream.

### Section dividers

Branch:

`section-divider-option`

Adds optional 1 px divider lines between visual widget sections.

Depends on the section-spacing work.

Not currently submitted upstream.

### Build path fix

Branch:

`fix-build-path-quoting`

Fixes build failures when the repository path contains spaces or parentheses.

Also causes `build.bat` to stop immediately if PyInstaller fails instead of
continuing into Inno Setup.

Submitted upstream as PR #329.


### Lock Free Move Position

Branch:

`floating-position-lock`

Adds an optional lock for the existing Free Move mode.

When Free Move is enabled, `Lock Free Move Position` can prevent accidental
dragging of the widget. Turning Free Move off automatically clears and disables
the lock.

Default: Off.

### Free Move left-edge positioning

The personal build allows a small controlled left-edge overhang while using
Free Move.

The widget may extend up to 12 px beyond the physical left edge of the screen,
allowing the visible readout to sit flush with the screen edge.

The right, top and bottom edges remain fully constrained on-screen.

### Hardware unit spacing

Branch:

`hardware-unit-spacing`

Adds an optional `Space Before Hardware Units` setting.

When enabled, CPU/GPU percentages and RAM/VRAM gigabyte units use the same
5 px value-to-unit gap already used by the Network readout.

Examples:

- `45 %`
- `7.2/15.8 G`

Default: Off.

The personal build also includes a small RAM/VRAM label-cell padding adjustment
so RAM and VRAM retain their fixed alignment while keeping a natural visual gap
before the memory value.

## Personal Build Identity

The `zeroflaglabs-modified` branch contains personal-build-only changes.

Current personal version:

`2.1.7.3`

Update checks are redirected from:

`erez-c137/NetSpeedTray`

to:

`ZeroFlagLabs/NetSpeedTray`

The normal NetSpeedTray application name, AppId, executable name, mutex,
installation directory and AppData directory are deliberately unchanged.

This allows the personal installer to upgrade the official NetSpeedTray
installation in place while preserving existing settings.

## Updating This Fork in Future

When upstream releases a new version:

1. Fetch the latest upstream repository.
2. Review upstream changes before merging or rebasing.
3. Check whether any local fixes or features have already been merged upstream.
4. Bring the remaining personal changes onto the new upstream version.
5. Keep personal build identity changes only on `zeroflaglabs-modified`.
6. Bump the personal version, for example upstream `2.1.8` -> personal `2.1.8.1`.
7. Run the complete test suite.
8. Build the installer and portable ZIP.
9. Verify SHA-256 checksums independently.
10. Install and test the packaged build.
11. Tag the tested commit and create a GitHub Release.

## Building

From the repository root:

`build\build.bat`

The build requires:

- Python virtual environment in `.venv`
- Inno Setup 6
- Normal project dependencies

Successful builds are placed under:

`dist\NetSpeedTray-<version>\`

## Upstream Remote

Expected remotes:

- `origin` -> `ZeroFlagLabs/NetSpeedTray`
- `upstream` -> `erez-c137/NetSpeedTray`

## General Rule

Do not put personal version or update-identity changes onto branches intended for
upstream pull requests.

Keep upstream PR branches small and independent wherever practical.
