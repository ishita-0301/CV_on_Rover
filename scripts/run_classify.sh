#!/usr/bin/env bash
# Convenience wrapper for the YOLOv5 classification inference script.
#
# Usage:
#   scripts/run_classify.sh --weights yolov5s-cls.pt --source 0        # webcam
#   scripts/run_classify.sh --weights yolov5s-cls.pt --source img.jpg  # image
#
# Any extra arguments are passed straight through to classification/predict.py.
set -e

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -f "$repo_root/yolov5/models/common.py" ]; then
  echo "YOLOv5 submodule not found. Run: git submodule update --init --recursive" >&2
  exit 1
fi

python "$repo_root/classification/predict.py" "$@"
