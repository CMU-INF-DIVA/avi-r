# Speed of avi_r.AVIReader

Test performed by [tests/speed_test.sh](../tests/speed_test.sh).

```sh
./tests/speed_test.sh <video_dir> | tee log.txt
```

## Test Environment

- CPU: Intel Core i9-9900X
- Memory: 128GB
- Disk: SSD
- avi-r: 1.3.8
- moviepy: 1.0.3
- opencv: 4.4.0
- ffmpeg: 4.3

## Overall Performance

Loading all frames of 7 videos from the [MEVA dataset](http://mevadata.org). Each video is 5-min long and 1080p at 30 fps.

|                 | `avi_r.AVIReader` | `moviepy.editor.VideoFileClip` | `cv2.VideoCapture` |
| :-------------: | :---------------: | :----------------------------: | :----------------: |
|    User Time    |      245.63s      |            868.50s             |      712.73s       |
|   System Time   |       0.98s       |            270.87s             |       11.47s       |
| CPU Utilization |        97%        |              296%              |        515%        |
|   Total Time    |      253.67s      |            263.92s             |      140.55s       |

## Detailed Results

Loading time and number of frames on each video.

|                   Video Name                   |                    Video Description                    | `avi_r.AVIReader` | `moviepy.editor .VideoFileClip` | `cv2.VideoCapture` |
| :--------------------------------------------: | :-----------------------------------------------------: | :---------------: | :-----------------------------: | :----------------: |
| 2018-03-11.16-30-08.16-35-08.hospital.G436.avi |                       No missing                        |    0:32 / 9000    |           0:56 / 9000           |    0:13 / 9000     |
|  2018-03-07.16-55-06.17-00-06.school.G336.avi  |                  Missing 104-109, 2294                  |    0:49 / 9007    |           0:55 / 9007           |  0:13  / **9000**  |
|  2018-03-11.11-25-01.11-30-01.school.G424.avi  |                    Missing 7391-7499                    |    0:26 / 9000    |           0:54 / 9000           |    0:12  / 9000    |
|  2018-03-11.16-25-00.16-30-00.school.G639.avi  |           Bidirectional frames, missing 1, 4            |    0:42 / 9002    |           0:55 / 9002           |  0:54 / **9000**   |
|  2018-03-11.11-35-00.11-40-00.school.G299.avi  | Packet id and frame id unsychronized, missing 5789-5797 |    0:37 / 9009    |           0:55 / 9009           |  0:18 / **9000**   |
|  2018-03-11.11-35-00.11-40-00.school.G330.avi  | Packet id and frame id unsychronized, missing 5755-5761 |    0:38 / 9007    |           0:56 / 9007           |  0:17 / **9000**   |
| 2018-03-12.10-05-00.10-10-00.hospital.G436.avi |                    First packet fail                    |    0:30 / 9000    |           0:54 / 9000           |    0:13 / 9000     |
