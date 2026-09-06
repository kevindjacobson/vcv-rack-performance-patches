# Multi-Octave Chord Arpeggiator

An original performance patch inspired by the dense, register-hopping vocabulary of classic Tim Follin game scores. Built in VCV Rack Pro 2.6.6 through the VCV Rack MCP Server.

Open [tim-follin-chord-arp.vcv](../patches/studies/tim-follin-chord-arp.vcv).

## Performance

1. Hold a 3- or 4-note chord on the Arturia MiniLab 3.
2. The ML Modules PolyArp scans the held notes across three octaves at roughly 12 notes per second.
3. Use the MiniLab mod wheel to open and brighten the VRC6 bass filter.
4. Velocity controls the level of the Sega-style PSG chord layer.

## Voices

- **NES pulse lead:** Bacon Music ChipWaves, short bright envelope.
- **VRC6 bass:** KautenjaDSP Step Saw, shifted down two octaves and filtered.
- **Sega PSG sparkle:** KautenjaDSP Mega Tone with three interlocked registers at root, +1 octave, and +2 octaves.
- **Space:** KautenjaDSP Super Echo, configured as a stereo SNES-style echo with slowly moving feedback color.

The patch is configured for **Minilab3 MIDI** input and **Scarlett 4i4 4th Gen** audio I/O at 48 kHz. Output level is deliberately conservative; still begin with monitor volume low.
