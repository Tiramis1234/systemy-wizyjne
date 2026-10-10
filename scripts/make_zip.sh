#!/usr/bin/env bash
# Builds the stage ZIP from the committed source code.
# git archive only takes tracked files, so .venv, node_modules, frontend/dist,
# __pycache__, .git and saved outputs are left out automatically.
# Usage: scripts/make_zip.sh 01   ->   Lenarczyk_Marek_Inf_Projekt01.zip
set -euo pipefail

stage="${1:?Usage: $0 <stage number, e.g. 01>}"
name="Lenarczyk_Marek_Inf_Projekt${stage}"

git archive --format=zip --prefix="${name}/" -o "${name}.zip" HEAD
echo "Created ${name}.zip"
