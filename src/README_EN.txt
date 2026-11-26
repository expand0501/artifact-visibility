Artifact Visibility 1.1.1 by Expand
===================================

Artefacts lying in the world are always visible, like in Shadow of Chernobyl: no detector needed to see them.
Glow light, idle particles and detector tiers are chosen in the installer.

Remake of "SoC-style Artefacts (DLTX)" by MaxSpringer: one mod with installer options instead of several
variants, covering G.A.M.M.A.'s own artefacts, junk artefacts, storyline artefacts and artefacts from other mods.

Features
- Artefacts always visible without a detector.
- Installer (Mod Organizer 2):
  - Detectors: "Keep detector tiers" (recommended; each detector still only finds the artefacts of its tier)
    or "Detectors find all artefacts".
  - "No glow light" and "No idle particles" (each optional).
- MCM: "Enable mod" (applies immediately) and a debug log.
- The mod never changes the game config while the game runs: the installer options are plain DLTX files,
  and a small script keeps artefacts visible.
- Performance: a tiny check per artefact every 2 seconds. Visible artefacts are drawn, so their glow light
  costs some GPU time near anomaly fields: "No glow light" saves it.

Requirements
- Anomaly 1.5.x with modded exes (DLTX), e.g. G.A.M.M.A. Also works on the Quark engine.
- MCM is optional (without it the mod is on and the debug log off).

Install
- Install the zip with Mod Organizer 2 and pick the options. To change them later, reinstall the mod.
- Remove/disable the old "SoC-style Artefacts (DLTX)" mod and all of its variants and patches
  (Main, No Lights, No Particles, Junkies, BAM).
- Can be installed or removed mid-playthrough. Installer options take effect after loading a save.
- The option files list 268 artefact sections. If an artefact mod in the list isn't installed, the game log
  shows a harmless "[DLTX] WARNING: Attemped to override section ..." line for each of its sections.

Settings (MCM -> Artifact Visibility)
- Enable mod: off = the game hides artefacts again a few seconds later, until a detector finds them.
  The installer options stay active.
- Debug log: writes which installer options are active to the game log on every save load.

Bug reports
Turn on "Debug log" in MCM, load a save, and send the [SoCArts] lines from <Anomaly folder>/appdata/logs/xray_*.log
together with the installer options you picked.

Version history
- 1.1.1: a dropped artefact no longer blinks (hidden, then shown again with the detector effect and sound).
  The installer options now cover 268 artefact sections (was 223): junk artefacts from Perk-Based Artefacts,
  Shadow of Chernobyl artefacts, DOGMA glowsticks and others kept their glow and particles. Reinstall to apply.
- 1.1.0: glow light, particles and detector tiers are now installer options (DLTX files); the mod no
  longer edits the game config while it runs. MCM keeps "Enable mod" (now applies immediately) and the debug log.
- 1.0.2: removed the "Artefacts always visible" MCM option: artefacts are always visible while the mod is enabled.
- 1.0.1: "Detectors keep their tiers" is now on by default.
- 1.0.0: first public release (version label only, no code changes).
- 0.3.0: renamed to "Artifact Visibility" (no functional changes).
- 0.2.0: new MCM option "Detectors keep their tiers".
- 0.1.0: first version.

Credits
- MaxSpringer: original idea and mod "SoC-style Artefacts (DLTX)".
- Expand: this remake.
