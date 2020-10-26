import os.path as osp
import sys
import time

from avi_r import AVIReader
from tqdm import tqdm

# Videos from the MEVA dataset (http://mevadata.org)
VIDEO_LIST = [
    '2018-03-11.16-30-08.16-35-08.hospital.G436.avi',  # no missing
    '2018-03-07.16-55-06.17-00-06.school.G336.avi',  # have missing
    '2018-03-11.11-25-01.11-30-01.school.G424.avi',
    '2018-03-11.16-25-00.16-30-00.school.G639.avi',  # bidirectional
    '2018-03-11.11-35-00.11-40-00.school.G299.avi',  # frame id misorder
    '2018-03-11.11-35-00.11-40-00.school.G330.avi',
    '2018-03-12.10-05-00.10-10-00.hospital.G436.avi',  # first frame fail
]


def integrity_test(video_dir, video_list=VIDEO_LIST,
                   random_access_point=(5790, 100)):
    print('Fix missing with random access')
    start_frame_id, length = random_access_point
    for video_name in video_list:
        print('\t video:', video_name, flush=True)
        start = time.time()
        v = AVIReader(video_name, video_dir)
        for i, f in tqdm(enumerate(v), total=v.num_frames):
            assert f.frame_id == i
        v = AVIReader(video_name, video_dir, silence_warning=False)
        v.seek(start_frame_id)
        for i, frame in tqdm(enumerate(v.get_iter(length))):
            assert frame.frame_id == start_frame_id + i
    print('No fix missing')
    for video_name in video_list:
        print('\t video:', video_name, flush=True)
        v = AVIReader(video_name, video_dir, fix_missing=False)
        for i, f in tqdm(enumerate(v), total=v.num_frames):
            pass


def speed_test_opencv(video_dir, video_list=VIDEO_LIST):
    import cv2
    for video_name in video_list:
        print('\t video:', video_name, flush=True)
        start = time.time()
        cap = cv2.VideoCapture(osp.join(video_dir, video_name))
        frame = 0
        for _ in tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
            r, _ = cap.read()
            if not r:
                break
            frame += 1
        total = time.time() - start
        print('\t frame:', frame)
        print('\t time:', total, flush=True)


def speed_test_moviepy(video_dir, video_list=VIDEO_LIST):
    from moviepy.editor import VideoFileClip
    for video_name in video_list:
        print('\t', video_name, flush=True)
        start = time.time()
        clip = VideoFileClip(osp.join(video_dir, video_name))
        frame = 0
        for i in tqdm(range(int(round(clip.duration * clip.fps)))):
            clip.get_frame(i / clip.fps)
            frame += 1
        total = time.time() - start
        print('\t frame:', frame)
        print('\t', total, flush=True)


def speed_test_avi_r(video_dir, video_list=VIDEO_LIST):
    for video_name in video_list:
        print('\t', video_name, flush=True)
        start = time.time()
        video = AVIReader(video_name, video_dir, silence_warning=False)
        frame = 0
        for _ in tqdm(range(video.length)):
            video.read()
            frame += 1
        total = time.time() - start
        print('\t frame:', frame)
        print('\t', total, flush=True)


if __name__ == "__main__":
    video_dir = sys.argv[1]
    integrity_test(video_dir)
