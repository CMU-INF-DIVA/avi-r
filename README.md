# DIVA IO Package

Version 0.1

Author: Lijun Yu

Email: lijun@lj-y.com

## Video Loader

A robust video loader that deals with missing frames in the MEVA dataset.

### Usage

#### Replace `cv2.VideoCapture`

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

#### Iterator Interface

```python
video = VideoReader(video_path)
for frame in video:
    # frame is a diva_io.video.frame.Frame object
    image = frame.numpy() 
    # image is an uint8 array shape (height, width, channel[bgr])
```

#### Other Interfaces

For other usages, please see the comments in `diva_io.video.reader.py`.