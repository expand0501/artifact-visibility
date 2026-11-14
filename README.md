# Artifact Visibility

A mod for **S.T.A.L.K.E.R. Anomaly G.A.M.M.A.** by Expand.

**[Download (Releases)](https://github.com/expand0501/soc-style-artefacts-remake/releases)** · [Русский](#русский)

Artefacts lying in the world are always visible, like in Shadow of Chernobyl: you don't need a detector to see them.
Their glow light and particles can be switched on or off in MCM. Remake of "SoC-style Artefacts (DLTX)" by
MaxSpringer: one mod instead of several install variants, covering every artefact in the game.

## Features

- Artefacts always visible without a detector.
- MCM: glow light on/off, particles on/off, detectors keep their tiers on/off, master switch, debug log.
- Works with every artefact mod: artefact sections are found automatically when the game loads.
- No cost during gameplay: the mod works once while a save loads (the detector tier mode adds a tiny
  check per artefact every 2 seconds).

## Installation (Mod Organizer 2)

1. Install the zip from [Releases](https://github.com/expand0501/soc-style-artefacts-remake/releases) as a new mod.
2. Disable the old "SoC-style Artefacts (DLTX)" mod and all its variants/patches.
3. Needs DLTX (part of the modded exes in G.A.M.M.A.). Also works on the Quark engine. MCM is optional.
4. Safe to add to or remove from an existing save. Settings apply after loading a save.

By default each detector beeps only for the artefacts of its tier, as in normal GAMMA (artefacts stay visible). Turn off
"Detectors keep their tiers" in MCM to make every detector find every artefact, as in the original mod.

## Bug reports

Turn on "Debug log" in MCM, load a save, and open an
[issue](https://github.com/expand0501/soc-style-artefacts-remake/issues) with the lines starting with `[SoCArts]`
from `Anomaly\appdata\logs\xray_*.log`.

## License

[CC BY-NC-SA 4.0](LICENSE). Idea and original mod: MaxSpringer.

---

## Русский

Артефакты в мире всегда видны, как в Тени Чернобыля: детектор, чтобы их увидеть, не нужен. Свечение и частицы
артефактов включаются и выключаются в MCM. Ремейк мода "SoC-style Artefacts (DLTX)" от MaxSpringer: один мод
вместо нескольких вариантов установки, работает со всеми артефактами игры.

- Установка: архив из [Releases](https://github.com/expand0501/soc-style-artefacts-remake/releases) через MO2;
  отключите старый "SoC-style Artefacts (DLTX)" со всеми вариантами. Нужен DLTX (есть в G.A.M.M.A.), MCM не обязателен.
- Можно ставить и удалять посреди прохождения. Настройки применяются после загрузки сохранения.
- По умолчанию каждый детектор находит только артефакты своего уровня, как в обычной GAMMA (артефакты при этом
  видны). Выключите "Детекторы со своим уровнем" в MCM, чтобы любой детектор находил любые артефакты, как в оригинале.
- Ошибки: включите "Журнал отладки" в MCM и пришлите строки `[SoCArts]` из `Anomaly\appdata\logs\xray_*.log`.
