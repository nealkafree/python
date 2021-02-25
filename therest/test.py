import json
import os
import re

from googleapiclient.discovery import build
from tqdm import tqdm

BANNED = {'sm', 'smoon', 'gas', 'fake', 'night', 'sc', 'se', 'n', 'smon'}


def take_n_unique(dataset, n):
    viewed = {}
    result = {}
    regexp = re.compile(r'(.+)_\d+_\d+')
    for key, value in dataset.items():
        video_id = regexp.match(key).group(1)
        if video_id not in viewed:
            viewed[video_id] = 1
            result[key] = value
        elif viewed[video_id] < n:
            viewed[video_id] += 1
            result[key] = value
    return result


def check_comment(obj, banned):
    if 'comment' in obj:
        tags = {tag.strip(',') for tag in obj['comment'].split()}
        return tags.isdisjoint(banned)
    else:
        return True


# 17 22 24 27 28 25 23
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# API_KEY = 'AIzaSyDerq5DRTqKetXwepR2zYwzW9os1MAhziA'
#
# youtube = build('youtube', 'v3', developerKey=API_KEY)
#
# video_ids = set()
# regexp = re.compile(r'.+embed/(.+)\?.*')
# with open('double_table', 'r') as file:
#     for video in json.load(file):
#         video_ids.add(regexp.match(video[8]).group(1))
#
# category_ids = {}
# for video_id in tqdm(video_ids):
#     results = youtube.videos().list(id=video_id, part='snippet').execute()
#     category_id = results["items"][0]["snippet"]["categoryId"]
#     if category_id in category_ids:
#         category_ids[category_id] += 1
#     else:
#         category_ids[category_id] = 1
#
# print(category_ids)

# with open('gunshot_data') as file:
#     groups = json.load(file)
#
# groups = {key: value for key, value in groups.items() if value['gunshot'] == 'TRUE' and check_comment(value, BANNED)}
#
# with open('gunshot_data_sorted', 'w') as file:
#     json.dump(groups, file, indent=4)

with open('gunshot_data_sorted') as file:
    data = json.load(file)

print('gunshots: ' + str(len(data)))
with_target = {key: value for key, value in data.items() if value['sound_from_target'] == 'TRUE'}
print('with_target: ' + str(len(with_target)))
without_target = {key: value for key, value in data.items() if value['sound_from_target'] != 'TRUE'}
print('without_target: ' + str(len(without_target)))
with_speech = {key: value for key, value in data.items() if value['speech'] == 'TRUE'}
print('with_speech: ' + str(len(with_speech)))
data_2 = take_n_unique(data, 2)
print('doubles: ' + str(len(data_2)))
data_1 = take_n_unique(data, 1)
print('singles: ' + str(len(data_1)))
