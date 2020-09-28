# AVI-R Package

[![PyPI version](https://badge.fury.io/py/avi-r.svg)](https://badge.fury.io/py/avi-r)
[![Downloads](https://pepy.tech/badge/avi-r)](https://pepy.tech/project/avi-r)
![Publish to PyPI](https://github.com/Lijun-Yu/avi-r/workflows/Publish%20to%20PyPI/badge.svg)
(formerly DIVA IO)

Author: Lijun Yu

Email: lijun@lj-y.com

A robust reader for AVI video files.
Originally designed for the [MEVA](http://mevadata.org) dataset to replace [OpenCV](https://opencv.org)'s `cv2.VideoCapture` in the [DIVA](https://www.iarpa.gov/index.php/research-programs/diva) project.

## Installation

```sh
pip install avi-r
```

## Usage

A robust video loader that deals with missing frames in [AVI](https://en.wikipedia.org/wiki/Audio_Video_Interleave) files.
In `AVI-R`, missing frames are automatically filled with the previous available frame, or the next available frame for the beginning of a video.
This ensures you are getting the correct frame ids and valid frame contents all the time.

In comparison, [OpenCV](https://opencv.org)'s `cv2.VideoCapture` would skip missing frames without warning, leading to wrong frame ids.
[Pims](https://github.com/soft-matter/pims) would return empty frames also without warning.
And [decord](https://github.com/dmlc/decord) would crash.

### Iterator Interface

```python
from avi_r import AVIReader
video = AVIReader(video_path) # or AVIReader(video_name, parent_dir)
for frame in video:
    # frame is a avi_r.frame.Frame object
    image = frame.numpy()
    # image is an uint8 array in a shape of (height, width, channel[BGR])
    # ... Do something with the image
video.close() # Release internal buffers
```

### Replace `cv2.VideoCapture`

To replace the `cv2.VideoCapture` objects in legacy codes, simply change from

```python
import cv2
cap = cv2.VideoCapture(video_path)
```

to

```python
from avi_r import AVIReader
cap = AVIReader(video_path)
```

`AVIReader.read` follows the schema of `cv2.VideoCapture.read` but automatically inserts the missing frames while reading the video.
`AVIReader.release` also follows `cv2.VideoCapture.release`.

### Random Access

Random access of a frame requires decoding from the nearest key frame (approximately every 60 frames for MEVA).
Averagely, this introduces a constant overhead of 0.1 seconds.
However, when the nearest key frame is missing, `AVIReader` will try to search a valid one till the beginning.

```python
start_frame_id = 1500
length = 100
video.seek(start_frame_id)
for frame in video.get_iter(length):
    image = frame.numpy()
    # ... Do something with the image
video.close()
```

### Video Properties

```python
video.num_frames # cap.get(cv2.CAP_PROP_FRAME_COUNT)
video.frame_rate # cap.get(cv2.CAP_PROP_FPS)
video.height # cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
video.width # cap.get(cv2.CAP_PROP_FRAME_WIDTH)
```

### Other Interfaces

For other usages, please see the comments in [reader.py](avi_r/reader.py).

## Speed

See [speed.md](docs/speed.md).

## Version History

See [version.md](docs/version.md).
