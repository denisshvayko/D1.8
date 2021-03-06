### Для активации вирутального окружения
### python -m venv C:\web_developer_tasks\D1\D1.6\env
### env\Scripts\activate.bat

from config import trello_key, trello_token, board_id
import sys
import requests


base_url = "https://api.trello.com/1/{}"
auth_params = {
    'key': trello_key,
    'token': trello_token, }



def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + "||##|| количество задач - " + str(len(task_data)))

        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + "Название задачи: " + task['name'] + "--  ID задачи: " + task['id'] )


def column_check(column_name):
    column_id = None
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            column_id = column['id']
            return column_id
    return column_id

def create_task(name, column_name):
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})


def create_column(name):
    return requests.post(base_url.format('boards') + '/' + board_id + '/lists',
                         data={'name': name, 'idBoard': board_id, **auth_params}).json()



def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_dict = {}
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()

        for task in column_tasks:
            if task['name'] == name:
                task_dict[task['id']] = {'task_column_name': column['name'], 'list_id': task['idList']}

    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    if len(task_dict.keys()) > 1:
        print('У вас несколько задач с таким именем выберите id задачи которую вы хотите перенести:')
        for k, v in task_dict.items():
            print('Название колонки: ' + v['task_column_name'] + ' |__| Название задачи: ' + name + ' |__| id: ' + k)
        task_id = input()
    elif len(task_dict.keys()) == 1:
        task_id = list(task_dict.keys())[0]
    else:
        return 'Данного названия задачи не сущесвует.'
    for column in column_data:
        if column['name'] == column_name[0]:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            break


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == 'read':
        read()
    elif sys.argv[1] == 'create_task':
        create_task(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3:])
