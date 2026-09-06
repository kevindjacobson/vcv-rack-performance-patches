# Follin / Live Trio

Open [follin-live-trio.vcv](../patches/featured/follin-live-trio.vcv) in VCV Rack Pro. The original [tim-follin-chord-arp.vcv](../patches/studies/tim-follin-chord-arp.vcv) is preserved.

## Play

- MIDI: **Minilab3 MIDI**, all MIDI channels, eight-voice input. Hold a chord. The lead, chip bass, and upper PSG arpeggios play different speeds, directions, and registers.
- Clock: **174 BPM**. The three derived rates are x4, x2, and x1 (sixteenths, eighths, quarters). ML Trigger Delay modules set note lengths separately.
- Arturia mod wheel opens the chip-bass filter; keyboard velocity controls the PSG layer.
- Arturia pitch-bend strip/wheel transposes **the entire sounding chord across all three synth families by ±2 semitones**, including in bass-controlled mode. For example, C–E–G sounds as D–F♯–A at full upward bend. Bend is continuous and is not snapped back into the selected scale. It is added *after* the arpeggiators so their stored notes remain an unbent reference: returning the strip to center restores the original chord, and new notes played while bending do not get bent twice. It does not pitch-shift the dry microphone or dry bass.
- The four MiniLab faders are performance macros: **1 lead octave span, 2 bass octave span, 3 sparkle octave span, 4 shared note length**. Use the MiniLab's Arturia or User MIDI program, not its DAW/MCU program.
- **PUSH Hold** selects the chord source: light off = Arturia; light on = bass. The large PUSH button temporarily flips that selection. Source changes include a short gate reset; MIDI note changes include per-voice retrigger masking.

## Chiptune punk band

The new bottom-row drum section is a deterministic 174 BPM backing band driven by the rack's existing x4/sixteenth clock. Four **SEQ 3** lanes hold an editable two-beat punk cell:

| Lane | Default enabled steps | Role |
| --- | --- | --- |
| Kick | 1, 3, 7 | Driving, syncopated low pulse |
| Snare | 5, 8 | Backbeat plus a pickup crack |
| Closed hat | 1–8 | Continuous metallic sixteenths |
| Fill | 6, 7, 8 | Descending three-hit tom/rim roll |

Click any lane's eight gate buttons to rewrite the rhythm without losing clock alignment. The hat lane's first two CV rows contain the per-step accent and global-tune contour; the fill lane's first CV row controls its descending tom pitch. Those knobs can be reshaped, automated, or patched elsewhere. The dedicated **PUSH Hold** beside the fill lane toggles the fill pattern; it does not reset any sequencer. The **Bitshift** module is neutral at 0 by default—small negative settings are a deliberately savage lo-fi performance effect, so lower the drum strip before exploring it.

## 8-bit pseudo chord

The bottom row now includes a fourth melodic layer built the old console way: one bright pulse oscillator cycles through the selected triad so rapidly that the ear fuses the notes into a buzzy chord. It follows either the Arturia chord or the bass-generated triad, shares the full-chord ±2-semitone pitch bend, and enters the mixer on its own quiet, slightly-left strip with a small echo send. A polyphonic OR holds one phrase envelope while any chord note is active; the rapid scan changes pitch only, avoiding a click train. A gentle low-pass keeps the switching edges musical.

The dedicated **Pseudo Clock is intentionally free-running**, independent of the 174 BPM band clock. Its three outputs are approximately 32, 48, and 64 pitch steps per second; Clock 3 is the default and measured about **66 changes per second** in the live rack. This removes beat-subdivision quantization and gives the layer its own flowing sound-chip motion. Move only the cable going to the pseudo Arpeggiator's Trigger input to switch speeds without disturbing the drums or main arps. The clock's Tempo knob provides continuous-feeling coarse rate control, the oscillator's duty-cycle switch changes the chip color, and the pseudo strip's red/blue/gray controls set level, echo, and pan.

In bass mode the pseudo chord no longer uses the conservative note-latch/grid path. Its dedicated **PitchVoltager** uses a 2048-sample frame, a 128-sample update period, and 12 ms smoothing, then feeds a chromatic quantizer directly. At 48 kHz, pitch estimates are refreshed every 2.67 ms and the analysis frame is 42.7 ms; a synthetic low-bass step test changed recognized roots in about 69 ms including control polling. A separate fast envelope follower and threshold create a continuous three-voice gate bank, so the pseudo chord does not inherit the main band's clock pulses either. Rack's dry-bass mixer path has a 54.95 ms, 100%-wet, zero-feedback compensation delay so the audible bass and pseudo chord arrive together. Scarlett hardware direct monitoring is untouched and will bypass this compensation.

The dedicated **Harmony II** is set to Chromatic with degree offsets **0 / 4 / 7**, so every chromatic bass note—including roots outside the main E-minor key—can generate a major triad. Its first three visible degree knobs are editable interval controls: set the second knob to **3** for minor; set the second and third to **3 / 6** for diminished; use **4 / 8** for augmented. This chromatic pseudo-harmony choice does not change the main band's scale-aware harmony.

## Scarlett and mixer

Scarlett 4i4 4th Gen, Core Audio, 48 kHz, 256-sample buffer. Audio module input/output offsets are zero: Scarlett inputs 1/2 and outputs 1/2.

The eight **Gig Bus** strips, in bus-chain order:

| Strip | Source | Starting state |
| --- | --- | --- |
| 1 | ChipWaves pulse lead | On, slightly left |
| 2 | Filtered VRC6 chip bass | On, centered |
| 3 | Three-register PSG sparkle | On, slightly right |
| 4 | Scarlett input 1 microphone, ~77 Hz high-pass | **Muted for feedback safety** |
| 5 | Scarlett input 2 dry bass | On, centered |
| 6 | Stereo Super Echo return | On |
| 7 | Clocked VCV Drum Machine through optional Bitshift | On, centered |
| 8 | Rapid pulse-wave pseudo chord | On, slightly left, modest echo send |

Each strip: red knob = main level; blue knob = echo send; gray = pan; small ON button = mute/unmute. The echo return's sends are zero. Begin with low hardware monitor volume. Unmute the microphone only with headphones or a feedback-safe monitoring arrangement. Hardware direct monitoring may duplicate the live signal if enabled alongside Rack monitoring.

The output has a soft saturation safety stage (8 V knee, asymptotic ceiling below 9 V) followed by a conservative audio-output level. This is protection against digital overload, **not** protection against acoustic microphone feedback.

## Bass controls the harmony

Inside Rack, pitch-to-note conversion uses **NYSTHI Pitch2Voltage**, not an external MIDI round-trip:

Input 2 → low-pass cleanup → Pitch2Voltage → Harmony II → polyphonic triad → selected arpeggiators.

Harmony II defaults to **E natural minor**. Choose its **key** and **mode** dropdowns. The three enabled generators are scale steps **0, +2, +4**: root, diatonic third, and diatonic fifth, voiced two octaves above the played bass. Major, minor, and diminished qualities follow the chosen scale; this is not simply parallel major chords. KordZ shows the resulting chord.

Use clean, single bass notes. The bass audio itself also has its own dry mixer strip. The pitch detector uses a 4096-sample analysis window and 512-sample hop; bass-tracking latency is perceptible and this is not a zero-latency guitar synth.

The generated harmony now behaves as a **note latch**. Repeated eighth- or sixteenth-note chugs on the same pitch keep the current triad held and do not refresh or restart the arpeggiators. A candidate change is smoothed for 70 ms, re-quantized, allowed to settle for 140 ms, and compared against the held root with a small equality deadband. Only a genuinely different note requests a chord update. That request waits for the next x4/sixteenth clock boundary, samples all three triad voices together, and gives the arps a 4 ms capture gap. Their x4, x2, and x1 clocks never reset, so the patterns remain on-grid and continue their phase. A real rest still closes the generated gates; restarting even on the same pitch opens a fresh phrase. Slides can intentionally produce a new in-scale chord once an intermediate note settles.

The NY envelope follower and **COMPARE** next to it suppress bass-generated notes below **0.08 V**. Adjust the Scarlett's input gain for a healthy clean signal first. If quiet sustained notes drop out, lower that threshold slightly; if idle noise triggers chords, raise it. The detector window, note gating, and threshold have been bench-tested, but your particular bass, pickup, playing style, and room still need a live check.

The real Scarlett input-2 calibration now uses an approximately **200 Hz low-pass** on the hidden analysis tap plus **60 ms Pitch2Voltage smoothing**. This does not touch the audible dry-bass route. In the live playing check, input 2 peaked at 2.38 V and the detector envelope at 0.92 V without clipping. The stability/latch chain reduced 13 rapid qualified transitions to 7 committed chord changes, and after playing stopped the envelope fell to 0.06 V—below the 0.08 V phrase threshold—so the harmony gate closed correctly.

## Pitch bend depth

The new **8vert** at the right of the top row scales the MIDI-CV **PW** output. Its first gain is **0.0333333** (3.33333%), giving ±2 semitones. Use 0.1166667 for ±7 semitones or 0.2 for ±12. The following **OctaPlus** adds this same bend to the lead, chip-bass, and PSG pitch streams. Keep MIDI-CV's own pitch-wheel V/OCT range at **0** to avoid baking bend into the arpeggiated chord; its separate PW output still works. Wheel smoothing is enabled.

## MiniLab faders

The **MIDI CC to CV** module listens to the official MiniLab 3 Arturia/User-program defaults: CC82, CC83, CC85, and CC17. Faders 1–3 select one through four octaves independently for the lead, bass, and sparkle arpeggiators. Fader 4 scales all three gate lengths together from tight staccato to the designed maximum; its CV is constrained to 2–10 V so the bottom position remains audible. Startup values preserve the patch's original character: lead three octaves, bass one octave, sparkle two octaves, and full note length. Moving a fader takes control immediately.

## Verified

- Pure-tone tests from five-string **B0 (30.87 Hz)** to E3; low-level sine, triangle, and saw tests at B0/E1/A1/E2 were within 0.6 cents after settling.
- All seven C-major diatonic triads matched expected pitches, including B diminished.
- Four-note MIDI chord replacements and keyboard/bass/held-keyboard switching produced the expected note sets after the retrigger fix.
- Removing the bass test signal cleared all three arpeggiator gates. MIDI all-notes-off also cleared all three in keyboard mode.
- Internal stereo recordings showed no digital clipping, with the tested dry synth peak around -3 dBFS **before** the final output attenuation. The final output attenuates by another ~5 dB. The bass stress-test tail fell below -100 dBFS.
- **follin-live-demo.wav** is a short generated MIDI demonstration of the synth mix at the final output gain; it does not include the live microphone or bass.
- All four MiniLab fader CC paths were exercised in a muted virtual-MIDI test. Each arpeggiator traversed its full one-to-four-octave range, and the articulation macro remained bounded from 20% to 100%.
- The final bass note latch was instrumented with a temporary binary event counter while a 70 ms synthetic E1/A1 bass pulse chugged on every sixteenth. Same-note trials produced **0 updates in 20 seconds**; changing E1→A1 produced exactly **1** update (about 0.46 s including pitch tracking and grid wait), and the count remained at 1 for another 20 seconds of A1 chugs.
- The drum lanes were counted over two-second windows at 174 BPM: kick 9 triggers, snare 6, closed hat 23, fill 0 while off and 8 while held. With neutral Bitshift, the tested drum generator peak was about 2.10 V and the protected mix peak about 1.96 V while the other live sources were idle.
- The free-running pseudo-chord clock produced **132 triggers in 2.01 seconds** (about 66 Hz), with its external-clock input disconnected. The common bend summer remains after note selection, and all pitch/gate/audio routes were verified in the saved patch.
- A synthetic **C♯2**, outside E natural minor, tracked at -1.9167 V and produced the exact chromatic major-triad outputs C♯–E♯–G♯. Eight C♯2↔D♯2 transitions were recognized 8/8 with a 68.8 ms median control-observed response. Subsequent live passes exposed adjacent chromatic roots; the independent phrase gate produced three active chord-gate channels with no clock cable in its path.
- A live Scarlett input-2 bass pass reached 2.38 V peak with a 0.92 V detector envelope. After the analysis-only filter/smoothing calibration, 13 rapid pitch candidates yielded 7 held-note updates; on release the phrase gate returned low despite residual input noise.

No claim is made that your real microphone/bass gain or acoustic feedback behavior has been auditioned. The microphone is deliberately muted pending safe monitoring confirmation.

## Module references

- [Harmony II manual](https://github.com/squinkylabs/SqHarmony/blob/main/docs/harmonyII.md)
- [ML Modules source and manuals](https://github.com/martin-lueders/ML_modules)
- [NYSTHI module notes](https://github.com/nysthi/nysthi/blob/master/changelog1.0.1_parsed.md)
- [Gig Bus mixers](https://github.com/gluethegiant/gtg-rack)

Harmony II was installed from its author's ARM64 2.2.5 release. All other performance modules were already installed. Wiring and parameters were built through the local VCV Rack MCP; unsupported saved-state fields and layout were staged in versioned patch files. The useful test racks and rollback points are preserved under `patches/development`, and the repository metadata records every patch and dependency.
