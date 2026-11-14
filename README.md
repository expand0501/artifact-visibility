# Artifact Visibility

A mod for **S.T.A.L.K.E.R. Anomaly G.A.M.M.A.** by Expand.

**[Download (Releases)](https://github.com/expand0501/artifact-visibility/releases)** · [Русский](#русский)

Artefacts lying in the world are always visible, like in Shadow of Chernobyl: you don't need a detector to see them.
Glow light, particles and detector tiers are chosen in the installer. Remake of "SoC-style Artefacts (DLTX)" by
MaxSpringer: one mod with installer options instead of several variants, covering G.A.M.M.A.'s artefacts and those of
common addons.

## Features

- Artefacts always visible without a detector.
- Installer options: "Keep detector tiers" (recommended) or "Detectors find all artefacts"; "No glow light" and
  "No idle particles".
- MCM: "Enable mod" (applies immediately) and a debug log.
- Never changes the game config while the game runs: the options are plain DLTX files, and a small script keeps
  artefacts from any mod visible (a tiny check per artefact every 2 seconds).

## Installation (Mod Organizer 2)

1. Install the zip from [Releases](https://github.com/expand0501/artifact-visibility/releases) as a new mod.
2. Disable the old "SoC-style Artefacts (DLTX)" mod and all its variants/patches.
3. Needs DLTX (part of the modded exes in G.A.M.M.A.). Also works on the Quark engine. MCM is optional.
4. Safe to add to or remove from an existing save. Installer options apply after loading a save; reinstall the mod
   to change them.

With "Keep detector tiers" each detector beeps only for the artefacts of its tier, as in normal GAMMA (artefacts stay
visible). Pick "Detectors find all artefacts" to make every detector find every artefact, as in the original mod.

## Bug reports

Turn on "Debug log" in MCM, load a save, and open an
[issue](https://github.com/expand0501/artifact-visibility/issues) with the lines starting with `[SoCArts]`
from `Anomaly\appdata\logs\xray_*.log` and the installer options you picked.

## License

[CC BY-NC-SA 4.0](LICENSE). Idea and original mod: MaxSpringer.

---

## Русский

Артефакты в мире всегда видны, как в Тени Чернобыля: детектор, чтобы их увидеть, не нужен. Свечение, частицы
и уровни детекторов выбираются в установщике. Ремейк мода "SoC-style Artefacts (DLTX)" от MaxSpringer: один мод с
опциями установщика вместо нескольких вариантов, работает с артефактами G.A.M.M.A. и популярных аддонов.

- Установка: архив из [Releases](https://github.com/expand0501/artifact-visibility/releases) через MO2;
  отключите старый "SoC-style Artefacts (DLTX)" со всеми вариантами. Нужен DLTX (есть в G.A.M.M.A.), MCM не обязателен.
- Опции установщика: "Keep detector tiers" (рекомендуется: каждый детектор находит только артефакты своего уровня,
  как в обычной GAMMA) или "Detectors find all artefacts" (любой детектор находит любые артефакты, как в оригинале);
  "No glow light" (без свечения) и "No idle particles" (без частиц). Чтобы изменить их, переустановите мод.
- В MCM: "Включить мод" (применяется сразу) и журнал отладки. Мод не меняет конфиг игры во время игры.
- Можно ставить и удалять посреди прохождения. Опции установщика применяются после загрузки сохранения.
- Ошибки: включите "Журнал отладки" в MCM и пришлите строки `[SoCArts]` из `Anomaly\appdata\logs\xray_*.log`
  и выбранные опции установщика.
