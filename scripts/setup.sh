#!/usr/bin/env bash
# Project setup: install Python dependencies. Pass --experiments to also pull
# the YOLOv5 submodule used by the learning scripts in experiments/.
set -e

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

echo ">> Installing project requirements..."
pip install -r requirements.txt

if [ "$1" = "--experiments" ]; then
  echo ">> Initializing the YOLOv5 submodule (experiments/classification)..."
  git submodule update --init --recursive
  pip install -r yolov5/requirements.txt
fi

echo ">> Done."
echo "   Rover Pi:       python rover/main.py"
echo "   Controller Pi:  python controller/main.py   (set ROVER_HOST in controller/config.py first)"
