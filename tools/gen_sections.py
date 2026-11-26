"""
Artifact Visibility - artefact section list generator (not shipped).

Builds the MO2 virtual configs folder of one or more profiles on top of the unpacked vanilla configs (--vanilla,
default reference/anomaly-1.5.3/configs: stands in for the .db archives, which hold e.g. items_artefacts_soc.ltx and
mp/weapons_mp/items_mp.ltx), parses the files the engine merges into system_ini (system.ltx and its #include tree,
then mod_system_*.ltx; since 1.1.1: other .ltx files are separate ini files and replaced real sections) with DLTX rules (base [sec]:parents, overrides ![sec] / @[sec], key delete !key), resolves
inheritance and lists every section that ends up with af_rank and can_be_controlled = true - the rule the engine uses to give an
artefact detector support (CArtefact::net_Spawn).

Usage (read-only on the GAMMA folder):
  python -I gen_sections.py --gamma F:/GAMMA --profile "G.A.M.M.A" --profile "v31.1 - radiation rework" \
      --out sections.json --write-src ../src
--write-src writes the three DLTX option files into the FOMOD option folders (CRLF, ASCII).
Output: JSON {section: {"profiles": [...], "binding": str|None, "lights": bool, "particles": bool, "rank": str}}
"""
import argparse
import fnmatch
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


def vanilla_configs(vanilla):
    """lowest layer: the unpacked vanilla configs (stand in for Anomaly's .db archives, which are not read)"""
    tree = {}
    if not vanilla or not os.path.isdir(vanilla):
        return tree
    for dp, _, files in os.walk(vanilla):
        for fn in files:
            if fn.lower().endswith(".ltx"):
                full = os.path.join(dp, fn)
                tree[os.path.relpath(full, vanilla).replace("\\", "/").lower()] = (full, "<vanilla>")
    return tree


INCLUDE = re.compile(r'^\s*#include\s+"([^"]+)"', re.I)


def reachable(tree):
    """files the engine loads into system_ini: system.ltx and its #include tree (wildcards too), then the DLTX
    mod_system_*.ltx files. Other .ltx files are separate ini files (e.g. grok_items_tier.ltx of the treasure
    manager) and must not be merged: their sections would replace the real ones."""
    order, seen = [], set()

    def visit(rel):
        if rel in seen or rel not in tree:
            return
        seen.add(rel)
        order.append(rel)
        d = os.path.dirname(rel)
        with open(tree[rel][0], "rb") as f:
            text = f.read().decode("cp1251", errors="replace")
        for line in text.splitlines():
            m = INCLUDE.match(line)
            if not m:
                continue
            pat = os.path.normpath(os.path.join(d, m.group(1).replace("\\", "/"))).replace("\\", "/").lower()
            for r in sorted(r for r in tree if fnmatch.fnmatch(r, pat)):
                visit(r)

    visit("system.ltx")
    order += sorted(r for r in tree if "/" not in r and r.startswith("mod_system_"))
    return {r: tree[r] for r in order}


def virtual_configs(gamma, mods, vanilla=None):
    """relative path (lower case) -> (real path, mod) of the winning file"""
    tree = vanilla_configs(vanilla)
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
    ap.add_argument("--vanilla", default=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "..", "..", "reference", "anomaly-1.5.3", "configs")),
                    help="unpacked vanilla Anomaly configs (default: the workspace's reference\\anomaly-1.5.3\\configs)")
    a = ap.parse_args()
    if not os.path.isfile(os.path.join(a.vanilla, "system.ltx")):
        sys.exit(f"no system.ltx in the vanilla configs folder {a.vanilla}")

    result = {}
    for prof in a.profile:
        base = build(reachable(virtual_configs(a.gamma, read_modlist(a.gamma, prof), a.vanilla)))
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
