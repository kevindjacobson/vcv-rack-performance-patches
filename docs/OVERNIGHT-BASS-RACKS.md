# Five Bass-Controlled Performance Racks

These patches are variations of the proven `follin-live-trio.vcv` input,
tracking, mixer, and safety architecture. Scarlett input 2 is the bass input.
The original live patch was not overwritten.

## Before playing

1. Wait until you are back at the computer and ready to monitor sound.
2. Open one `.vcv` patch at a time.
3. Put on headphones or turn the Scarlett monitor level down, then bring it up
   gradually. Each patch has conservative strip levels and a final `cf PEAK`
   safety stage, but the bass's interface gain still matters.
4. Play one clean note for calibration. If tracking flickers, adjust the
   Scarlett input-2 gain rather than raising the Rack master.

On the MiniLab 3, hold **Shift** and tap **Pad 3 / Prog** until its display
shows **ARTURIA**. That program sends the four fader CCs already mapped in
these racks (82, 83, 85, and 17). The racks start with all four performance
macros neutral; move a fader once to take control of its macro.

The MiniLab pitch strip bends the original keyboard chord voices, the fast
pseudo-chord voice, and each rack's principal pitched layer by **±2
semitones**. In Icebreaker, it bends the granular voice while the unbent bass
note continues selecting the slice pattern.

The bass tracker runs chromatically at a short 2048-sample frame and 128-sample
period. A separate stable-note latch accepts actual pitch changes on the clock
grid while rejecting repeated same-note 8th/16th-note chugs. The dry bass path
keeps its natural articulation.

Every rack retains the 174 BPM chip-punk drum machine and its preset kick,
snare, hat, and fill sequencers. Use the latched **FILL** Push switch in the drum
row to bring the alternate fill gates in and out without disturbing the clock.

## 1. Cathedral Wire

File: [bass-rack-01-cathedral-wire.vcv](../patches/bass-variants/bass-rack-01-cathedral-wire.vcv)

The bass excites an Audible Instruments Resonator tuned to the detected note.
Only a stable note change strikes it, so chugs sustain the space instead of
machine-gunning the resonator. The odd/even resonances feed a stereo Texture
Synthesizer cloud.

- Fader 1: resonator brightness
- Fader 2: damping
- Fader 3: resonator structure
- Fader 4: granular blend
- Try: widely spaced fifths, upper-register harmonics, and long rests

## 2. FM Riot Reactor

File: [bass-rack-02-fm-riot-reactor.vcv](../patches/bass-variants/bass-rack-02-fm-riot-reactor.vcv)

Stable bass changes trigger a retro two-operator Vult FM voice. A mechanical
chaos source moves the modulation while Debriatus adds controlled fold, crush,
distortion, and saturation. The chip-punk drums are louder in this one.

- Fader 1: chaos speed
- Fader 2: chaos energy
- Fader 3: digital crush modulation
- Fader 4: saturation modulation
- Try: E-string pedal tones with sudden minor-third or tritone jumps

## 3. Icebreaker Glitch Looper

File: [bass-rack-03-icebreaker-glitch-looper.vcv](../patches/bass-variants/bass-rack-03-icebreaker-glitch-looper.vcv)

The latency-aligned bass is captured by Path Set IceTray. Record and playback
clocks use different divisions, so the rack makes repeatable rhythmic shards
without losing the main grid. A second granular stage spreads them in stereo.

- Fader 1: frozen-track percentage
- Fader 2: feedback
- Fader 3: grain position
- Fader 4: grain density
- Try: two bars of steady chugs, then stop and move the faders

## 4. Polybeast Chord Swarm

File: [bass-rack-04-polybeast-chord-swarm.vcv](../patches/bass-variants/bass-rack-04-polybeast-chord-swarm.vcv)

Each stable bass note becomes a three-voice chromatic chord. The root does not
need to belong to a preselected key. Note-change pulses trigger all three
voices together, a Plaits-style voice supplies the timbre, and a stereo comb
resonator adds moving metallic space.

- Fader 1: harmonic content
- Fader 2: timbre
- Fader 3: morph
- Fader 4: comb feedback
- Try: chromatic descending lines and notes outside the nominal key

## 5. Elemental War Drums

File: [bass-rack-05-elemental-war-drums.vcv](../patches/bass-variants/bass-rack-05-elemental-war-drums.vcv)

Every new stable bass note strikes a stereo physical-model voice and a
pitch-following FM percussion layer. Repeated same-note chugs remain the dry
bass rhythm; genuine pitch changes summon the synthetic ensemble.

- Fader 1: resonator geometry
- Fader 2: brightness
- Fader 3: energy dissipation
- Fader 4: internal reverb space
- Try: sparse root/fifth riffs, octave jumps, and dramatic rests

## Dependencies

The five patches use modules already installed before the overnight build:

- VCV Fundamental and Core
- Audible Instruments
- Vult Modules Free
- Path Set: Free
- ML Modules
- Squinktronix Harmony II
- NYSTHI
- Glue the Giant
- HetrickCV
- Sulamith
- cf
- VCV Drums
- Bacon Music and Potato Chips

Bogaudio 2.6.47 and Befaco 2.11.0 were also subscribed, downloaded, and
installed as free VCV Library plugins for later expansion. They activate after
Rack's next safe restart, but none of these five patches depends on them.

## Output routing

These five performance patches retain their stereo Audio 2 output cables. Begin
with the Scarlett monitor level down, open only one patch at a time, and raise
the monitor level gradually. Their conservative strip levels and `cf PEAK`
stage protect against digital overload, not excessive acoustic playback level.
