import os
import DB_program

def get_folders_names():
    folder_name1 = "rnd_version2"
    folder_name2 = "user_impactv2"
    sub_folder1 = "16 sec"
    sub_folder2 = "25 sec"
    sub_folder3 = "50 sec"

    folder_names =[]
    temp_list = []
    for f_name in [folder_name1, folder_name2]:
        temp_list.append(f_name)
    folder_names.append(temp_list)

    temp_list = []
    for sub_f_name in [sub_folder1, sub_folder2, sub_folder3]:
        temp_list.append(sub_f_name)
    folder_names.append(temp_list)
    return folder_names
def get_new_file_name(main_folder_name, sub_folder_name):
    return f'./logs/{main_folder_name}/{main_folder_name+"_"+sub_folder_name}.csv'

def get_current_folders_names(main_folder, sub_folder):
    return f'./logs/{main_folder}/{sub_folder}'

def delete_tables():
    folder_names = get_folders_names()
    for f_name in folder_names[0]:
        for sub_f_name in folder_names[1]:
            os.remove(get_new_file_name(f_name, sub_f_name))
            # print(get_file_name(f_name, sub_f_name))
def get_cell_id(talbe_name):
    return talbe_name.split('_')[-1].split('.')[0]
def get_table_id(talbe_name):
    return  talbe_name.split('_')[0][5::]
def make_dataset():
    folder_names =get_folders_names()
    for f_name in folder_names[0]:
        for sub_f_name in folder_names[1]:
            path, dirs, files = next(os.walk(get_current_folders_names(f_name, sub_f_name)))
            # print(path)
            title_already_written = False
            with open(get_new_file_name(f_name, sub_f_name), 'a') as target_csv:
                for file in files:
                    targetCellId = get_cell_id(file)    #file.split('_')[-1].split('.')[0]
                    targetTableId = get_table_id(file)  #file.split('_')[0][5::]
                    # print( targetCellId)
                    with open(f'./logs/{f_name}/{sub_f_name}/{file}', 'r') as source_csv:
                        for line in source_csv.readlines():
                            if line.split(',')[1]==targetCellId or (not title_already_written and line.split(',')[0]=='id' ):
                                if not title_already_written:
                                    print(line.strip('\n') + ',' + 'TableID', file=target_csv)
                                else:
                                    print(line.strip('\n')+','+targetTableId, file = target_csv)
                                title_already_written = True

def make_anal():
    pass


def get_save_lst(save_list):
    temp_list = []
    temp_id = -1
    # запись данных за предыдущий такт для сохранения в файл
    for sub_list in save_list:
        if int(sub_list[1]) > temp_id:
            temp_list.append(sub_list)  # [el for el in sub_list])
            temp_id = int(sub_list[1])
        else:
            break
    # print(f'BIG save_arr = {len(save_list)} {save_list}')
    # for sub_list in temp_list:
    #     save_list.remove(sub_list)

    # создание списка для записи в файл
    # save_lst = []
    # for sub_list in temp_list:
    #     for el in sub_list:
    #         save_lst.append(el)
    # # заполнение нулями списка
    # for i in range(COLUMN_NUMBER * ROW_NUMBER - len(save_lst)):
    #     save_lst.append('0')

    # print(f'save_arr = {len(save_list)} {save_list}')
    # print(f'temp_list = {len(temp_list)} {temp_list}')

    return temp_list

def user_impact_transform(value):
    if (value=='0' or value=='8' or value=='15' or value=='22' or value=='29'  or value=='36'  or value=='43' or value=='50'):
        res= '0'
    elif(value=='1' or value=='16' or value=='23' or value=='30'  or value=='37'  or value=='44' or value=='51'):
        res=  '1'
    elif (value=='2' or value=='9' or value=='24' or value=='31'  or value=='38'  or value=='45' or value=='52'):
        res= '2'
    elif (value=='3' or value=='10' or value=='17' or value=='32'  or value=='39'  or value=='46' or value=='53'):
        res= '3'
    elif (value=='4' or value=='11' or value=='18' or value=='25'  or value=='40'  or value=='47' or value=='54'):
        res= '4'
    elif (value=='5' or value=='12' or value=='19' or value=='26'  or value=='33'  or value=='48' or value=='54'):
        res= '5'
    elif (value=='6' or value=='13' or value=='20' or value=='27'  or value=='34'  or value=='41' or value=='56'):
        res= '6'
    else:
        res= '7'

    return  str(int(res)/10)

def append_to_file(file_path,save_str):
    with open(file_path, 'a') as file_csv:
        print(save_str, file=file_csv)
def make_one_dataset_for_NN(source_path, target_path, targetCellId):
    global COLUMN_NUMBER
    global ROW_NUMBER



    is_first = True
    save_list = []

    with open(source_path, 'r') as source_csv:
        prev_cell_id = -1

        for line in source_csv.readlines():

            line = line.strip('\n')
            print(f'line = {line}')

            line_splitted = line.split(',')

            #удаление ненужных значений из строки
            for id in DELETE_COLUMNS_IDS_REVERSED:
                line_splitted.pop(id)

            #первая линия - заголовок
            if line_splitted[0] == 'id':
                title=''
                for i in range(ROW_NUMBER):
                    arr = line_splitted.copy()
                    for j in range(len(arr)):
                        arr[j]=arr[j]+str(i)
                    title+=','.join(arr)+','

                title+="next_user_impact"
                print(title)
                append_to_file(file_path=target_path, save_str=title)



            #остальные линии
            else:
                #условие сохранения данных
                if not is_first and int(line_splitted[1]) == int(targetCellId):
                    save_list.append(line_splitted)


                    #формирование итогового списка(двумерного) сохранения и перевод его в строку
                    temp_list = get_save_lst(save_list)


                    #формирование итогового списка(одномерного) сохранения и перевод его в строку
                    save_temp_list = []
                    #переход от двумерного к одномерному списку
                    for sub_list in save_list:
                        for el in sub_list:
                            save_temp_list.append(el)
                    # заполнение нулями списка
                    for i in range(COLUMN_NUMBER * ROW_NUMBER - len(save_temp_list)):
                        save_temp_list.append('0')
                    #print(len(save_temp_list))
                    save_temp_list.append(user_impact_transform(line_splitted[-1]))

                    # Удаление лишних элементов из основного списка данных
                    save_list = save_list[len(temp_list)::]
                    save_str = ','.join(save_temp_list)
                    append_to_file(file_path=target_path, save_str=save_str)


                else:
                     if int(line_splitted[1]) == int(targetCellId) and is_first:
                         is_first = False
                     save_list.append(line_splitted)

        # формирование последней записи
        #save_temp_list = get_save_lst(save_list)


        #удаление такта из списка
        id = -1
        del_list = []
        for el in save_list:
            if int(el[1])>id:
                id = int(el[1])
                del_list.append(el)
            else:
                break
        save_list = save_list[len(del_list)::]

        temp_list = []
        for el in save_list:
            if el not in save_temp_list:
                temp_list.append(el)
        save_list =[]
        for sub_list in temp_list:
            for el in sub_list:
                save_list.append(el)
        for i in range(COLUMN_NUMBER * ROW_NUMBER - len(save_list)):
            save_list.append('0')
        save_list.append(str(0.0))
        save_str = ','.join(save_list)
        # print(f'ID = {targetCellId}\nsave_list = {save_list}\n  save_temp_list = {save_temp_list}\ntemp_list = {temp_list}\n save_str =  {save_str} \n')
        append_to_file(file_path=target_path, save_str=save_str)


def make_all_dataset_for_NN():
    #алгоритм создания нейминга датасетов
    folder_names = get_folders_names()
    for f_name in folder_names[0]:
        for sub_f_name in folder_names[1]:
            path, dirs, files = next(os.walk(get_current_folders_names(f_name, sub_f_name)))

            for filename in files:
                targetCellId = get_cell_id(filename)
                targetTableId = get_table_id(filename)
                source_path = path + '/' + filename
                target_path = f'./logs/dataset/{f_name}/{sub_f_name}/dataset{targetTableId}_{f_name.split("_")[0]}_{targetCellId}.csv'
                make_one_dataset_for_NN(source_path, target_path,targetCellId)

def delete_datasets():
    folder_names = get_folders_names()
    #print(folder_names)
    for f_name in folder_names[0]:
        for sub_f_name in folder_names[1]:
            path, dirs, files = next(os.walk(f'./logs/dataset/{f_name}/{sub_f_name}'))
            for file in files:
                os.remove(f'./logs/dataset/{f_name}/{sub_f_name}/{file}')


def make_summary_datasets():
    dataset_folder_path = './logs/dataset'
    path, dirs_main, files = next(os.walk(dataset_folder_path))
    for dir in dirs_main:
        if dir == 'rnd_version2':
            continue
        is_first = True
        path, sub_dirs, files = next(os.walk(dataset_folder_path+'/'+dir))
        for sub_dir in sub_dirs:
            path, dirs, files = next(os.walk(dataset_folder_path + '/' + dir+'/'+sub_dir))
            for file_csv_name in files:
                # print(path+'/'+file_csv_name)
                # print(dataset_folder_path+'/'+f'{dir.split("_")[0]}')
                # print()
                with open(path+'/'+file_csv_name, 'r') as source_csv:
                    # for line in source_csv.readlines():
                    #     if line.strip('\n').split(',')[-1] == 'next_user_impact':
                    #         #print('skipped')
                    #         continue
                    #     if float(line.strip('\n').split(',')[-1]) >1.0:
                    #         print(path+'/'+file_csv_name)
                    for line in source_csv.readlines():
                        # print(line.split(',')[0])
                        if  line.split(',')[0] == 'id0':
                            if is_first:
                                append_to_file(dataset_folder_path+'/'+f'{dir.split("_")[0]}.csv', line.strip('\n'))
                                is_first = False
                        else:
                            append_to_file(dataset_folder_path+'/'+f'{dir.split("_")[0]}.csv', line.strip('\n'))


DELETE_COLUMNS_NAMES = [
            'dx',
            'dy',
            'radius' ,
            'view_field',
            'steps_max' ,
            'cant_colide_period'  ,
            'can_proliferation' ,
            'FIELD_WIDTH' ,
            'FIELD_HEIGHT'
                       ]
COLUMN_NUMBER = len(DB_program.COLUMN_NAMES)-len(DELETE_COLUMNS_NAMES)
ROW_NUMBER = 20
DELETE_COLUMNS_IDS_REVERSED =[]
for str1 in DELETE_COLUMNS_NAMES:
    DELETE_COLUMNS_IDS_REVERSED.append(DB_program.COLUMN_NAMES.index(str1))
DELETE_COLUMNS_IDS_REVERSED.reverse()

def make_csv_only_impact():
    path = './logs/dataset'
    source_file_name = 'user.csv'
    target_file_name = 'user_impact.csv'

    with open(path+'/'+source_file_name, 'r') as source_csv:
        for line in source_csv.readlines():
            line = line.strip('\n')
            for user_impact in line.split(',')[17::18]:
                if user_impact == 'user_impact0':
                    with open(path+'/'+target_file_name, 'a') as target_csv:
                        print(line, file =target_csv)
                    break
                if int(line[-1])>0:
                    with open(path+'/'+target_file_name, 'a') as target_csv:
                        print(line, file =target_csv)
                    break


make_csv_only_impact()
# make_summary_datasets()
# make_all_dataset_for_NN()
# make_dataset()
# get_folders_names()
# delete_datasets()

# delete_tables()
# make_all_dataset_for_NN()
# make_one_dataset_for_NN(source_path='./logs/user_impactv2/50 sec/Table8459_06_05_2024__14_40_41_user_10.csv',
#                         target_path='./logs/user_impactv2/a.csv',
#                         targetCellId="10"
#                         )