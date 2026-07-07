#!/usr/bin/env bash
# One-time project setup: pull the YOLOv5 submodule and install dependencies.
set -e

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

echo ">> Initializing the YOLOv5 submodule..."
git submodule update --init --recursive

echo ">> Installing project requirements..."
pip install -r requirements.txt

echo ">> Installing YOLOv5 requirements..."
pip install -r yolov5/requirements.txt

echo ">> Done. Try:  python vision/facedetection.py"
