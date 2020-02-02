import sys
from progressbar import progressbar
from .reader import VideoReader


def test(video_list, video_dir, random_access_point=(5790, 100)):
    print('No fix missing')
    for video_name in video_list:
        print(video_name, flush=True)
        v = VideoReader(video_name, video_dir, fix_missing=False)
        for i, f in progressbar(enumerate(v)):
            pass

    print('Fix missing with random access')
    for video_name in video_list:
        print(video_name, flush=True)
        v = VideoReader(video_name, video_dir)
        for i, f in progressbar(enumerate(v)):
            assert f.frame_id == i
        start_frame_id, length = random_access_point
        v.seek(start_frame_id)
        for i, frame in progressbar(enumerate(v.get_iter(length))):
            assert frame.frame_id == start_frame_id + i


VIDEO_LIST = video_list = [
    '2018-03-11.16-30-08.16-35-08.hospital.G436.avi',  # no missing
    '2018-03-07.16-55-06.17-00-06.school.G336.avi',  # have missing
    '2018-03-11.11-25-01.11-30-01.school.G424.avi',
    '2018-03-11.16-25-00.16-30-00.school.G639.avi',  # bidirectional
    '2018-03-11.11-35-00.11-40-00.school.G299.avi',  # frame id misorder
    '2018-03-11.11-35-00.11-40-00.school.G330.avi',
    '2018-03-12.10-05-00.10-10-00.hospital.G436.avi'  # first frame fail
]


if __name__ == "__main__":
    test(VIDEO_LIST, sys.argv[1])
