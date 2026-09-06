# Shaped Noise Wind Simulation

Built in VCV Rack 2.6.6 through the Neural Harmonics VCV Rack MCP Server.

Signal flow:

- Pink noise feeds a low-pass VCF at about 456 Hz for the wind body.
- White noise feeds a high-pass VCF at about 1.2 kHz for the air/hiss layer.
- A 0.171 Hz unipolar LFO slowly sweeps both filters with different waveforms.
- Both filtered layers enter VCA Mix, with the high-frequency layer additionally modulated by a 0.050 Hz triangle wave for gust variation.
- The mixed result passes through an exponential VCA, whose amplitude is modulated by the same slow LFO's sine output.
- The final signal is sent to both channels of Audio 2 at a conservative output level.

Open [wind-simulation.vcv](../patches/studies/wind-simulation.vcv) in VCV Rack. In the Audio 2 module, select your preferred Core Audio device before listening, and start with a low system volume.
