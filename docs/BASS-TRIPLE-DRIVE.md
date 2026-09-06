# Bass Triple Drive Mixer

Open [bass-triple-drive-mixer.vcv](../patches/featured/bass-triple-drive-mixer.vcv) in VCV Rack Pro.

Scarlett input 2 is split into three independently mixable VCV VCA Mix channels:

1. Clean
2. NYSTHI RodentV2 (Pro Co RAT emulator)
3. HM-2-inspired chain: boosted three-band EQ into Bidoo bAFIs multiband distortion and a hard clipper

MiniLab 3 pads 1, 2, and 3 control the Clean, RAT, and HM-2 octave selectors. Each tap advances that path through `original`, `+1 octave`, and `-1 octave`. The selectors start in `original`; their three LEDs show the current state.

The pad assignments listen for MIDI notes 36, 37, and 38 on any MIDI channel. If an Arturia preset changes those notes, click the first three cells in **MIDI to Gate** and tap the desired pads to relearn them.

## Silent staging

The rack is deliberately unable to reach the Scarlett outputs yet: Audio 2 is at zero and the final LMTR outputs are not connected to Audio 2. When monitoring is safe, connect LMTR L/R to Audio 2 outputs 1/2, then raise Audio 2 slowly.
