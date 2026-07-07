# Third-Party Notices

This project bundles or depends on the following third-party components. Their
respective licenses apply to those files.

| Component | Location | License | Source |
|---|---|---|---|
| **Ultralytics YOLOv5** | `yolov5/` (git submodule) and `classification/{predict,train,val}.py` | **AGPL-3.0** | https://github.com/ultralytics/yolov5 |
| **OpenCV Haar cascade** (`haarcascade_frontalface_default.xml`) | `models/` | BSD-3-Clause (OpenCV) | https://github.com/opencv/opencv |
| **cvzone** `FaceDetectionModule` | used by `vision/facetracking.py` | MIT | https://github.com/cvzone/cvzone |

## Notes on the YOLOv5 files

`classification/predict.py`, `classification/train.py` and `classification/val.py`
are derived from the Ultralytics YOLOv5 `classify/` scripts and retain their
original **AGPL-3.0** headers. They import the rest of the framework from the
`yolov5/` git submodule. Because AGPL-3.0 is copyleft, any distribution or
network-served use that includes these files must comply with AGPL-3.0.

The original vision/hardware code in this repository (`vision/`, `hardware/`)
was written for this project; choose and add a top-level `LICENSE` for it that
is compatible with the AGPL-3.0 obligations above.
