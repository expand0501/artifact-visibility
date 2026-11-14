# Changelog - Artifact Visibility by Expand

- 1.0.2: removed the MCM option "Artefacts always visible": the mod's whole point is that artefacts are visible, so
  they always are while "Enable mod" is on. Old saved values of that option are ignored.
- 1.0.1: MCM option "Detectors keep their tiers" is now on by default (script defaults table and MCM default). Players
  who saved MCM values keep their choice.
- 1.0.0: first public release. Version label only, no code changes.
- 0.3.0: renamed from "SoC-Style Artefacts Remake" to "Artifact Visibility" (mod name, MCM menu, readmes, zip
  name). No functional changes; MCM id `socart`, file names and the `[SoCArts]` log tag are unchanged, so settings
  and saves carry over. Disable the old-named 0.2.0 install in MO2 when installing this one.
- 0.2.0: new MCM option "Detectors keep their tiers" (off by default). Artefacts stay visible, but `af_rank`
  keeps its original value, so each detector only finds the artefacts of its tier, as in normal GAMMA. The
  artefact binder re-sends "visible" every 2 s to artefacts lying in the world so the engine never hides them
  (resets the engine's 5 s timer only, no effect or sound). Artefacts with another script binder fall back to
  rank 0.
- 0.1.0: first version. Remake of "SoC-style Artefacts (DLTX)" by MaxSpringer as one mod. Artefacts on the
  ground are always visible without a detector; glow light and idle particles have MCM switches (plus master
  switch and debug log). Instead of a fixed DLTX list, the script finds every artefact section when the game loads
  and edits `af_rank` / `lights_enabled` / `particles` in the loaded config, so all GAMMA, junk, storyline and
  other mods' artefacts are covered and GAMMA's later `mod_system_zzz..._grok_artifacts.ltx` can no longer undo it.
  Settings apply on the next save load; nothing runs during gameplay.
