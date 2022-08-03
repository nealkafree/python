import json

from tqdm import tqdm

from work.toloka_api import TolokaAPI
import os


def get_project_id(api, name):
    response = api.get_list_of_projects({'limit': 299}).json()
    if 'items' in response:
        projects_list = list(response['items'])
        project = list(filter(lambda x: True if x['public_name'] == name else False, projects_list))[0]
        return project['id']
    else:
        return None


def get_pool_id(api, pool_name, project_id):
    response = api.get_list_of_pools({"project_id": project_id}).json()
    if 'items' in response:
        pool_list = list(response['items'])
        pool = list(filter(lambda x: True if x['private_name'] == pool_name else False, pool_list))[0]
        return pool['id']
    else:
        return None


def get_list_of_submitted_assignments(api, pool_id, status='SUBMITTED', datetime='2017-01-01T00:00:00'):
    last_id = None
    items = []
    has_more = True

    while has_more:
        if last_id:
            date = api.get_list_of_assignments({
                "sort": "id",
                "pool_id": pool_id,
                "id_gt": last_id,
                "submitted_gt": datetime}).json()
        else:
            date = api.get_list_of_assignments({
                "sort": "id",
                "pool_id": pool_id,
                "submitted_gt": datetime}).json()

        items = items + date["items"]
        has_more = date["has_more"]
        if items:
            last_id = items[-1]["id"]

    # submitted_items = []
    # for assignment in items:
    #     if assignment['status'] == status:
    #         submitted_items.append(assignment)
    #     if len(submitted_items) >= 450:
    #         break
    submitted_items = list(filter(lambda x: x["status"] == status, items))
    return submitted_items


def read_json(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    else:
        return {}


def download_attachments(api, submitted_items, new_video_path, field_name):
    counter = 0
    for item in tqdm(submitted_items):
        attachment_id = item['solutions'][0]['output_values'][field_name]
        assignment_id = item['id']
        if attachment_id:
            os.makedirs(os.path.join(new_video_path, assignment_id), exist_ok=True)
            api.get_file(attachment_id, os.path.join(new_video_path, assignment_id))
            counter += 1
    return counter


def download_brk_files(pool_id, new_video_path, video_urls, field_name):

    api = TolokaAPI(TOKEN, sandbox=False)

    submitted_items = get_list_of_submitted_assignments(api, pool_id, status='SUBMITTED')
    print(len(submitted_items))
    if not os.path.exists(new_video_path):
        os.makedirs(new_video_path)

    attachment_num = download_attachments(api, submitted_items, new_video_path, video_urls, field_name)
    print('attachments_num:' + str(attachment_num))


# api = TolokaAPI(TOKEN, sandbox=False)
#
# project_id = get_project_id(api, 'Записать лай вашей собаки на видео')
# if not project_id:
#     print('Invalid project name and/or token')
# print(project_id)
# pool_id = get_pool_id(api, 'February_2020', project_id)
# if not pool_id:
#     print('Invalid pool name')
# print(pool_id)

# download_brk_files(11019463, 'D:\\data\\new_video', 'D:\\data\\video\\brk_video_urls.json', 'out_video')
