# Artifact Visibility by Expand

Goal: remake of "SoC-style Artefacts (DLTX)" v0.3 by MaxSpringer (archive: `D:\Gamma Files\Mods Archive\
SoCStyleArtefactsv0.3DLTX.rar`, all variants + readme) as one mod. Artefacts on the ground are always visible without
a detector; glow light and particles are MCM options instead of install variants. Shipped readmes:
`src/README_EN.txt`, `src/README_RU.txt` (cp1251).

## Files
- `src/gamedata/scripts/socart_main.script`: all logic, runs once per load in `on_game_start` (log tag `[SoCArts]`).
- `src/gamedata/scripts/socart_mcm.script`: MCM menu (id `socart`). Defaults must match `DEFAULTS` in the main script.
- `src/gamedata/configs/mod_system_socart.ltx`: the empty `[socart_backup]` section (backup storage, see below).
- `src/gamedata/configs/text/{eng,rus}/ui_st_socart_mcm.xml`: MCM strings (rus = Windows-1251).

## Version
In `mod.json`, both readme titles + history, script header, both MCM text files (comment line).

## How it works (keep)
- Engine (xray-monolith and Quark `src/xrGame/Artefact.cpp`, same code): `CArtefact::Load` reads `af_rank`,
  `lights_enabled` (+ `trail_light_color/range` only when true) and `particles` from `pSettings` every time an
  artefact object comes online. `SArtefactDetectorsSupport::UpdateOnFrame` hides a visible artefact 5 s after the last
  `SetVisible` when `af_rank != 0`; with 0 it is never hidden. `CCustomDetector` skips artefacts with
  `af_rank > detector af_rank`, so rank 0 also removes detector tier limits (same as the original mod; said in the
  MCM hint and readme).
- `on_game_start` is called from `CALifeSimulator` right after `script_engine().init()` (which recreates the Lua
  state) and before A-Life loads: main thread, no artefact online yet. We edit `system_ini()` only there, never
  during gameplay (Quark rebuilds per-section lookup tables on every write; mid-game writes could race with worker
  threads). So MCM changes apply on the next load.
- Writes: `set_readonly(false)` + `set_override_names(true)`, `w_string` on existing lines only, then flags back.
  No section is created or removed: Quark stores sections by value in a vector, inserting one moves all of them.
  The backup section therefore ships in `mod_system_socart.ltx` and only gets lines added.
- Backup `[socart_backup]`: `<section> = <af_rank>|<lights_enabled raw or ->|<particles or ->`, `_ready = true` once
  filled. pSettings lives for the whole exe session, the Lua state doesn't, so later loads read originals from here.
  Light is recorded only when it was on (only those sections have `trail_light_*`).
- Particles off = empty value (`r_string` returns NULL, engine loads no particles). No script in GAMMA reads
  `particles` of artefacts (checked 2026-11-14).
- Artefact sections = any section with `af_rank` and `can_be_controlled` (scan with `section_for_each` on the first
  load of the session only).

- Detector tier mode (MCM `tiers`, 0.2.0; on by default since 1.0.1): `af_rank` stays original; `item_artefact.artefact_binder.update` is
  wrapped in `on_game_start` (axr_main runs all top-level code first, so Perk-Based Artefacts' `zz_item_artefact`
  replacement is already in place and gets wrapped). Every 2 s, for artefacts without parent:
  `cast_Artefact():SwitchVisibility(true)`. `SetVisible` stores the time before its "already visible" early return,
  so on a visible artefact it only resets the 5 s hide timer. `CArtefact::shedule_Update` -> ... ->
  `CGameObject::shedule_Update` calls the script binder before `UpdateOnFrame` (hide check) in the same tick.
  Never call it in binder `net_spawn`: `CPhysicItem::net_Spawn` sets visible only after the binder's net_spawn, so
  the artefact is still invisible there (show particles + sound, second StartLights). Sections whose
  `script_binding` isn't `item_artefact.bind` get rank 0 in this mode.
- The config reads in `CArtefact::Load` happen with or without this mod (on spawn only, never per frame).

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
- Not tested in game yet (0.2.0).
- Tier mode untested: check that low detectors ignore high-tier artefacts and no show effect/sound plays when
  artefacts come online or are dropped.
