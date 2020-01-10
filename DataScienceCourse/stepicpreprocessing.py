import math

import pandas as pd
import numpy as np

COURSE_LENGTH = 198
WORK_LENGTH = 76


def make_data_ready(event_data, submissions_data):
    # Сдан ли курс (количество правильных (разных) практических заданий больше 40)
    event_data['date'] = pd.to_datetime(event_data.timestamp, unit='s')
    event_data['day'] = event_data.date.dt.date

    # Сколько и какого вида actions совершил студент (таблица events)
    x = event_data.pivot_table(index='user_id', columns='action'
                               , values='step_id', aggfunc='count'
                               , fill_value=0).reset_index()

    submissions_data['date'] = pd.to_datetime(submissions_data.timestamp, unit='s')
    submissions_data['day'] = submissions_data.date.dt.date

    # Количества правильно и неправильно решенных заданий
    x = x.merge(submissions_data.pivot_table(index='user_id', columns='submission_status'
                                             , values='step_id', aggfunc='count'
                                             , fill_value=0).reset_index(), how='outer', on='user_id')

    # Количество заданий, которые студент пытался решить
    x = x.merge(submissions_data.groupby('user_id').step_id.nunique().to_frame()
                .reset_index().rename(columns={'step_id': 'steps_tried'}), on='user_id', how='outer')

    # Наибольшая разница между timestamp событий
    temp = (event_data.groupby('user_id').timestamp.max() - event_data.groupby(
        'user_id').timestamp.min()) \
        .to_frame().reset_index().rename(columns={'timestamp': 'timestamp_diff_events'})
    x = x.merge(temp, on='user_id', how='outer')

    # Наибольшая разница между timestamp сабмитов
    temp = (submissions_data.groupby('user_id').timestamp.max() - submissions_data.groupby(
        'user_id').timestamp.min()) \
        .to_frame().reset_index().rename(columns={'timestamp': 'timestamp_diff_submits'})
    x = x.merge(temp, on='user_id', how='outer')

    # Отношение правильно решенных заданий к неправильным
    x['efficiency'] = x.correct / x.wrong

    # Пройденная часть курса в событиях
    temp = (event_data.groupby('user_id').step_id.nunique() / COURSE_LENGTH) \
        .to_frame().reset_index().rename(columns={'step_id': 'event_passed_part'})
    x = x.merge(temp, on='user_id', how='outer')

    # Пройденная часть курса в сабмитах
    temp = (submissions_data[submissions_data.submission_status == 'correct']
            .groupby('user_id').step_id.nunique() / WORK_LENGTH) \
        .to_frame().reset_index().rename(columns={'step_id': 'submit_passed_part'})
    x = x.merge(temp, on='user_id', how='outer')

    x = x.replace(math.inf, 0)
    x = x.fillna(0)
    return x.drop('user_id', axis=1)
