# DIVA IO Package

Version 0.1

Author: Lijun Yu

Email: lijun@lj-y.com

## Requirements

Environment requirements are listed in `environment.yml`.
For the `av` package, I recommend you install it via `conda` by 
```sh
conda install av -c conda-forge
```
as building from `pip` would require a lot of dependencies.

## Video Loader

A robust video loader that deals with missing frames in the [MEVA dataset](http://mevadata.org). 

This video loader is developed based on [`PyAV`](https://github.com/mikeboers/PyAV) package.
The [`pims`](https://github.com/soft-matter/pims) package was also a good reference despite its compatibility issue with current `PyAV`.

For the videos in the MEVA, using `cv2.VideoCapture` would result in wrong frame ids as it never counts the missing frames.
If you are using MEVA, I suggest you change to this video loader ASAP.

### Replace `cv2.VideoCapture`

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
    # image is an uint8 array shape (height, width, channel[bgr])
```

### Other Interfaces

For other usages, please see the comments in `diva_io/video/reader.py`.