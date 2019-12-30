import yaml
import os.path as osp
from collections import defaultdict

FIELDS = ['activities', 'geom', 'types']


class KitwareAnnotation(object):

    def __init__(self, video_name, annotation_dir):
        self.video_name = video_name
        self.raw_data = self._load_raw_data(video_name, annotation_dir)
        self.annotation = 0

    def _split_meta(self, contents, key):
        meta = []
        i = 0
        while i < len(contents) and 'meta' in contents[i]:
            assert key not in contents[i]
            meta.append(contents[i]['meta'])
            i += 1
        data = [content[key] for content in contents[i:]]
        return meta, data

    def _load_raw_data(self, video_name, annotation_dir):
        raw_data = {'meta': {}}
        date, _, time = video_name.split('.')[:3]
        for field in FIELDS:
            with open(osp.join(annotation_dir, date, time[:2],
                               '%s.%s.yml' % (video_name, field))) as f:
                contents = yaml.load(f, Loader=yaml.FullLoader)
                key = field if field != 'activities' else 'act'
                raw_data['meta'][field], raw_data[field] = self._split_meta(
                    contents, key)
        objs = defaultdict(dict)
        for obj in raw_data['geom']:
            obj['g0'] = [int(x) for x in obj['g0'].split()]
            objs[obj['id1']][obj['ts0']] = obj
        for obj in raw_data['types']:
            objs[obj['id1']]['type'] = [*obj['cset3'].keys()][0]
        for act in raw_data['activities']:
            for actor in act.get('actors', []):
                obj = objs[actor['id1']]
                geoms = []
                for ts in actor['timespan']:
                    start, end = ts['tsr0']
                    for time in range(start, end + 1):
                        geoms.append(obj[time])
                actor['geoms'] = geoms
                actor['type'] = obj['type']
        return raw_data

    def get_activities_official(self):
        activities = []
        for act in self.raw_data['activities']:
            act_id = act['id2']
            act_type = [*act['act2'].keys()][0]
            start, end = act['timespan'][0]['tsr0']
            objects = []
            for actor_id, actor in act['actors'].items():
                bbox_history = {}
                for geom in actor['geom']:
                    frame_id = geom['ts0']
                    x1, y1, x2, y2 = [int(x) for x in geom['g0'].split()]
                    bbox_history[frame_id] = {
                        'presenceConf': 1,
                        'boundingBox': {'x': x1, 'y': y1, 'w': x2 - x1,
                                        'h': y2 - y1}}
                for frame_id in range(start, end + 1):
                    if frame_id not in bbox_history:
                        bbox_history[frame_id] = {}
                obj = {'objectType': 'Vehicle', 'objectID': actor_id,
                       'localization': {self.video_name: bbox_history}}
                objects.append(obj)
            activity = {
                'activity': act_type, 'activityID': act_id,
                'presenceConf': 1, 'alertFrame': start,
                'localization': {self.video_name: {start: 1, end + 1: 0}},
                'objects': objects}
            activities.append(activity)
        return activities


def get_reference(video_list, annotation_dir):
    activities = []
    for video_name in video_list:
        annotation = KitwareAnnotation(video_name, annotation_dir)
        activities.extend(annotation.get_activities_official())
    reference = {'filesProcessed': video_list, 'activities': activities}
    file_index = {video_name: {'framerate': 30.0, 'selected': {0: 1, 9000: 0}}
                  for video_name in video_list}
    return reference, file_index
