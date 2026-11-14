# Artifact Visibility by Expand

Goal: remake of "SoC-style Artefacts (DLTX)" v0.3 by MaxSpringer (archive: `D:\Gamma Files\Mods Archive\
SoCStyleArtefactsv0.3DLTX.rar`, all variants + readme) as one mod. Artefacts on the ground are always visible without
a detector. Since 1.1.0, glow light, idle particles and "detectors find all artefacts" are FOMOD installer options
(static DLTX files); the script only keeps artefacts visible. Shipped readmes: `src/README_EN.txt`,
`src/README_RU.txt` (cp1251).

## Files (FOMOD layout since 1.1.0)
- `src/fomod/info.xml`, `src/fomod/ModuleConfig.xml`: installer. Group "Detectors" (SelectExactlyOne: "Keep detector
  tiers" = no files, recommended / "Detectors find all artefacts" = `03`), group "Look" (SelectAny: `01`, `02`).
- `src/00 Main/gamedata/scripts/socart_main.script`: binder visibility keeper + MCM reading (log tag `[SoCArts]`).
- `src/00 Main/gamedata/scripts/socart_mcm.script`: MCM menu (id `socart`): `enabled`, `debug`. Defaults must match
  `DEFAULTS` in the main script.
- `src/00 Main/gamedata/configs/text/{eng,rus}/ui_st_socart_mcm.xml`: MCM strings (rus = Windows-1251).
- `src/01 No Glow Light`, `src/02 No Particles`, `src/03 Detectors Find All`: one
  `gamedata/configs/mod_system_zzzzzzzzzzzzzzzzzz_socart_<no_light|no_particles|rank0>.ltx` each. **Generated, don't
  edit by hand**: `tools/gen_sections.py` (not shipped). Regenerate when GAMMA or an artefact mod adds sections:
  `python -I tools/gen_sections.py --gamma F:/GAMMA --profile "G.A.M.M.A" --profile "<active profile>"
  --out <scratchpad>/sections.json --write-src src`. The section count also appears in the FOMOD description of
  "Detectors find all artefacts" (update it by hand).

## Version
`mod.json` `versionFiles`: both readme titles (+ history by hand), script header, both MCM text files (comment line),
both fomod xml files.

## Rule (Expand, 2026-11-14)
No runtime edits of `system_ini()` / engine state. 1.0.x did this (`w_string` in `on_game_start`); 1.1.0 removed it.
Any future idea that needs engine-state writes must be asked first (workspace CLAUDE.md, Stability rules).

## How it works (keep)
- Engine (xray-monolith and Quark `src/xrGame/Artefact.cpp`, same code): `CArtefact::Load` reads `af_rank`,
  `lights_enabled` (+ `trail_light_color/range` only when true) and `particles` from `pSettings` every time an
  artefact object comes online. `SArtefactDetectorsSupport::UpdateOnFrame` hides a visible artefact 5 s after the last
  `SetVisible` when `af_rank != 0`; with 0 it is never hidden. `CCustomDetector` skips artefacts with
  `af_rank > detector af_rank`, so rank 0 also removes detector tier limits. Detector support exists only when
  `can_be_controlled` is true (`CArtefact::net_Spawn`).
- Lua API of `CArtefact` (both engines): only `SwitchVisibility`, `GetAfRank`, `FollowByPath`, `ActivateArtefact`,
  `CanBeActivated` and some fields. No light or idle-particle switch. `game_object:stop_particles` only stops
  particles started by script (sender id 9999, the name argument is ignored), so it can't stop an artefact's idle
  particles. Hence installer options for light/particles.
- Visibility keeper: `item_artefact.artefact_binder.update` is wrapped in `on_game_start` (axr_main runs all
  top-level code first, so Perk-Based Artefacts' `zz_item_artefact` replacement is already in place and gets
  wrapped). While MCM `enabled`, every 2 s, for artefacts without parent and `GetAfRank() ~= 0`:
  `cast_Artefact():SwitchVisibility(true)`. `SetVisible` stores the time before its "already visible" early return,
  so on a visible artefact it only resets the 5 s hide timer. `CArtefact::shedule_Update` -> ... ->
  `CGameObject::shedule_Update` calls the script binder before `UpdateOnFrame` (hide check) in the same tick.
  Never call it in binder `net_spawn`: `CPhysicItem::net_Spawn` sets visible only after the binder's net_spawn, so
  the artefact is still invisible there (show particles + sound, second StartLights). All 223 sections found use
  `item_artefact.bind` (2026-11-14), so no rank-0 fallback is needed for tier mode.
- DLTX (xray-monolith `src/xrCore/Xr_ini.cpp`): overrides must use `![sec]` (merges keys, override wins per key;
  missing section = warning only). A plain duplicate `[sec]` is a fatal "Duplicate section" crash. Mod files of one
  root file load alphabetically, later override wins: our `zzzzzzzzzzzzzzzzzz` (18 z) sorts after GAMMA's
  `mod_system_zzzzzzzzzzzzzzzzz_grok_artifacts.ltx` (17 z, sets `af_rank = 2` on ~10 artefacts).
- Particles off = empty value `particles =` (DLTX stores NULL, `r_string` returns NULL, `m_sParticlesName` stays
  empty, `SwitchAfParticles` does nothing). Not `!particles`: a deleted key may fall back to a parent's value.
  No script in GAMMA reads `particles` of artefacts (checked 2026-11-14).
- Section list = every section with `af_rank` and `can_be_controlled = true` after DLTX merge and inheritance, from
  profiles `G.A.M.M.A` (211) and `v31.1 - radiation rework` (223; the 12 extra: mag pouches, side saddles,
  `af_grid_prototype`, monolith/prometheus container variants). Every section redefines `af_rank` itself, so a parent
  override would not cover children. Includes non-artefact `af_base` items (hides, `marker`, attachments), same
  as the 1.0.x runtime scan.

## Why the original failed (found 2026-11-14)
- Profile `v31.1 - radiation rework` had only variant 0.2 (`SoCStyleArtefacts_NoLights`, 44 sections). 33 more lit
  artefact sections exist (all junk artefacts from Perk-Based Artefacts, `af_ah_*`, `af_tlf_*`, `af_sun`,
  `af_lighthouse`, storyline / New Tasks artefacts): they kept light and stayed invisible.
- `G.A.M.M.A. Artefacts Reinvention` ships `mod_system_zzzzzzzzzzzzzzzzz_grok_artifacts.ltx`, loaded after
  `mod_system_soclikearts*` (alphabetical DLTX order), setting `af_rank = 2` for fireball, baloon, electra_flash,
  black_spray and others: those were hidden again. `[WIP] GAMMA Artefact Container Revamp` ships the same file name.
- The "No Lights" variant keeps idle particles, which look like glow on many artefacts.

## Profiles
- `v31.1 - radiation rework`: old `SoCStyleArtefacts_NoLights` enabled; must be disabled for this mod.
- `G.A.M.M.A` (base 0.9.5): old mod disabled; nothing to change.

## Open items
- 1.1.0 not tested in game: installer options (light/particles gone, rank 0 makes simple detectors find everything),
  MCM "Enable mod" off/on live, debug line in the log.
- Tier mode: check that low detectors ignore high-tier artefacts and no show effect/sound plays when artefacts come
  online or are dropped.
- GAMMA `dev2` (0.9.6) artefact sections not checked against the list.
