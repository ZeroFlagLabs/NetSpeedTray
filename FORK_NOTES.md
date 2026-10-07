# NetSpeedTray - ZeroFlagLabs Fork Notes

Last updated: 6 October 2026

## Purpose

This fork contains my personal NetSpeedTray build plus several fixes and features
developed against the upstream project:

https://github.com/erez-c137/NetSpeedTray

The personal build is maintained on:

`zeroflaglabs-modified`

## Current Personal Release

Version: `2.1.7.4`

Tag: `v2.1.7.4`

Release source commit:

`6fd0f261466a640f9861bb9073abb76e9b82a9d6`

The release contains:

- `NetSpeedTray-2.1.7.4-x64-Setup.exe`
- `NetSpeedTray-Portable-2.1.7.4.zip`
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


### Position locking

The original Free Move position lock has been expanded into a general
`Lock Position` setting.

The lock is available in both taskbar-docked and Free Move modes. It prevents
manual dragging without blocking legitimate application-driven repositioning,
such as when the active taskbar, display geometry or monitor arrangement
changes.

Default: Off.

### Side-by-side memory spacing and alignment

In Side-by-Side mode, RAM and VRAM use a fixed 6 px gap between the memory
label and its value.

CPU and GPU values above them align with the right edge of their corresponding
RAM and VRAM value. This keeps each CPU/RAM and GPU/VRAM pair visually aligned
while allowing the memory value to grow naturally from its label.

### Content anchoring

The widget provides a selectable `Content Anchor` in both taskbar-docked and
Free Move modes:

- `Left` keeps the visible content anchored at the left and lets changing
  values grow or shrink to the right.
- `Right` keeps the visible content anchored at the right and preserves unused
  space on the left as expansion headroom.

Screen-edge positioning uses the visible content rather than the full reserved
widget window. This allows transparent or unused width to extend beyond the
screen while keeping the selected visible edge approximately 1 px inside the
physical display edge.

Free Move still stores an absolute desktop position, so the settings page
explicitly warns that its position may need adjustment after changes to
displays, resolution, scaling/DPI or monitor arrangement.

### Stable taskbar-docked positioning

Taskbar-docked positioning no longer uses the moving system-tray boundary as
the permanent horizontal reference after the user chooses a position.

Horizontal docked placement is stored as a normalized visible-content position
across the current screen. When display geometry changes, NetSpeedTray rebuilds
the X position against the current screen while independently recalculating Y
from the current taskbar.

This prevents tray/clock geometry changes from moving a user-positioned widget
and makes docked placement resilient to resolution, DPI and monitor-topology
changes.

The existing tray-relative offsets remain available as compatibility/default
placement data, but no longer drive the horizontal position once a docked
position has been established.

### Hover-card positioning

The data-usage hover card is centred over the content that is actually visible
at the time instead of the full reserved widget width.

This prevents anti-jiggle expansion space from visually shifting the hover card.

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

`2.1.7.4`

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
