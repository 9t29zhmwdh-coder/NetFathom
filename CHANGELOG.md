# Changelog

All notable changes to NetFathom will be documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.1.2] - 2026-07-31

### Fixed

- Lint and tests ran on Linux only, while the release builds a PyInstaller executable for Linux, macOS and Windows. Five modules branch on `platform.system()` or `sys.platform`, and layer-2 scanning uses raw sockets, which behave differently on Windows. Only the Linux branch was ever executed, so the macOS and Windows paths shipped untested. The check job now runs as a matrix over all three. The formatting check stays on one runner, being platform-independent.
- The `solo-main-protection` ruleset now requires `Lint & Check (ubuntu-latest)`, `(macos-latest)` and `(windows-latest)` instead of the old single `Lint & Check`. Renaming a job without moving the required context leaves every later pull request permanently unmergeable while looking green.

---

## [1.1.1] - 2026-07-31

### Changed

- The README opens with what the tool answers rather than what it contains. It began "a cross-platform Network Discovery and Diagnostic Toolkit" followed by four verbs, which describes any scanner. What distinguishes this one is that it stores every scan, so "what changed since last time" becomes answerable; that is now the first line, with the three commands that get there.
- The opening names the case this tool is not for: a one-off look at who is online, where `arp-scan` or `nmap` do the job in a line and need no database. The repository description follows.

---

## [1.1.0] - 2026-07-30

### Changed

- The speedtest protocol derives its header length from the magic value instead of hardcoding it. The old magic `NETSCANX` was eight bytes and the code relied on that in two comparisons and one payload calculation; `NETFATHOM` is nine, which made every comparison false and every packet one byte too long. The rename would have silently broken the UDP throughput measurement.
- Renamed from NetScanX to NetFathom. netscanx.com is an active commercial product that also analyses network traffic, so the collision was in the same category rather than merely a similar word.

---

## [1.0.6] - 2026-07-29

### Security

- The release workflow no longer grants `contents: write` for its whole run. The permission moves to the one job that publishes the release, and everything else runs with `contents: read`. OpenSSF Scorecard scores the Token-Permissions check 0 out of 10 whenever any workflow holds a top-level write permission, regardless of how little of the run needs it, so this single line was what held the check at zero.

---

## [1.0.5] - 2026-07-29

### Changed

Dependency and workflow updates merged since 1.0.4:

- chore(ci): bump the actions group across 1 directory with 4 updates

---

## [1.0.4] - 2026-07-28

### Changed

- CodeQL moved from GitHub's default setup to an advanced setup with a committed `.github/workflows/codeql.yml`. The default setup skips pull requests that touch no code of a given language, so a dependency pull request changing only a lock file reported `skipping` on the required `Analyze (...)` checks forever and could never be merged. The workflow runs on every pull request regardless of what changed and uses the `security-extended` query suite, which the default setup does not allow choosing. Required checks are unchanged.
- The CodeQL job requests only `security-events: write` beyond the workflow-level `contents: read`. Repeating read grants at job level is what OpenSSF Scorecard counts as excessive token permissions, and it costs the full `Token-Permissions` score.
- Dependabot now groups only minor and patch updates per ecosystem; majors arrive as individual pull requests. The previous grouping bundled breaking changes with urgently needed security patches into one unreviewable diff. Actions stay grouped wholesale. Follows `engineering-standards` v0.11.0.

## [1.0.3] - 2026-07-28

### Fixed

- CI ran `ruff check . --select E9,F821,F822,F823`, which overrode the `select = ["E", "F", "W", "I"]` configured in `pyproject.toml`. Only syntax errors and undefined names were ever checked, so the configuration described a standard the pipeline did not apply, and a green run said less than it appeared to. CI now runs the configured rule set and a `ruff format --check` that did not exist before. See `engineering-standards` `standards/ci-cd.md` section 3: a stage is fixed, not scoped down.
- The 33 findings this surfaced: 11 unused imports, 9 module-level imports below other code in `cli/main.py`, 6 unsorted import blocks, 3 unused local variables, 3 f-strings without placeholders, and one ambiguous variable name `l`. The imports in `main.py` sat below the `cli()` group definition, which is a common Click pattern to avoid a circular import; verified here that no subcommand module imports from `main`, so moving them to the top is safe. 51 tests pass and the CLI still registers all nine subcommands.
- `[tool.ruff] select` moved to `[tool.ruff.lint] select`, which ruff has been warning about as deprecated.

## [1.0.2] - 2026-07-28

### Added

- `.github/dependabot.yml`, covering GitHub Actions and pip with grouped weekly updates. The file was missing, and without it there are no version updates at all: security alerts only fire for disclosed vulnerabilities. The `actions/checkout` pin here had been sitting on v7.0.0 while v7.0.1 was current. Follows `engineering-standards` v0.10.0.

### Changed

- `ruff` is pinned to 0.16.0 instead of `>=0.5.0`. An open range lets a new release change what counts as correct on unchanged source and turn CI red without a commit, which happened to `AdapterForge` earlier today.

## [1.0.1] - 2026-07-20

### Changed

- OpenSSF Scorecard workflow and badge.
- `copilot-instructions.md` for consistent AI-assisted contributions.
- Unified the EN/DE language-switch link format.
- Fixed a duplicated `[0.3.12]` CHANGELOG entry and a misplaced `[Unreleased]` heading.
- Split the README's security/CI badges onto their own line, separate from the platform/tech/AI badges (they were rendering as a single merged line).

## [1.0.0] - 2026-07-17

First stable release: a real, packaged, installable distribution
(single-file binaries for Windows/macOS/Linux, attached to every
GitHub Release) already exists for end users, the prerequisite for a
1.0 release per this portfolio's own SemVer discipline.

## [0.3.12] - 2026-07-17

### Added

- README.md/README.de.md: "How it runs" callout, "In practice" paragraph, and "Uninstall/Cleanup" section (adapted for a CLI tool with an optional local dashboard and portable/USB mode), which this repo was missing entirely in both languages.

### Changed
- CI: added an explicit `permissions: contents: read` block to the workflow(s) that were missing one (CodeQL `actions/missing-workflow-permissions`), narrowing the default GITHUB_TOKEN scope.

## [0.3.11] - 2026-07-12

### Removed

- Stale scaffold-tool bookkeeping files SKELETON.md and TEMPLATE_NOTES.md (internal generator artifacts, not real project docs).

## [0.3.10] - 2026-07-12

### Added

- TERMS_OF_SALE.md: terms covering the purchase of a pre-built, packaged distribution through a marketplace (as-is, no warranty, liability strictly capped at the amount paid). Does not modify the existing MIT LICENSE, which continues to cover the source code at no cost.

## [0.3.9] - 2026-07-12

### Added

- Dual-Licensing skeleton: LICENSE.COMMERCIAL, COMMERCIAL.md, and ENTERPRISE_FEATURES.md, documenting the licensing model for a future Enterprise Edition ahead of any actual feature split. The existing MIT LICENSE and all currently released code are unchanged; nothing in this repository is restricted by this addition.

## [0.3.8] - 2026-07-12

### Fixed

- Removed an eszett and em-dashes/en-dashes across the repo (docs, LICENSE, .env.example, scripts, CLI docstrings and messages, diagnostics/checks.py, output.py, and the dashboard's index.html). Swiss German orthography.

## [0.3.7] - 2026-07-11

### Added

- Documented Dual-Licensing readiness assessment in ROADMAP.md.

### Fixed

- Removed em-dashes from ROADMAP.md headings.

## [0.3.6] - 2026-07-11

### Fixed

- Replaced the unmonitored security@raystudio.ch email in SECURITY.md with a GitHub Security Advisory link, matching the rest of the portfolio.

## [0.3.5] - 2026-07-11

### Fixed

- Updated actions/setup-python, actions/upload-artifact and actions/download-artifact to their latest major versions in CI and the release workflow, since GitHub is deprecating the Node.js 20 runtime and older action versions were being forced onto Node 24 and crashing during post-run cleanup.

## [0.3.4] - 2026-07-10

### Fixed

- Removed em-dash from README.md/README.de.md, replaced with a colon

## [0.3.3] - 2026-07-10

### Added

- Windows release binary is now signed with a self-signed certificate (`signtool`, RFC3161 timestamped). Does not remove the SmartScreen warning (no trusted CA), but the signature does guarantee the file wasn't tampered with after release

## [0.3.2] - 2026-07-10

### Added

- Release workflow now also builds `NetScanX-Start-macOS.dmg`, a disk image wrapping the portable macOS binary for a more familiar download experience. Not code-signed, same Gatekeeper warning as the raw binary.

### Fixed

- Release workflow lacked `contents: write` permission, so the automated GitHub Release creation on tag push always failed with HTTP 403 (v0.3.1 tag was pushed but its release creation failed for this reason; skipped straight to 0.3.2 rather than deleting/retagging v0.3.1)

## [0.3.0] - 2026-07-09

### Added
- `netscanx baseline`: run a fresh scan and pin it as the reference baseline for drift detection.
- `netscanx changes [--since-baseline|--since-last]`: show devices/ports/services that changed since the last scan or the pinned baseline. This is the project's new centerpiece feature.
- `netscanx assets`: list the persisted device inventory (distinct from a single scan's transient results).
- `netscanx health [TARGET]`: local machine health checks (disk/CPU/RAM/Defender/BitLocker/Windows Update) without a target, or lightweight network-observable health signals (reachability, DNS response, risky open ports) for a given host.
- `discover --persist [--db-path PATH]`: persist scan results to the local SQLite inventory so they participate in baseline/drift detection.
- Passive Asset Discovery Plus: every discovered host now gets a best-effort `os_guess` (TTL heuristic) and `device_type` (printer/NAS/router/access-point/workstation/server) classification, with no additional network calls or credentials required.
- SQLite persistence layer (SQLAlchemy 2.0 async + aiosqlite): every scan is stored as a `ScanRun` with per-device `DeviceSnapshot`s, diffed against the previous snapshot to produce `ChangeEvent` records.
- Dashboard: new Change Report and Asset Inventory cards, a Pin Baseline button, and `GET /api/changes`, `GET /api/assets`, `POST /api/baseline` endpoints. The background scan now persists automatically and broadcasts a `change_detected` WebSocket event when drift is found.
- Portable USB launcher: single-file PyInstaller binaries for Windows/macOS/Linux (`NetScanX-Start-Windows.exe`, `NetScanX-Start-macOS`, `NetScanX-Start-Linux`). Double-clicking with no arguments launches the dashboard; running from a terminal exposes the full CLI. The SQLite database is stored next to the binary (`NetScanX-Data/`) so scan history travels with the USB stick across machines. Built automatically on tagged releases via `.github/workflows/release.yml`.
- Initial `tests/` suite (pytest + pytest-asyncio) covering the DB path resolution, schema round-trips, device identity heuristics, drift-detection diff logic, health score arithmetic, and an end-to-end persistence/diff scenario. CI now runs `pytest` in addition to lint.

### Changed
- Version bumped to 0.3.0.
- `netscanx/models.py`: `Host` gained two optional fields, `os_guess` and `device_type`, populated by the new passive enrichment pass.

### Security
- New credential-requiring features (WMI-based enrichment, WinRM-based remote health checks) are intentionally left as unimplemented interface stubs in this release rather than shipped half-finished; when implemented, they will use OS-keychain-backed credential storage per SECURITY.md, never `.env`/plaintext.

## [0.2.0] - 2026-07-06

### Fixed
- `discover`: MAC vendor lookup and hostname were always empty on non-root runs. The ARP sweep silently fell back to a MAC-less ping sweep, and no reverse DNS lookup existed at all.
- `discover`: the OS ARP cache is now always consulted to enrich already-discovered hosts with a MAC address (pinging a host makes the OS resolve it), so `--vendor` works without `sudo`/`--arp`.
- `discover`/`services`/`diagnose`/`speedtest`/`dashboard`: progress messages (e.g. "Looking up N MAC vendors…") were printed to stdout via Rich `Console()`, corrupting `--format json`/`--format yaml` output when redirected. They now go to stderr.
- `dashboard`: the background scan only ever read the ARP cache and ran diagnostics. Host discovery (ping/ARP sweep, vendor, hostname) and service discovery (mDNS/SSDP) never ran, leaving `/api/hosts` MAC-less and `/api/services` permanently empty.
- `dashboard`: the Services table used `name + ip` as its list key; several real-world services (e.g. duplicate SSDP announcements from one host) share both, so duplicate keys made Alpine.js silently drop rows even though the count in the header was correct. The key now includes the loop index, type, and port.
- `dashboard`: the Speedtest card checked for a nested `speedtest.latency` object that the `/api/speedtest` endpoint never returns (it returns the latency stats flat), so a result never rendered even on a successful ping.

### Added
- `discover --hostname/--no-hostname`: reverse DNS hostname resolution for discovered hosts (default on).
- Dashboard: hosts table now shows a Hostname column.
- Dashboard: new Speedtest/Ping card. Run an on-demand latency test (min/avg/max/jitter/packet loss) against any IP or hostname from the browser, backed by `GET/POST /api/speedtest`.
- README/README.de: corrected macOS/Linux install instructions. Plain `pip install` fails with `externally-managed-environment` (PEP 668) on Homebrew/Debian Python; documented the venv path as the default, with the `--break-system-packages` escape hatch called out as not recommended.

### Changed
- `netscanx.cli.discover.run_discover_scan()` and `netscanx.cli.services.run_services_scan()` are now reusable async functions returning result objects, shared by the CLI commands and the dashboard instead of duplicating scan logic.

## [0.1.0] - 2026-06-13

### Added
- Initial import: ARP/ICMP/TCP scan engine
- mDNS, SSDP, NetBIOS, SNMP discovery modules
- Speedtest integration
- Auto-diagnose engine
- CLI interface (Click + Rich)
