import csv
import  time
import sqlite3, os
from datetime import datetime
TABLE_NAME = ''
DB_NAME = "logs/DataBase.db"



COLUMN_NAMES = [
            "id",
            "id_cell",
            "x",
            'y',
            'dx',
            'dy',
            'radius' ,
            'view_field',
            'satiety' ,
            'dir' ,
            'color' ,
            'steps_amount' ,
            'steps_max' ,
            'can_colide' ,
            'last_colision_time'  ,
            'cant_colide_period'  ,
            'can_proliferation' ,
            'satiety_time'  ,
            'hunger_time' ,
            'spawn_time' ,
            'can_move' ,
            'creation_time' ,
            'children_amount' ,
            'steps_skip' ,
            'user_impact' ,
            'FIELD_WIDTH' ,
            'FIELD_HEIGHT'
]


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
def user_impact_transform(value):
    # 0,4; 4,0; 1,7; 1,3; 1,5; 2,6; 6,2; 3,1; 3,7; 3,5; 5,3; 5,7; 5,1; 7,1; 7,3; 7,5
    #счет от 0 направления
    if value[0]==0:
        if value[1]==0:
            return 0
        elif value[1]==1:
            return 1
        elif value[1]==2:
            return 2
        elif value[1]==3:
            return 3
        elif value[1]==4:
            return 4
        elif value[1]==5:
            return 5
        elif value[1]==6:
            return 6
        elif value[1]==7:
            return 7
    elif value[0]==1:
        if value[1]==0:
            return 8
        elif value[1]==1:
            return 0
        elif value[1]==2:
            return 9
        elif value[1]==3:
            return 10
        elif value[1]==4:
            return 11
        elif value[1]==5:
            return 12
        elif value[1]==6:
            return 13
        elif value[1]==7:
            return 14
    elif value[0]==2:
        if value[1]==0:
            return 15
        elif value[1]==1:
            return 16
        elif value[1]==2:
            return 0
        elif value[1]==3:
            return 17
        elif value[1]==4:
            return 18
        elif value[1]==5:
            return 19
        elif value[1]==6:
            return 20
        elif value[1]==7:
            return 21
    elif value[0]==3:
        if value[1]==0:
            return 22
        elif value[1]==1:
            return 23
        elif value[1]==2:
            return 24
        elif value[1]==3:
            return 0
        elif value[1]==4:
            return 25
        elif value[1]==5:
            return 26
        elif value[1]==6:
            return 27
        elif value[1]==7:
            return 28
    elif value[0]==4:
        if value[1]==0:
            return 29
        elif value[1]==1:
            return 30
        elif value[1]==2:
            return 31
        elif value[1]==3:
            return 32
        elif value[1]==4:
            return 0
        elif value[1]==5:
            return 33
        elif value[1]==6:
            return 34
        elif value[1]==7:
            return 35
    elif value[0]==5:
        if value[1]==0:
            return 36
        elif value[1]==1:
            return 37
        elif value[1]==2:
            return 38
        elif value[1]==3:
            return 39
        elif value[1]==4:
            return 40
        elif value[1]==5:
            return 0
        elif value[1]==6:
            return 41
        elif value[1]==7:
            return 42
    elif value[0]==6:
        if value[1]==0:
            return 43
        elif value[1]==1:
            return 44
        elif value[1]==2:
            return 45
        elif value[1]==3:
            return 46
        elif value[1]==4:
            return 47
        elif value[1]==5:
            return 48
        elif value[1]==6:
            return 0
        elif value[1]==7:
            return 49
    elif value[0]==7:
        if value[1]==0:
            return 50
        elif value[1]==1:
            return 51
        elif value[1]==2:
            return 52
        elif value[1]==3:
            return 53
        elif value[1]==4:
            return 54
        elif value[1]==5:
            return 55
        elif value[1]==6:
            return 56
        elif value[1]==7:
            return 0

def insert_db( row_names, list_values):
    # db_name = 'logs/'+db_name+".db"



    str_q_marks = ''.join(['?, ' for i in range(len(row_names))])
    str_q_marks = '(' + str_q_marks[0:len(str_q_marks)-2]+ ')'
    row_names='(' +', '.join(row_names) + ')'


    #Перевод вида голода в числа
    if list_values[7] == [0,0,1]:
        list_values[7]= 1
    elif list_values[7] == [0,1,0]:
        list_values[7]=2
    elif list_values[7] == [1,0,0]:
        list_values[7]=3

    #перевод цвета в число
    # начальный серый цвет
    if list_values[9] == (128, 128, 128):
        list_values[9]=0
    #обычный бирюзовый цвет клетки
    elif list_values[9] == (0, 125, 125):
        list_values[9] = 1
    # наступил голод, фиолетовый
    elif list_values[9] ==(255, 0, 255):
        list_values[9] = 2
    # потенциально скоро погибнет, если еще раз в этом состоянии столкнется, красный
    elif list_values[9] == (255, 0, 0):
        list_values[9] = 3
    # мертвый шар, черный
    elif list_values[9] == (0, 0, 0):
        list_values[9] = 4

    is_print = False
    #перевод направления в цифры
    list_values[23] = user_impact_transform(list_values[23])
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


def create_table(mark):
    global start_time
    start_time = time.time()

    global  TABLE_NAME
    global DB_NAME
    global cursor
    global sqliteConnection

    # подключение к нужной базе данных
    sqliteConnection = sqlite3.connect(DB_NAME)
    cursor = sqliteConnection.cursor()

    # текущая дата и время
    current_data_time = str(datetime.now().strftime("%d_%m_%Y__%H_%M_%S")).replace(" ", "_")
    #print(current_data_time)

    # table_name = ''
    # db_name = "logs/DataBase.db"

    #Запрос на получение баз данных
    sql_query = """SELECT name FROM sqlite_master
      WHERE type='table';"""

    cursor.execute(sql_query)

    #Создание списка таблиц (элементы - строковые названия таблиц)
    tables_list = [el[0] for el in cursor.fetchall()]
    #print(tables_list)

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

            number = 0
            # возможно и не надо пробегаться циклом, а просто так записать
            last_table = tables_list[-1]
            start_ind = 5
            stop_ind = last_table.find("_")
            number = int(last_table[start_ind:stop_ind])


            # for table in tables_list:
            #     #стартовый индекс. Все таблицы имеют в начале слово "Table" следующий после этого символ - начало порядкового номера
            #     start_ind = 5
            #     #индекс начала даты (начнинается с символа "_")
            #     stop_ind = table.find("_")
            #     if number< int(table[start_ind:stop_ind]):
            #         number= int(table[start_ind:stop_ind])
            number+=1
            TABLE_NAME = f'Table{number}_' + current_data_time
    TABLE_NAME = TABLE_NAME + '_' + mark
    #print(TABLE_NAME)
    #Создание таблицы
    #cursor = sqliteConnection.cursor()

    cursor.execute(f'''CREATE TABLE {TABLE_NAME}
            (id INTEGER PRIMARY KEY,
            id_cell integer,
            x real,
            y real,
            dx real,
            dy real,
            radius  real,
            view_field real,
            satiety integer,
            dir integer,
            color integer,
            steps_amount integer,
            steps_max integer,
            can_colide bool,
            last_colision_time real,
            cant_colide_period integer,
            can_proliferation bool,
            satiety_time integer,
            hunger_time integer,
            spawn_time integer,
            can_move bool,
            creation_time real,
            children_amount integer,
            steps_skip integer,
            user_impact integer,
            FIELD_WIDTH integer,
            FIELD_HEIGHT integer
            )''')


# cursor.execute(f'''CREATE TABLE {TABLE_NAME}
#           ID INTEGER PRIMARY KEY,
#           id_cell integer,
#           x real,
#           y real,
#           dx real,
#           dy real,
#           radius  real,
#           view_field real,
#           satiety integer,
#           dir integer,
#           color integer,
#           steps_amount integer,
#           steps_max integer,
#           can_colide bool,
#           last_colision_time  integer,
#           cant_colide_period  integer,
#           can_proliferation bool,
#           satiety_time  integer,
#           hunger_time integer,
#           spawn_time integer,
#           can_move bool,
#           creation_time integer,
#           children_amount integer,
#           steps_skip integer,
#           user_impact integer,
#           FIELD_WIDTH integer,
#           FIELD_HEIGHT integer
#
#      )''')

start_time = time.time()
TIME_16_PERIOD = 16
TIME_25_PERIOD = 25
TIME_50_PERIOD = 50

amount_16 = 0
amount_25 = 0

SEC_16_AMOUNT = 25
SEC_25_AMOUNT = 25


FOLDER_NAME = 'user_impactv2'

def make_csv_file():
    global  amount_16
    global amount_25
    time_period=0
    if time.time() - start_time> TIME_50_PERIOD:
        time_period = 50
    elif time.time() - start_time> TIME_25_PERIOD and amount_25<SEC_25_AMOUNT:
        time_period = 25
        amount_25+=1
    elif time.time() - start_time> TIME_16_PERIOD and amount_16<SEC_16_AMOUNT:
        time_period = 16
        amount_16+=1



    if time_period:
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")

        with open(f'logs/{FOLDER_NAME}/{time_period} sec/'+TABLE_NAME+'.csv', 'w', newline='') as filescv:
            writer = csv.writer(filescv)
            writer.writerow(COLUMN_NAMES)
            for row in cursor.fetchall():
                #print(row)
                writer.writerow(list(map(str,row)))

def print_files_amount():
    folder_name1 = "rnd_version2"
    folder_name2 = "user_impactv2"
    sub_folder1 = "16 sec"
    sub_folder2 = "25 sec"
    sub_folder3 = "50 sec"
    summa = 0
    steps_amount = 0
    files_amount = 0
    for f_name in [ folder_name2]:
        print(f'количество файлов в {f_name}:')
        for sub_f_name in [sub_folder1, sub_folder2, sub_folder3]:
            path, dirs, files = next(os.walk(f"./logs/{f_name}/{sub_f_name}"))
            file_count = len(files)
            print(f"\tВ папке '{sub_f_name}'\t{file_count} файлов")
            summa = 0
            files_amount+=len(files)
            for file_name in files:
                cell_id = int(file_name.split('_')[-1][0:-4])
                print(f'cell id = {cell_id}')
                with open(path+'/'+file_name, 'r') as filecsv:
                    arr = filecsv.readlines()
                    lines_count = len(arr)
                    summa+=lines_count

                    line_id =1

                    while int(arr[-line_id].split(',')[1])!=cell_id:
                        print(arr[-line_id].split(','), cell_id)
                        line_id +=1

                    last_line= arr[-line_id]
                    steps_amount += int(last_line.split(',')[11])
                    print(last_line)
            print(f'всего строк в папке {path} = {summa}')
        print()
    print(summa)
    print(f'steps_amount = {steps_amount} files_amount = {files_amount}, divide = {steps_amount/files_amount}')
# print_files_amount()




# sqliteConnection = sqlite3.connect(DB_NAME)
# sql_query = """SELECT name FROM sqlite_master
#   WHERE type='table';"""
# cursor = sqliteConnection.cursor()
# cursor.execute(sql_query)
# arr =  cursor.fetchall()
# # print( arr)
#
#
# # Создание списка таблиц (элементы - строковые названия таблиц)
# TABLE_NAME = 'Table576_04_05_2024__16_43_48_chng_rnd_14'
# #make_csv_file()
# select_everything()
