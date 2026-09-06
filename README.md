# Bass-Controlled VCV Rack Performance Patches

A private working collection of 30 VCV Rack Pro patches built around an Arturia MiniLab 3, a Scarlett 4i4, live bass pitch tracking, chiptune arranging, and shaped-noise sound design.

## Start here

- [Follin / Live Trio](patches/featured/follin-live-trio.vcv) is the full chiptune-punk performance rack: MIDI chord arpeggiators, bass-generated harmony, free-running pseudo chords, drums, microphone, dry bass, pitch bend, and MiniLab fader macros.
- [Bass Triple Drive](patches/featured/bass-triple-drive-mixer.vcv) splits Scarlett input 2 into clean, RAT, and HM-2-inspired paths with independent three-state octave selection.
- [Five Bass Variants](docs/OVERNIGHT-BASS-RACKS.md) are alternate bass-controlled instruments built from the live-trio architecture.
- [Wind Simulation](patches/studies/wind-simulation.vcv) is the original shaped-noise and slow-modulation study.

See [Patch Index](docs/PATCHES.md) for every release, experiment, test rack, and development checkpoint.

## Hardware assumptions

- Audio interface: Scarlett 4i4 4th Gen at 48 kHz
- Input 1: microphone
- Input 2: bass
- Outputs 1/2: stereo monitoring
- MIDI controller: Arturia MiniLab 3 (`Minilab3 MIDI`)

Hardware and MIDI selections are stored in several performance patches. If Rack cannot find an exact device name, choose the replacement in the Core Audio or MIDI module.

## Audio safety

Most performance and historical patches contain cables to Audio 2 outputs 1/2. Begin with the Scarlett monitor level down and raise it gradually. The microphone channel in the current live-trio rack starts muted, but that is not a substitute for feedback-safe monitoring.

The triple-drive patch is the exception: its final limiter is deliberately disconnected from Audio 2 and Audio 2 starts at zero.

## Modules and cost

The complete [Module and Plugin Catalog](docs/MODULES.md) links all 68 unique modules used across the collection and labels each one as free, paid, or locally installed.

At the time of catalog generation:

- 66 modules are available free from the VCV Library.
- VCV Drum Machine belongs to the paid **VCV Drums** bundle ($30) and appears in 15 patches.
- The MCP Server is a free MIT-licensed local helper. It is not in the VCV Library and does not generate or process sound.

## Repository layout

```text
patches/
  featured/                 current performance-ready racks
  bass-variants/            five alternate bass-controlled instruments
  studies/                  original wind and chord-arpeggiator studies
  development/
    iterations/             major work-in-progress milestones
    tests/                  purpose-built test racks
    checkpoints/            rollback snapshots before major changes
docs/                       performance guides and catalogs
metadata/                   generated inventories, checksums, and validation
tools/                      catalog and validation utilities
```

All patch archives were repackaged with a single canonical `patch.json` and stripped of absolute `/Users/...` paths. Recordings, downloaded third-party source trees, local autosaves, and MCP audit logs are intentionally excluded.

The latest [load-validation report](metadata/load-validation.json) records a hardware-disabled Rack Pro load test for every patch.
