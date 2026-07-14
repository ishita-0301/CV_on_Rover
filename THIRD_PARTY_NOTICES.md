# Third-Party Notices

This project bundles or depends on the following third-party components. Their
respective licenses apply to those files.

| Component | Location | License | Source |
|---|---|---|---|
| **Ultralytics YOLOv5** | `yolov5/` (git submodule) and `experiments/classification/{predict,train,val}.py` | **AGPL-3.0** | https://github.com/ultralytics/yolov5 |
| **OpenCV Haar cascade** (`haarcascade_frontalface_default.xml`) | `experiments/models/` | BSD-3-Clause (OpenCV) | https://github.com/opencv/opencv |
| **cvzone** `FaceDetectionModule` | used by `experiments/face_tracking.py` | MIT | https://github.com/cvzone/cvzone |

## Notes on the YOLOv5 files

`experiments/classification/{predict,train,val}.py` are derived from the
Ultralytics YOLOv5 `classify/` scripts and retain their original **AGPL-3.0**
headers. They import the rest of the framework from the `yolov5/` git submodule.
Because AGPL-3.0 is copyleft, any distribution or network-served use that
includes these files must comply with AGPL-3.0. They live under `experiments/`
and are not part of the rover application (`controller/`, `rover/`).

The rover application code (`controller/`, `rover/`) and the face scripts in
`experiments/` were written for this project; add a top-level `LICENSE` for them
that is compatible with the AGPL-3.0 obligations above.
