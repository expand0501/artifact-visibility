"""
Artifact Visibility - artefact section list generator (not shipped).

Builds the MO2 virtual configs folder of one or more profiles (loose files only: vanilla .db archives are not read;
GAMMA replaces vanilla items_artefacts.ltx with Perk-Based Artefacts' copy), parses every .ltx below
gamedata/configs with DLTX rules (base [sec]:parents, overrides ![sec] / @[sec], key delete !key), resolves
inheritance and lists every section that ends up with af_rank and can_be_controlled = true - the rule the engine uses to give an
artefact detector support (CArtefact::net_Spawn).

Usage (read-only on the GAMMA folder):
  python -I gen_sections.py --gamma F:/GAMMA --profile "G.A.M.M.A" --profile "v31.1 - radiation rework" \
      --out sections.json --write-src ../src
--write-src writes the three DLTX option files into the FOMOD option folders (CRLF, ASCII).
Output: JSON {section: {"profiles": [...], "binding": str|None, "lights": bool, "particles": bool, "rank": str}}
"""
import argparse
import json
import os
import re
import sys

HDR = re.compile(r'^(!!|!|@)?\[([^\]]+)\]\s*(?::\s*(.*))?$')


def read_modlist(gamma, profile):
    path = os.path.join(gamma, "profiles", profile, "modlist.txt")
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = [l.rstrip("\r\n") for l in f]
    # top of the file = highest priority; return lowest priority first
    mods = [l[1:] for l in lines if l.startswith("+") and not l.endswith("_separator")]
    mods.reverse()
    return mods


def virtual_configs(gamma, mods):
    """relative path (lower case) -> (real path, mod) of the winning file"""
    tree = {}
    for mod in mods:
        root = os.path.join(gamma, "mods", mod, "gamedata", "configs")
        if not os.path.isdir(root):
            continue
        for dp, _, files in os.walk(root):
            for fn in files:
                if not fn.lower().endswith(".ltx"):
                    continue
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, root).replace("\\", "/").lower()
                tree[rel] = (full, mod)
    return tree


def strip_comment(line):
    for mark in (";", "//"):
        i = line.find(mark)
        if i >= 0:
            line = line[:i]
    return line.strip()


def parse_file(path):
    """yield (kind, name, parents, items) with kind in base/override/delete"""
    with open(path, "rb") as f:
        text = f.read().decode("cp1251", errors="replace")
    cur = None
    for raw in text.splitlines():
        line = strip_comment(raw)
        if not line or line.startswith("#include"):
            continue
        m = HDR.match(line)
        if m:
            if cur:
                yield cur
            prefix, name, parents = m.group(1), m.group(2).strip().lower(), m.group(3)
            kind = {"!!": "delete", "!": "override", "@": "override"}.get(prefix, "base")
            plist = [p.strip().lower() for p in parents.split(",")] if parents else []
            cur = (kind, name, plist, {})
            continue
        if cur is None:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip().lower(), val.strip()
        if key.startswith("!"):
            cur[3][key[1:]] = None          # DLTX delete
        elif key:
            cur[3][key] = val
    if cur:
        yield cur


def build(tree):
    base, overrides, deleted = {}, [], set()
    # mod_*.ltx files are loaded alphabetically after their root file; sort so overrides apply in that order
    for rel in sorted(tree, key=lambda r: (os.path.basename(r).startswith("mod_"), r)):
        for kind, name, parents, items in parse_file(tree[rel][0]):
            if kind == "base":
                base[name] = {"parents": parents, "items": dict(items)}
            elif kind == "override":
                overrides.append((name, parents, items))
            else:
                deleted.add(name)
    for name, parents, items in overrides:
        sec = base.get(name)
        if sec is None:
            continue                        # DLTX only warns; @[sec] creation ignored here
        if parents:
            sec["parents"] = [p for p in parents if not p.startswith("!")]
        for k, v in items.items():
            if v is None:
                sec["items"].pop(k, None)
            else:
                sec["items"][k] = v
    for name in deleted:
        base.pop(name, None)
    return base


def resolve(base, name, seen=None):
    seen = seen or set()
    if name in seen or name not in base:
        return {}
    seen.add(name)
    out = {}
    for p in base[name]["parents"]:
        out.update(resolve(base, p, seen))
    out.update(base[name]["items"])
    return out


# Name sorts after GAMMA's mod_system_zzzzzzzzzzzzzzzzz_grok_artifacts.ltx (17 z): DLTX loads mod files of one root
# file alphabetically and the last override of a key wins.
PREFIX = "mod_system_zzzzzzzzzzzzzzzzzz_socart_"
OPTIONS = [
    ("01 No Glow Light", "no_light", "lights_enabled = false",
     "No glow light: artefacts lying in the world cast no dynamic light."),
    ("02 No Particles", "no_particles", "particles =",
     "No idle particles: empty value, the engine loads no idle particle effect for these artefacts."),
    ("03 Detectors Find All", "rank0", "af_rank = 0",
     "Detectors find all artefacts: rank 0 = the engine never hides the artefact and every detector finds it."),
]


def write_dltx(src, sections, profiles):
    for folder, name, line, about in OPTIONS:
        d = os.path.join(src, folder, "gamedata", "configs")
        os.makedirs(d, exist_ok=True)
        out = [
            "; Artifact Visibility by Expand - installer option",
            "; " + about,
            "; Generated by tools/gen_sections.py (mod repository) from base G.A.M.M.A and the author's mod list:",
            "; every section with af_rank and can_be_controlled = true (%d sections)." % len(sections),
            "; Sections of artefact mods that aren't installed only cause a harmless DLTX warning in the log.",
            "",
        ]
        for sec in sections:
            out += ["![%s]" % sec, line, ""]
        with open(os.path.join(d, PREFIX + name + ".ltx"), "w", encoding="ascii", newline="\r\n") as f:
            f.write("\n".join(out))
        print(f"wrote {folder}: {len(sections)} sections", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gamma", required=True)
    ap.add_argument("--profile", action="append", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--write-src")
    a = ap.parse_args()

    result = {}
    for prof in a.profile:
        base = build(virtual_configs(a.gamma, read_modlist(a.gamma, prof)))
        n = 0
        for name in base:
            r = resolve(base, name)
            if "af_rank" in r and r.get("can_be_controlled", "").lower() in ("true", "on", "yes", "1"):
                e = result.setdefault(name, {"profiles": []})
                e["profiles"].append(prof)
                e["binding"] = r.get("script_binding")
                e["lights"] = r.get("lights_enabled", "").lower() in ("true", "on", "yes", "1")
                e["particles"] = bool(r.get("particles"))
                e["rank"] = r.get("af_rank")
                n += 1
        print(f"{prof}: {n} artefact sections", file=sys.stderr)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(result.items())), f, indent=1)
    print(f"total: {len(result)} -> {a.out}", file=sys.stderr)
    if a.write_src:
        write_dltx(a.write_src, sorted(result), a.profile)


if __name__ == "__main__":
    main()
