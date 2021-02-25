# -*- coding: utf-8 -*-

import requests
import argparse
from pprint import pprint
from  functools import reduce
import json
import os

#class TolokaAPI(TolokaAPICore):
class TolokaAPI():
    def __init__(self, token, sandbox = True):
        self.TOKEN = token
        self.toloka_url = 'https://sandbox.toloka.yandex.ru/api/v1' if sandbox else 'https://toloka.yandex.ru/api/v1'

    # Отправка "боевого запроса" в толоку
    def __get_request(self, address, params = None):
        with requests.Session() as s:
            headers = {"Authorization": "OAuth "+self.TOKEN}
            r = s.get(self.toloka_url + address, params=params, headers=headers) 
        return r

    def __path_request(self, address, params = None):
        with requests.Session() as s:
            headers = {"Authorization": "OAuth "+self.TOKEN}
            r = s.get(self.toloka_url + address, params=params, headers=headers)
        return r

    def __post_request(self, address, data = None, json = None):
        with requests.Session() as s:
            headers = {"Authorization": "OAuth "+self.TOKEN}
            r = s.post(self.toloka_url + address, data=data, json=json)
        return r

    def __check_params(self, params, params_name):
        flag = all(list(map(lambda name: name in params_name, params.keys())))
        return flag

    def __proc_function(self, address, params, params_name):
        try:
            assert self.__check_params(params, params_name)
        except  AssertionError:
            print("Неверные параметры в вызове.")
            raise
        else:
            return self.__get_request(address, params)

    #################
    #### Проекты ####
    #################

    # Получить список проектов # Поля params:
    # status - статус проекта
    # limit - максимальное количество результатов в ответе
    # sort - поля для сортировки
    # id_gt - id проекта
    # id_gte - id проекта
    # id_lt - id проекта
    # id_lte - id проекта
    # created_gt - дата
    # created_gte - дата
    # created_lt - дата
    # created_lte - дата
    def get_list_of_projects(self, params):
        params_name = [
            "status",
            "limit",
            "sort",
            "id_gt",
            "id_gte",
            "id_lt",
            "id_lte",
            "created_gt",
            "created_gte",
            "created_lt",
            "created_lte"
        ]
        address = '/projects'
        return self.__proc_function(address, params, params_name)

    # Получить информацию о проекте
    # project_id - id проекта
    def get_project_properties(self, project_id):
        address = '/projects/' + str(project_id)
        return self.__get_request(address)


    ##############
    #### Пулы ####
    ##############

    # Получить списук пулов
    # Поля params:
    # status - статус пула
    # project_id - id проекта
    # limit - максимальное количество результатов в ответе
    # sort - поля для сортировки
    # id_gt - id пула
    # id_gte - id пула
    # id_lt - id пула
    # id_lte - id пула
    # created_gt - дата
    # created_gte - дата
    # created_lt - дата
    # created_lte - дата
    # last_started_gt - дата
    # last_started_gte - дата
    # last_started_lt - дата
    # last_started_lte - дата
    def get_list_of_pools(self, params):
        params_name = [
            "status",
            "project_id",
            "limit",
            "sort",
            "id_gt",
            "id_gte",
            "id_lt",
            "id_lte",
            "created_gt",
            "created_gte",
            "created_lt",
            "created_lte",
            "last_started_gt",
            "last_started_gte",
            "last_started_lt",
            "last_started_lte",
        ]
        address = '/pools'
        return self.__proc_function(address, params, params_name)

    # Получить информацию о пуле
    # pool_id - id пула
    def get_pool_properties(self, pool_id):
        address = '/pools/' + str(pool_id)
        return self.__get_request(address)

    # Создать пул
    def create_pool(self, json):
        params_name = [
            #...
        ]
        address = '/pools'
        # assert self.__check_params(json, params_name)
        with requests.Session() as s:
            headers = {"Authorization": "OAuth "+self.TOKEN, "Content-Type": "application/JSON"}
            r = s.post(self.toloka_url + address, json=json, headers=headers)
        return r.text

    def update_pool(self, pool_id, json):
        params_name = [
            # ...
        ]
        address = '/pools/' + str(pool_id)
        # assert self.__check_params(json, params_name)
        with requests.Session() as s:
            headers = {"Authorization": "OAuth " + self.TOKEN, "Content-Type": "application/JSON"}
            r = s.post(self.toloka_url + address, json=json, headers=headers)
        return r.text

    # Открыть пул
    # pool_id - id пула
    def open_pool(self, pool_id):
        address = '/pools/' + str(pool_id) + '/open'
        return self.__post_request(address)

    # Закрыть пул
    # pool_id - id пула
    def close_pool(self, pool_id):
        address = '/pools/' + str(pool_id) + '/close'
        return self.__post_request(address)

    # Клонировать пул
    # pool_id - id пула
    def clone_pool(self, pool_id):
        address = '/pools/' + str(pool_id) + '/clone'
        return self.__post_request(address)

    ################
    #### Ответы ####
    ################

    # Получить список ответов
    # Поля params:
    # status - статус выданного набора заданий
    # task_id - id задания
    # task_suite_id - id набора заданий
    # pool_id - id пула
    # user_id - id пользователя
    # limit - максимальное количество результатов в ответе
    # sort - поля для сортировки
    # id_gt - id выдачи набора заданий
    # id_gte - id выдачи набора заданий
    # id_lt - id выдачи набора заданий
    # id_lte - id выдачи набора заданий
    # created_gt - дата
    # created_gte - дата
    # created_lt - дата
    # created_lte - дата
    # submitted_gt - дата
    # submitted_gte - дата
    # submitted_lt - дата
    # submitted_lte - дата
    def get_list_of_assignments(self, params):
        params_name = [
            "status",
            "task_id",
            "task_suite_id",
            "pool_id",
            "user_id",
            "limit",
            "sort",
            "id_gt",
            "id_gte",
            "id_lt",
            "id_lte",
            "created_gt",
            "created_gte",
            "created_lt",
            "created_lte",
            "submitted_gt",
            "submitted_gte",
            "submitted_lt",
            "submitted_lte",
        ]
        address = '/assignments'
        return self.__proc_function(address, params, params_name)

    # Изменение статуса задания
    def set_assignment_status(self, id, json):
        params_name = [
            "status", # [SUBMITTED, ACCEPTED, REJECTED]
            "public_comment",
        ]
        address = '/assignments/'+str(id)
        assert self.__check_params(json, params_name)
        with requests.Session() as s:
            headers = {"Authorization": "OAuth "+self.TOKEN, "Content-Type": "application/JSON"}
            r = s.patch(self.toloka_url + address, json=json, headers=headers)
        return r

    ################
    ### Задания ####
    ################

    # Получить список заданий
    # Поля params:
    # pool_id - id пула
    # limit - максимальное количество результатов в ответе
    # sort - поля для сортировки
    # id_gt - id задания
    # id_gte - id задания
    # id_lt - id задания
    # id_lte - id задания
    # created_gt - дата
    # created_gte - дата
    # created_lt - дата
    # created_lte - дата
    # overlap - перекрытие
    # overlap_gt - перекрытие
    # overlap_gte - перекрытие
    # overlap_lt - перекрытие
    # overlap_lte - перекрытие
    def get_list_of_tasks(self, params):
        params_name = [
            "pool_id",
            "limit",
            "sort",
            "id_gt",
            "id_gte",
            "id_lt",
            "id_lte",
            "created_gt",
            "created_gte",
            "created_lt",
            "created_lte",
            "overlap",
            "overlap_gt",
            "overlap_gte",
            "overlap_lt",
            "overlap_lte",
        ]
        address = '/tasks'
        return self.__proc_function(address, params, params_name)
    
    # Получить информацию о задании
    # task_id - id задания
    def get_task_properties(self, task_id):
        address = '/tasks/' + str(task_id)
        return self.__get_request(address)

    # Создать задание
    def create_task(self, json):
        params_name = [
            #...
        ]
        address = '/tasks'
        # assert self.__check_params(json, params_name)
        with requests.Session() as s:
            headers = {"Authorization": "OAuth "+self.TOKEN, "Content-Type": "application/JSON"}
            r = s.post(self.toloka_url + address, json=json, headers=headers)
        return r.text

    ################
    ###  Файлы  ####
    ################

    # Получить список файлов
    # Поля params:
    # name - имя файла
    # type - тип приложения (только ASSIGNMENT_ATTACHMENT)
    # user_id - id пользователя
    # assignment_id - id выдачи набора данных
    # pool_id - id пула
    # limit - максимальное количество результатов в ответе
    # sort - поля для сортировки
    # id_gt - id файла
    # id_gte - id файла
    # id_lt - id файла
    # id_lte - id файла
    # created_gt - дата
    # created_gte - дата
    # created_lt - дата
    # created_lte - дата
    def get_list_of_files(self, params):
        params_name = [
            "name",
            "type",
            "user_id",
            "assignment_id",
            "pool_id",
            "limit",
            "sort",
            "id_gt",
            "id_gte",
            "id_lt",
            "id_lte",
            "created_gt",
            "created_gte",
            "created_lt",
            "created_lte",
        ]
        address = '/attachments'
        return self.__proc_function(address, params, params_name)

    # Получить информацию о файле
    # file_id - id файла
    def get_file_properties(self, file_id):
        address = '/attachments/' + str(file_id)
        return self.__get_request(address)

    # Скачать файл
    # file_id - id файла
    def get_file(self, file_id, spoof_dir=''):
        address = '/attachments/' + str(file_id) + '/download'
        video = self.__get_request(address)
        ext = video.headers['content-type'].rsplit('/', maxsplit=1)
        if ext == 'quicktime':
            ext = 'mov'
        filename = os.path.join(spoof_dir, file_id + '.' + ext[-1])
        with open(filename, 'wb') as f:
            for chunk in video.iter_content(chunk_size=255): 
                if chunk:
                    f.write(chunk)


def main():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-t', '--token', action='store',
                        help='tolokaAPI token',
                        required=True)
    parser.add_argument('-s', '--sandbox', action='store_true',
                        help='sandbox mode')

    args = parser.parse_args()

    api = TolokaAPI(args.token)

    # pprint(api.get_project_properties('13386'))
    # pprint(api.get_list_of_pools(params).json())


if __name__ == "__main__":
    main()
