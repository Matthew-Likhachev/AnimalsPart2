import sqlite3, os
from datetime import datetime
TABLE_NAME = ''
DB_NAME = "logs/DataBase.db"

# подключение к нужной базе данных
sqliteConnection = sqlite3.connect(DB_NAME)
cursor = sqliteConnection.cursor()


# def connect_db(db_name = 'log', table_name = 'Test'):
#     db_name = 'logs/'+db_name+".db"
#
#     if not os.path.exists(db_name):
#         conn = sqlite3.connect(db_name)
#
#         # Создание курсора для выполнения SQL-запросов
#         cursor = conn.cursor()
#         # Создание таблицы
#         cursor.execute(f'''CREATE TABLE {table_name}
#                      (id INTEGER PRIMARY KEY,
#         x real,
#         y real,
#         dx real,
#         dy real,
#         radius  real,
#         view_field real,
#         satiety integer,
#         can_colide bool,
#         cant_colide_period  integer,
#         last_colision_time  integer,
#         can_proliferation bool,
#         satiety_time  integer,
#         hunger_time integer,
#         spawn_time integer,
#         can_move bool,
#         breed text,
#         child_breed text,
#         live_time integer,
#         children_amount integer,
#         id_cell integer
#         )''')
#
#         conn.commit()
#         conn.close()

def insert_db( row_names, list_values):
    # db_name = 'logs/'+db_name+".db"


    str_q_marks = ''.join(['?, ' for i in range(len(row_names))])
    str_q_marks = '(' + str_q_marks[0:len(str_q_marks)-2]+ ')'
    row_names='(' +', '.join(row_names) + ')'

    if list_values[0] == [0,0,1]:
        list_values[0]= 1
    elif list_values[0] == [0,1,0]:
        list_values[0]=2
    elif list_values[0] == [1,0,0]:
        list_values[0]=3
    list_values = tuple(list_values)

    # Вставка данных в базу данных
    cursor.execute(f"INSERT INTO {TABLE_NAME} {row_names}"
          f" VALUES {str_q_marks}",
          list_values)

def commit():
    sqliteConnection.commit()
def close():
    sqliteConnection.close()

def select_everything():
    # db_name = 'logs/'+db_name+".db"

    cursor.execute(f"SELECT * FROM {TABLE_NAME}")

    for row in cursor.fetchall():
        print(row)


def create_table():
    global  TABLE_NAME

    # текущая дата и время
    current_data_time = str(datetime.now().strftime("%d_%m_%Y__%H_%M_%S")).replace(" ", "_")
    print(current_data_time)

    # table_name = ''
    # db_name = "logs/DataBase.db"

    #Запрос на получение баз данных
    sql_query = """SELECT name FROM sqlite_master
      WHERE type='table';"""

    cursor.execute(sql_query)

    #Создание списка таблиц (элементы - строковые названия таблиц)
    tables_list = [el[0] for el in cursor.fetchall()]
    print(tables_list)

    if len(tables_list) == 0:
        TABLE_NAME = 'Table0_' + current_data_time
    else:
        # список нахождения нулевой таблицы в списке. Если таблица есть то значение 0, иначе -1
        is_table0_list = list(map(lambda table: table.find("Table0"), tables_list))
        #таблица не найдена
        if sum(is_table0_list) * -1 == len(is_table0_list):
            TABLE_NAME = 'Table0_' + current_data_time
        else:
            #создание нового имени по алгоритму


            # возможно и не надо пробегаться циклом, а просто так записать
            last_table = tables_list[-1]
            start_ind = 5
            stop_ind = last_table.find("_")
            number = last_table[start_ind:stop_ind]

            number = 0
            # for table in tables_list:
            #     #стартовый индекс. Все таблицы имеют в начале слово "Table" следующий после этого символ - начало порядкового номера
            #     start_ind = 5
            #     #индекс начала даты (начнинается с символа "_")
            #     stop_ind = table.find("_")
            #     if number< int(table[start_ind:stop_ind]):
            #         number= int(table[start_ind:stop_ind])
            number+=1
            TABLE_NAME = f'Table{number}_' + current_data_time

    #Создание таблицы
    #cursor = sqliteConnection.cursor()
    cursor.execute(f'''CREATE TABLE {TABLE_NAME}
        (id INTEGER PRIMARY KEY,
       x real,
       y real,
       dx real,
       dy real,
       radius  real,
       view_field real,
       satiety integer,
       can_colide bool,
       cant_colide_period  integer,
       last_colision_time  integer,
       can_proliferation bool,
       satiety_time  integer,
       hunger_time integer,
       spawn_time integer,
       can_move bool,
       breed text,
       child_breed text,
       live_time integer,
       children_amount integer,
       id_cell integer,
       creation_time integer,
       FIELD_WIDTH integer,
       FIELD_HEIGHT integer
       )''')





# sqliteConnection = sqlite3.connect(DB_NAME)
# sql_query = """SELECT name FROM sqlite_master
#   WHERE type='table';"""
# cursor = sqliteConnection.cursor()
# cursor.execute(sql_query)
# arr =  cursor.fetchall()
# print( arr)
#
# #
# # Создание списка таблиц (элементы - строковые названия таблиц)
# TABLE_NAME = 'Table1_24_03_2024__16_50_09'
# select_everything()
