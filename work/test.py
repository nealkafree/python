import json

from tqdm import tqdm

import work.AssignmentDownloader as toloka
from work.toloka_api import TolokaAPI
import os

TOKEN = 'AQAAAAAl97zMAACtpRN7SJA0tUFtrnLNhmPYSdc'


def get_list_of_submitted_assignments(api, pool_id, status='SUBMITTED', datetime='2017-01-01T00:00:00'):
    last_id = None
    items = []
    has_more = True

    while has_more:
        if last_id:
            data = api.get_list_of_assignments({
                "sort": "id",
                "pool_id": pool_id,
                "id_gt": last_id,
                "submitted_gt": datetime}).json()
        else:
            data = api.get_list_of_assignments({
                "sort": "id",
                "pool_id": pool_id,
                "submitted_gt": datetime}).json()
        if 'items' in data:
            items = items + data["items"]
        has_more = data["has_more"]
        if items:
            last_id = items[-1]["id"]

    # submitted_items = []
    # for assignment in items:
    #     if assignment['status'] == status:
    #         submitted_items.append(assignment)
    #     if len(submitted_items) >= 200:
    #         break

    submitted_items = list(filter(lambda x: x["status"] == status, items))
    return submitted_items


api = TolokaAPI(TOKEN, sandbox=False)
projects = [('web_countries', 43163), ('web_south_africa', 37123), ('web_kenya', 37122), ('web_nigeria', 37121),
            ('web_philippines', 37116), ('web_india', 37115), ('web_vietnam', 37114), ('phone_countries', 42135),
            ('phone_south_africa', 36220), ('phone_kenya', 36219), ('phone_nigeria', 36217), ('phone_philippines', 36211),
            ('phone_india', 35628), ('phone_vietnam', 35420), ('web_russia', 39172), ('phone_45+', 33039)]
for project_name, project_id in projects:
    list_of_pools = [pool['id'] for pool in api.get_list_of_pools({'project_id': project_id}).json()['items']]
    done = 0
    for pool in list_of_pools:
        accepted = get_list_of_submitted_assignments(api, pool, status='ACCEPTED', datetime='2020-10-13T00:00:00')
        done += len(accepted)
    print(project_name)
    print(done)
