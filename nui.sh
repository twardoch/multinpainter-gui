#!/usr/bin/env bash
dir=${0%/*}
if [ "$dir" = "$0" ]; then dir="."; fi
cd "$dir" || exit

python3 -m nuitka --onefile --follow-imports --nofollow-import-to='IPython,unittest,setuptools_scm' src/multinpainter_gui/__main__.py