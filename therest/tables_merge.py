from googleapiclient.discovery import build
import json
import re


API_KEY = 'AIzaSyBhT7i0HvxQ0JXWZHcBPMKrekE83dxvcxM'
SHEET1 = '1DKRq6CnpFm_wFnVVo2UnUfzuH_s2DtDsJMDAMnHYIFI'
SHEET2 = '1kboYe0wPftOOXp5NdnC5qP4iZzeUGVRMVKgul77AneQ'
SHEET3 = '1DOG7z1GC4Pk3IDwrhpEjcUl9R00YBwfkEtGMO_VzS5Q'
SHEET4 = '14oZitIDDw-4PU9_UFp2DEUtm1Y4UlNUXSVXwgpZnrJo'
SHEET5 = '1YBzxlK0AyUFLNv4aPDGfXAtUhMOSdbeMQk6f5JNNYSo'


def get_markup(table_row):
    data_object = {}
    if len(table_row) > 1:
        data_object['gunshot'] = table_row[1]
    else:
        return data_object
    if len(table_row) > 2:
        data_object['speech'] = table_row[2]
    else:
        return data_object
    if len(table_row) > 3:
        data_object['sound_from_target'] = table_row[3]
    else:
        return data_object
    if len(table_row) > 4:
        data_object['environment'] = table_row[4]
    else:
        return data_object
    if len(table_row) > 5:
        data_object['environment_tag'] = table_row[5]
    else:
        return data_object
    if len(table_row) > 6:
        data_object['distance_to_object'] = table_row[6]
    else:
        return data_object
    if len(table_row) > 7:
        data_object['target_material'] = table_row[7]
    else:
        return data_object
    if len(table_row) > 8:
        data_object['microphone_distance'] = table_row[8]
    else:
        return data_object
    if len(table_row) > 9:
        data_object['shooting_type'] = table_row[9]
    else:
        return data_object
    if len(table_row) > 11:
        data_object['comment'] = table_row[11]
    else:
        return data_object
    return data_object


with open('gunshot_data') as file:
    data = json.load(file)

service = build('sheets', 'v4', developerKey=API_KEY)

result = service.spreadsheets().get(spreadsheetId=SHEET5).execute()
values = result.get('sheets', [])

ranges_template = ['!' + str(i) + ':' + str(i) for i in range(1, 1001)]
sheets = [value['properties']['title'] for value in values]

tables = []
for sheet in sheets[0:5]:
    range_names = [sheet + template for template in ranges_template]
    result = service.spreadsheets().values().batchGet(spreadsheetId=SHEET5, ranges=range_names).execute()
    for res in result['valueRanges']:
        if 'values' in res:
            tables += res['values']

regexp = re.compile(r'.+embed/(.+)\?start=(\d+)&end=(\d+)')
for row in tables:
    match = regexp.match(row[0])
    if match:
        video_id = match.group(1) + '_' + match.group(2) + '_' + match.group(3)
        data[video_id] = get_markup(row)

with open('gunshot_data', 'w') as file:
    data = json.dump(data, file, indent=4)
