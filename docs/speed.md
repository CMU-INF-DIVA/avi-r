# Speed of diva_io.video.VideoReader

## Test Results

Test performed by `speed_test()` in [video/test.py](../video/test.py).

| Video Name | Video Description | `diva_io.video .VideoReader (fix_missing=True)` | `diva_io.video .VideoReader (fix_missing=False)` | `pymovie.editor .VideoFileClip` |
|------------------------------------------------|---------------------------------------------------------|-------------------------------------------------|--------------------------------------------------|---------------------------------|
| 2018-03-11.16-30-08.16-35-08.hospital.G436.avi | No missing | 0:54 | 0:46 | 0:57 |
| 2018-03-07.16-55-06.17-00-06.school.G336.avi | Missing 104-109, 2294 | 1:06 | 0:56 | 0:56 |
| 2018-03-11.11-25-01.11-30-01.school.G424.avi | Missing 7391-7499 | 0:45 | 0:39 | 0:58 |
| 2018-03-11.16-25-00.16-30-00.school.G639.avi | Bidirectional frames, missing 1, 4 | 0:56 | 0:56 | 0:57 |
| 2018-03-11.11-35-00.11-40-00.school.G299.avi | Packet id and frame id unsychronized, missing 5789-5797 | 0:51 | 0:50 | 0:56 |
| 2018-03-11.11-35-00.11-40-00.school.G330.avi | Packet id and frame id unsychronized, missing 5755-5761 | 0:51 | 0:49 | 0:56 |
| 2018-03-12.10-05-00.10-10-00.hospital.G436.avi | First packet fail | 0:43 | 0:41 | 0:58 |
| Total (include overhead) |  | 6:11 | 5:41 | 6:42 |
| Relative (include overhead) |  | 100% | 91.9% | 108.3% |
| CPU Utilization |  | ~110% | ~110% | ~320% |
