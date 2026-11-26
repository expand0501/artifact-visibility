# Artifact Visibility: in-game test plan (`run.ps1 -Suite av`)

Runner: `tools\autotest\mod\gamedata\scripts\zzz_claude_autotest_av.script` (flag `-claudeav=`, log
`F:\Anomaly\appdata\logs\claude_autotest_av.log`). It tests the **installed zip unchanged**: the mod has no hooks for
tests; its locals (`ENABLED`, `DEBUG`, `DEFAULTS`, `REFRESH_MS`, `keeper_installed`, `base_update`, `on_option_change`)
are read through the upvalues of `socart_main.on_game_start` and `item_artefact.artefact_binder.update`.

## How it measures
- **Visibility**: `obj:cast_Artefact():getVisible()`. `CArtefact` derives from `CGameObject` in the Lua bindings
  (`artefact_script.cpp`), and `CGameObject` exports `getVisible` (`base_client_classes_script.cpp`). It returns
  `BOOL`, a number in Lua (0 = hidden). **verified in source**, not run yet.
- A sampler runs every frame for the artefacts the scenario spawned and records state changes (visible / hidden on
  the ground / offline or in an inventory) with `time_global()`, and **refreshes** = changes of the binder's
  `socart_next` field (`obj:binded_object()`).
- MCM values in memory (wrapper around `ui_mcm.get`), set by the runner's **top-level code**: the mod reads MCM in its
  `on_game_start`, which runs before the runner's (`axr_main`: every script's top-level code first, then the
  `on_game_start`s). Same for the capture of `[SoCArts]` lines (wrapped `printf`, matched on the formatted text).
- Expected values from the runner's own copies: `DEFAULTS` (`enabled = true`, `debug = false`), `REFRESH` 2000 ms,
  engine hide delay 5000 ms (`SArtefactDetectorsSupport::UpdateOnFrame`), slack 700 ms on timings.
- Test artefacts: the first of `af_medusa, af_blood, af_vaselisk, af_fireball, af_cristall, af_soul,
  af_electra_flash` with `af_rank > 0`, `can_be_controlled`, `item_artefact.bind`, `det_show_particles`. With the
  installer option "Detectors find all artefacts" (all ranks 0) the same list at rank 0. A rank-0 `af_*` section
  (if one exists) is added as a control in `visible_on` / `disabled`.

## Scenarios (one launch, save `claude_test`)

| Scenario | Setup | Proof | UNCLEAR when |
|---|---|---|---|
| `basics` | MCM debug on, no world | mod loaded, version 1.1.0 in the loaded script header, all internals readable, one socart wrapper in the binder chain (also after a second `on_game_start`), `base_update` not ours, `DEFAULTS` = runner's, settings read (`ENABLED`, `DEBUG` true), `REFRESH_MS` 2000 and below the hide delay, MCM menu (`id`, defaults = `DEFAULTS`, every string id resolves), eng/rus ids equal, rus cp1251, version comments; installer files found (log line), every `af_rank` + `can_be_controlled` section: installed options hold for all of them (`no_light_all`, `no_particles_all`, `rank0_all`) and each installed file lists every section (`*_file_covers`: catches a GAMMA / artefact mod update that needs `gen_sections.py`), ranked sections all use `item_artefact.bind`; debug line = values read from the config; detector ranks logged | no `[af_vaselisk]` (debug line) |
| `visible_on` | defaults, 3 artefacts (+ rank-0 control) 4-6 m away | never hidden for 16 s (3 hide windows), refresh gaps 1900-2700 ms, `ENABLED` true, no debug line | - |
| `disabled` | MCM "Enable mod" off from the load | **control for the method**: ranked artefacts are hidden from spawn + 7 s to the end (proves the sampler sees hiding), no `socart_next` set, rank-0 control stays visible | a detector is in the player's hands |
| `live_toggle` | defaults; MCM off then on with `SendScriptCallback("on_option_change", true)` (as `ui_mcm` does) | visible 6 s; off: `ENABLED` false at once, each artefact hidden 2.3-5.7 s after the toggle (5 s after its last refresh) and stays hidden; on: shown within 2.7 s, once, then never hidden | - |
| `drop` | 4 artefacts spawned in the inventory, carried 6 s, dropped 700 ms apart | first state on the ground visible, **no hide after the drop** (a hide + show = show particles and sound on every drop), visible at the end; log line per drop with the time to the next refresh | - |
| `no_mcm` | MCM values missing (`NIL`) | `ENABLED`/`DEBUG` = defaults; value false then `ui_mcm = false` while applying -> defaults again, no error; 2 artefacts kept visible 10 s with refreshes | - |
| `saveload` | 2 artefacts on the ground, `save claude_autotest`, load it | same ids and sections online after the load, keeper installed in the new script engine, never hidden from the first frame after the load, refreshes going | - |

`saveload` overwrites the save `claude_autotest` (meant for that). Nothing needs `-Isolated`, a real death or another level.

## `drop` history
Predicted from engine source and **confirmed in game on 1.1.0** (run `20261126-164620`): 4 of 4 dropped artefacts were
hidden 10-40 ms after the drop and shown again at the next refresh (show particles + sound). Fixed in 1.1.1 (the
refresh timer runs only on the ground). On 1.1.1 the `dropped ... next refresh due in N ms` lines show a negative N
(refresh overdue while carried), and `drop_no_hide_*` must PASS.

## Not automated (for Expand)
- Look: no glow light / no idle particles with the installer options (the config side is checked in `basics`).
- Sound / particles of a show, judged by eye and ear.
- Detector tiers: a low detector ignoring high-tier artefacts, and every detector finding everything with rank 0
  (engine behaviour; ranks are logged in `basics`).
- A real level change (covered by `saveload` in principle: every load builds new binders, **inference**).
- Profile `G.A.M.M.A` (base 0.9.5): run `basics` + `visible_on` there once before a release (own save, `-Isolated`).
