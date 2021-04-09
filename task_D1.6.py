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
        print(column['name'])
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create_task(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if ':' in column['name']:
            column_name_from_API = column['name'].split(':')[0]
        else:
            column_name_from_API = column['name']
        if column_name_from_API == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
            auth_params['name'] = column_name_from_API + ': ' + str(len(task_data)) + ' tasks'
            requests.put('https://api.trello.com/1/lists/{}'.format(column['id']), params = auth_params)
            break

def create_column(name):
    url = "https://api.trello.com/1/boards/{}/lists".format(board_id)
    auth_params['name'] = name + ': 0 tasks'
    response = requests.request(
       "POST",
       url,
       params=auth_params
    )



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
        task_id = task_dict.keys()[0]
    else:
        return 'Данного названия задачи не сущесвует.'

    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            break


# if __name__ == "__main__":
#     if len(sys.argv) < 2 or sys.argv[1] == 'read':
#         read()
#     elif sys.argv[1] == 'create_task':
#         create_task(sys.argv[2], sys.argv[3])
#     elif sys.argv[1] == 'create_column':
#         create_column(sys.argv[2])
#     elif sys.argv[1] == 'move':
#         move(sys.argv[2], sys.argv[3:])

if __name__ == "__main__":
    if sys.argv[1] == 'read':
        read()
    elif sys.argv[1] == 'create_task':
        name = input()
        column_name = input()
        create_task(name, column_name)
    elif sys.argv[1] == 'create_column':
        column_name = input()
        create_column(column_name)
    elif sys.argv[1] == 'move':
        name = input()
        column_name = input()
        move(name, column_name)