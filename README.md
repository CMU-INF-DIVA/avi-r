# MEVA IO Package

Version 1.0

Author: Lijun Yu

Email: lijun@lj-y.com

A robust reader for AVI video files.
Originally designed for the [MEVA](http://mevadata.org) dataset.

## Installation

```sh
pip install robust_avi
```

## Usage

A robust video loader that deals with missing frames in the [MEVA dataset](http://mevadata.org).

This video loader is developed based on [`PyAV`](https://github.com/mikeboers/PyAV) package.
The [`pims`](https://github.com/soft-matter/pims) package was also a good reference despite its compatibility issue with current `PyAV`.

For the videos in the MEVA, using `cv2.VideoCapture` would result in wrong frame ids as it never counts the missing frames.
If you are using MEVA, I suggest you change to this video loader ASAP.

### Replace `cv2.VideoCapture`

According to my test, this video loader returns the exact same frame as `cv2.VideoCapture` unless missing frame or decoding error occured.
To replace the `cv2.VideoCapture` objects in legacy codes, simply change from

```python
import cv2
cap = cv2.VideoCapture(video_path)
```

to

```python
from diva_io.video import VideoReader
cap = VideoReader(video_path)
```

`VideoReader.read` follows the schema of `cv2.VideoCapture.read` but automatically inserts the missing frames while reading the video.

### Iterator Interface

```python
video = VideoReader(video_path)
for frame in video:
    # frame is a diva_io.video.frame.Frame object
    image = frame.numpy()
    # image is an uint8 array in a shape of (height, width, channel[BGR])
    # ... Do something with the image
```

### Random Access

Random access of a frame requires decoding from the nearest key frame (approximately every 60 frames for MEVA).
Averagely, this introduces a constant overhead of 0.1 seconds, which is much faster than iterating from the beginning.

```python
start_frame_id = 1500
length = 100
video.seek(start_frame_id)
for frame in video.get_iter(length):
    image = frame.numpy()
    # ... Do something with the image
```

### Video Properties

```python
video.width # cap.get(cv2.CAP_PROP_FRAME_WIDTH)
video.height # cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
video.fps # cap.get(cv2.CAP_PROP_FPS)
video.length # cap.get(cv2.CAP_PROP_FRAME_COUNT)
```

### Other Interfaces

For other usages, please see the comments in [video/reader.py](video/reader.py).

### Speed

See [speed.md](docs/speed.md).
