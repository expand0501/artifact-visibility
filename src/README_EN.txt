Artifact Visibility 1.0.2 by Expand
===================================

Artefacts lying in the world are always visible, like in Shadow of Chernobyl: no detector needed to see them.
Their glow light and particles can be switched on or off in MCM.

Remake of "SoC-style Artefacts (DLTX)" by MaxSpringer. One mod instead of several install variants, and it
covers every artefact in the game, including GAMMA's own, junk artefacts and artefacts from other mods.

Features
- Artefacts always visible without a detector.
- MCM: artefact glow light on/off, artefact particles on/off, detectors keep their tiers on/off,
  master switch, debug log.
- Works with any artefact mod: artefact sections are found automatically when the game loads.
- No cost during gameplay: the mod works once while a save loads (the detector tier mode adds
  a tiny check per artefact every 2 seconds).

Requirements
- Anomaly 1.5.x with modded exes (DLTX), e.g. G.A.M.M.A. Also works on the Quark engine.
- MCM is optional (without it the defaults are used: detector tiers on, light on, particles on).

Install
- Install the zip with Mod Organizer 2 (or copy gamedata into the game folder).
- Remove/disable the old "SoC-style Artefacts (DLTX)" mod and all of its variants and patches
  (Main, No Lights, No Particles, Junkies, BAM). Otherwise its values count as the originals and
  the light/particles options can't bring them back.
- Can be installed or removed mid-playthrough. Changes take effect after loading a save.

Settings (MCM -> Artifact Visibility)
All settings take effect after you load a save or start a new game.
- Enable mod: off = all artefacts behave as without this mod.
- Detectors keep their tiers: artefacts stay visible, but a detector only beeps for the artefacts of
  its tier, as in normal GAMMA (on by default). Off = every detector finds every artefact.
- Artefact glow light: the coloured light around artefacts.
- Artefact particles: glowing halo, sparks, smoke around artefacts. Turn this off too if artefacts still
  look like they glow with the light off.

Bug reports
Turn on "Debug log" in MCM, load a save, and send the [SoCArts] lines from <Anomaly folder>/appdata/logs/xray_*.log.

Version history
- 1.0.2: removed the "Artefacts always visible" MCM option: artefacts are always visible while the mod is enabled.
- 1.0.1: "Detectors keep their tiers" is now on by default.
- 1.0.0: first public release (version label only, no code changes).
- 0.3.0: renamed to "Artifact Visibility" (no functional changes).
- 0.2.0: new MCM option "Detectors keep their tiers".
- 0.1.0: first version.

Credits
- MaxSpringer: original idea and mod "SoC-style Artefacts (DLTX)".
- Expand: this remake.
