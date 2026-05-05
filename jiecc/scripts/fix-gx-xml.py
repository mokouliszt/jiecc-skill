#!/usr/bin/env python3
"""
fix-gx-xml.py
Post-process jiecc-generated IEC 61131-10 XML for GX Works3 import.

Known GX Works3 XML import incompatibilities handled:
  1. <Task> element inside <Resource> is unreadable by GX Works3.
     Fix: remove all <Task ...> elements.
  2. associatedTaskName attribute in <ProgramInstance> references a removed Task.
     Fix: remove associatedTaskName attributes from all <ProgramInstance> elements.
  3. Mitsubishi MotionControl library FB type names use '+' separator in GX Works3
     (e.g. MC_Power+RD77) but jiecc source uses '_' (MC_Power_RD77).
     Fix: convert <TypeName> content for MC_*/MCv_* types with library suffix.
     Affected suffixes: _RD77  _RD77GF  _RD77MS  _J4GFIO

Usage:
  python fix-gx-xml.py input.xml              # patch in-place
  python fix-gx-xml.py input.xml -o out.xml   # write to new file
  python fix-gx-xml.py *.xml                  # batch (in-place)
"""

import re
import sys
import shutil
import argparse
from pathlib import Path


# ── fix 1/2: Task element and associatedTaskName ────────────────────────────

# Self-closing <Task .../> on its own line (optional leading whitespace)
_RE_TASK = re.compile(r'[ \t]*<Task\b[^>]*/>\r?\n?')

# associatedTaskName="..." attribute inside any element
_RE_ASSOC = re.compile(r'\s+associatedTaskName="[^"]*"')


# ── fix 3: MotionControl library FB type name format ────────────────────────
#
# GX Works3 internal name: MC_Power+RD77  (plus as module separator)
# jiecc source/XML name:   MC_Power_RD77  (underscore — valid IEC identifier)
#
# Rule: within <TypeName>...</TypeName>, replace the last '_' with '+' when
#       the type name matches  MCv?_<BaseName>_<LibSuffix>
#       LibSuffix in: RD77GF  RD77MS  RD77  J4GFIO   (order: longest first)
#
# Safe guard: pattern requires MC_ or MCv_ prefix, so AXIS_REF, AXIS_REF_J4GF,
#             TON, and other non-MC types are not affected.
#
_RE_LIB_FB = re.compile(
    r'(<TypeName>)(MCv?_\w+?)_(RD77GF|RD77MS|RD77|J4GFIO)(</TypeName>)'
)


def patch(text):
    # Fix 1: remove <Task> elements
    task_count = len(_RE_TASK.findall(text))
    text = _RE_TASK.sub('', text)

    # Fix 2: remove associatedTaskName attributes
    assoc_count = len(_RE_ASSOC.findall(text))
    text = _RE_ASSOC.sub('', text)

    # Fix 3: convert MC_*_RD77 -> MC_*+RD77 inside <TypeName> only
    lib_fb_count = len(_RE_LIB_FB.findall(text))
    text = _RE_LIB_FB.sub(r'\1\2+\3\4', text)

    return text, task_count, assoc_count, lib_fb_count


def process_file(path, out_path):
    raw = Path(path).read_text(encoding='utf-8')
    fixed, tasks, assocs, lib_fbs = patch(raw)
    changed = fixed != raw
    if changed:
        parts = []
        if tasks:    parts.append(f'{tasks} <Task>')
        if assocs:   parts.append(f'{assocs} associatedTaskName')
        if lib_fbs:  parts.append(f'{lib_fbs} MC_*_Lib -> MC_*+Lib')
        print(f'  {Path(path).name}: fixed {", ".join(parts)}')
        Path(out_path).write_text(fixed, encoding='utf-8')
    else:
        print(f'  {Path(path).name}: nothing to change')
        if str(out_path) != str(path):
            shutil.copy(path, out_path)
    return changed


def main():
    ap = argparse.ArgumentParser(
        description='Fix GX Works3 XML import incompatibilities in jiecc output')
    ap.add_argument('inputs', nargs='+', help='Input XML file(s)')
    ap.add_argument('-o', '--output',
                    help='Output file (only valid when a single input is given)')
    args = ap.parse_args()

    if args.output and len(args.inputs) > 1:
        ap.error('-o / --output can only be used with a single input file')

    any_changed = False
    for src in args.inputs:
        out = args.output or src
        any_changed |= process_file(src, out)

    print('[OK] Done.' if any_changed else '[OK] All files already clean.')


if __name__ == '__main__':
    main()
