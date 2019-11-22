import av
import numpy as np
import os.path as osp
from typing import Tuple

from ..utils import get_logger
from .frame import Frame


class VideoReader(object):

    def __init__(self, video_path: str, parent_dir: str = '',
                 fix_missing: bool = True):
        """Read frames from a video file.

        Parameters
        ----------
        video_path : str
            Path of the video file, will be joint with parent_dir if specified.

        parent_dir : str, optional
            Parent directory of the videos, convenient for path management, by 
            default ''.

        fix_missing : bool, optional
            Whether to fix missing frames.

        Raises
        ------
        FileNotFoundError
            If the video file to read does not exist.
        """
        self.path = osp.join(parent_dir, video_path)
        if not osp.exists(self.path):
            raise FileNotFoundError(self.path)
        self.logger = get_logger(__name__)
        self.fix_missing = fix_missing
        if not self.fix_missing:
            self.logger.warn('Not fixing missing frames.')
        self._init()
        stream = self._container.streams.video[0]
        self.length = stream.duration
        self.fps = float(1 / stream.time_base)

    def __iter__(self):
        """Iterator interface to use in a for-loop directly as:
        for frame in video:
            pass

        Yields
        -------
        Frame
            A Frame object.
        """
        if not self.reseted:
            self.reset()
        yield from self.get_iter()

    def get_iter(self, limit: int = None, cycle: int = 1) -> Frame:
        """Get an iterator to yield a frame every cycle frames and stop at a 
        limited number of yielded frames.

        Parameters
        ----------
        limit : int, optional
            Total number of frames to yield, by default None. If None, it 
            yields until the video ends.

        cycle : int, optional
            The cycle length for each read, by default 1. If cycle = 1, no 
            frames are skipped.

        Yields
        -------
        Frame
            A Frame object.
        """
        if limit is None or limit > self.length:
            limit = self.length
        for _ in range(limit):
            try:
                yield self.get_skip(cycle)
            except StopIteration:
                break

    def get_skip(self, cycle: int = 1) -> Frame:
        """Read a frame from the video every cycle frames. It returns the 
        immediate next frame and skips cycle - 1 frames for the next call of 
        get.

        Parameters
        ----------
        cycle : int, optional
            The cycle length for each read, by default 1. If cycle = 1, no 
            frames are skipped.

        Returns
        -------
        Frame
            A Frame object.

        Raises
        -------
        StopIteration
            When the video ends.
        """
        frame = self.get()
        try:
            for _ in range(cycle - 1):
                self.get()
        except StopIteration:  # will be raised in the next call of get
            pass
        return frame

    def get(self) -> Frame:
        """Read the next frame from the video.

        Returns
        -------
        Frame
            The frame object.

        Raises
        -------
        StopIteration
            When the video ends.
        """
        return next(self._generator)

    def read(self) -> Tuple[bool, np.ndarray]:
        """Read the next frame from the video. Following the API of 
        cv2.VideoCapture.read() for consistency in old codes. For new codes, 
        the get method is recommended.

        Returns
        -------
        bool
            True when the read is successful, False when the video ends.

        numpy.ndarray
            The frame when successful, with format bgr24, shape (height, width, 
            channel) and dtype int.
        """
        try:
            frame = next(self._generator)
        except StopIteration:
            frame = None
        return frame is not None, frame.numpy()

    def reset(self):
        """Reset the internal states to load the video from the beginning.
        """
        self._container.close()
        self._init()

    def _init(self):
        self._container = av.open(self.path)
        self._generator = self._get_generator()
        self.reseted = True

    def _decode(self):
        self.reseted = False
        for frame in self._container.decode():
            if isinstance(frame, av.VideoFrame):
                yield Frame(frame)

    def _get_generator(self):
        prev_frame = None
        inserted_count = 0
        for frame in self._decode():
            offset = 0
            while frame.frame_index_display > frame.frame_index_store + \
                    inserted_count + offset:
                offset += 1
                if offset == 1:
                    self.logger.warn(
                        'Frame loss encountered between frame %d and frame %d.',
                        prev_frame.frame_id, frame.frame_id)
                if self.fix_missing:
                    yield Frame(prev_frame.frame, offset)
            inserted_count += offset
            prev_frame = frame
            yield frame
