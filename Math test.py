import keyboard
import sys

from threading import Thread
import time
import pygame
import random
import DB_program

def give_me_time(param = True):
    if param==True:
        return float('%.2f' % time.time())
    else:
        return float('%.2f' % param)

class Cell_properties():
    global START_TIME
    def __init__(self,x=0,y=0,dx=0,dy=0,radius=25, view_field=50, satiety = [1,0,0], can_colide = False, last_colision_time=0, can_proliferation = False, id_cell=0):
        #x=0,y=0,dx=0,dy=0,radius=25, view_field=50, satiety = [1,0,0], can_colide = false, last_colision_time=0, can_proliferation = false
        self.id_cell = id_cell
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.radius = radius        #размер шара
        self.view_field = view_field  #поле зрения шара
        self.satiety = satiety      #сытость. [1,0,0] – сытая клетка, [0,1,0] – голодная, [0,0,1] – смерть
        self.can_colide = can_colide # true false - может или нет сталкиваться с другими шарами. Если столкнулся - умирает
        self.cant_colide_period = 3 #через 3 секунды снова может сталкиваться
        self.creation_time =  give_me_time(give_me_time() - START_TIME)    #время создания клетки от начала игры
        self.last_colision_time = give_me_time(last_colision_time - START_TIME - self.creation_time )#последнее время коллизии. Отсчет с начала игры
        self.can_proliferation=can_proliferation  #может ли размножаться true - может, false - не может
        self.children_amount = 0 #количество потомков
        self.steps_amount = 0   #количество шагов для каждой шара
        self.steps_max = 10000 #максимальное количество шагов шара
        self.color = (128, 128, 128) #начальный серый цвет
        self.view_color = (128, 128, 128) #цвет отображения на экране
        self.dir = random.randint(0,7) #0-7 значений направления движения клетки


        self.satiety_time = 5 #5 секунд для сытости
        self.hunger_time = 10 #10 секунд голода
        self.spawn_time = 3 #3 секунд ожидания до спавна
        self.can_move = False #Может или нет двигаться клетка, сделано для новых клеток чтобы был кулдаун движения
        self.steps_skip = 5 #Сколько шагов после появления пропустить, чтобы не задеть родителей

        self.user_impact = [0,0] #какое действие было совершено управляющей программой или пользвателем.
        #Виды переходов движения




        self.properties_list = {
                'id_cell':self.id_cell,
                'x' : self.x,
                'y' :self.y ,
                'dx' : self.dx,
                'dy' : self.dy,
                'radius' : self.radius,
                'view_field' : self.view_field,
                'satiety' : self.satiety,
                'dir': self.dir,
                'color': self.color,
                'steps_amount': self.steps_amount,
                'steps_max': self.steps_max,
                'can_colide' : self.can_colide,
                'last_colision_time' : self.last_colision_time,
                'cant_colide_period': self.cant_colide_period,
                'can_proliferation' : self.can_proliferation,
                'satiety_time':self.satiety_time,
                'hunger_time':self.hunger_time,
                'spawn_time':self.spawn_time,
                'can_move':self.can_move,
                'creation_time':self.creation_time,
                'children_amount':self.children_amount,
                'steps_skip':self.steps_skip,
                'user_impact':self.user_impact,



        }

class Cell(Cell_properties):
    global START_TIME
    def __init__(self,x,y,dx,dy,radius, view_field, satiety, can_colide, last_colision_time, can_proliferation,  id):
      super().__init__(x,y,dx,dy,radius, view_field, satiety, can_colide, last_colision_time, can_proliferation, id)
      self.dir = 1
      # self.satiety_time = self.properties_list['satiety_time']
      # self.hunger_time = self.properties_list['hunger_time']
      # self.properties_list = self.get_Properties_List()

    def move1(self):

        #rnd = random.randint(1,8)
        #print(rnd)

        if self.properties_list['dir'] == 0:
            self.moveX_positive()
        elif self.properties_list['dir'] == 1:
            self.moveXY1()
        elif self.properties_list['dir'] == 2:
            self.moveY_positive()
        elif self.properties_list['dir'] == 3:
            self.moveXY2()
        elif self.properties_list['dir'] == 4:
            self.moveX_negative()
        elif self.properties_list['dir'] == 5:
            self.moveXY3()
        elif self.properties_list['dir'] == 6:
            self.moveY_negative()
        elif self.properties_list['dir'] == 7:
            self.moveXY4()
    def change_dir(self,is_rnd=False,dir = 0):

        if is_rnd:
            self.properties_list['dir'] = random.randint(0,7)
        else:
            self.properties_list['dir'] = dir

    def move(self):
        #не проверяется, если клетка не может двигаться
        if not self.properties_list['can_move']:
            return
        self.properties_list['x'] += self.properties_list['dx']
        self.properties_list['y'] += self.properties_list['dy']
    def bounce(self):
        self.properties_list['dx']*=-1
        self.properties_list['dy']*=-1
    def xbounce(self):
        self.properties_list['dx']*=-1
    def ybounce(self):
        self.properties_list['dy']*=-1

    def moveX_positive(self):
        self.properties_list['x'] += self.properties_list['dx']
    def moveX_negative(self):
        self.properties_list['x'] -= self.properties_list['dx']
    def moveY_positive(self):
        self.properties_list['y'] -= self.properties_list['dy']
    def moveY_negative(self):
        self.properties_list['y'] += self.properties_list['dy']
    def moveXY1(self):
        self.properties_list['x'] += self.properties_list['dx']*1#0.5
        self.properties_list['y'] -= self.properties_list['dy']*1#0.5
    def moveXY2(self):
        self.properties_list['x'] -= self.properties_list['dx']*1#0.5
        self.properties_list['y'] -= self.properties_list['dy']*1#0.5
    def moveXY3(self):
        self.properties_list['x'] -= self.properties_list['dx']*1#0.5
        self.properties_list['y'] += self.properties_list['dy']*1#0.5
    def moveXY4(self):
        self.properties_list['x'] += self.properties_list['dx']*1#0.5
        self.properties_list['y'] += self.properties_list['dy']*1#0.5

    def check_satiety(self):
        #не проверяется, если клетка не может двигаться
        if not self.properties_list['can_move']:
            return
        #print(self.properties_list['satiety_time']+self.properties_list['hunger_time'], self.satiety_time+self.hunger_time)
        #уменьшение времени. сумма времени + секунды прошедшие после столкновения больше стандартной суммы времени
        #15+1 > 15
        #14+2 > 15
        #...
        sum_time = self.properties_list['satiety_time']+self.properties_list['hunger_time']
        if sum_time + int(give_me_time()- START_TIME - self.properties_list['creation_time'] - self.properties_list['last_colision_time']) > self.satiety_time+self.hunger_time:
            if self.properties_list['satiety_time'] > 0:
                #print("УМЕНЬШЕНИЕ ВРЕМЕНИ")
                self.properties_list['satiety_time']-=1
            elif self.properties_list['hunger_time']>0:
                #print("УМЕНЬШЕНИЕ ВРЕМЕНИ")
                self.properties_list['hunger_time']-=1

        #Установка значения состояния голода
        if self.properties_list['satiety_time']==0 and self.properties_list['satiety'] != [0,1,0]:
            self.properties_list['satiety'] = [0, 1, 0]

        #Установка значения состояния смерти
        elif self.properties_list['hunger_time']==0 and self.properties_list['satiety'] != [0,0,1]:
            self.properties_list['satiety'] = [0, 0, 1]


    def check_can_colide_parameters(self):
        # if self.properties_list['children_amount']==0:
        #     print(give_me_time(), START_TIME, self.properties_list['creation_time'], self.properties_list['last_colision_time'])
        #     print(give_me_time() - START_TIME - self.properties_list['creation_time']  + self.properties_list['last_colision_time'])
        if  not self.properties_list['can_colide'] and \
                ( (give_me_time() - START_TIME - self.properties_list['creation_time']  - self.properties_list['last_colision_time']) > self.properties_list['cant_colide_period']):
            self.properties_list['can_colide'] = True




        # else:
        #     self.properties_list['color'] = (0, 125, 125)

        #print(self.properties_list['can_colide'])
    #Проверка счетчика времени начала движения
    def check_can_move(self):
        #если уже может двигаться то ничего не происходит
        if self.properties_list['can_move']:
            return
        #постепенное вычитание посекундно из времени спавна
        if  self.properties_list['spawn_time'] + int(give_me_time()- START_TIME  - self.properties_list['creation_time'] - self.properties_list['last_colision_time'])>self.spawn_time:
            self.properties_list['spawn_time']-=1
            #Время вышло
            if self.properties_list['spawn_time'] == 0:
                self.properties_list['satiety'] = [0, 0, 1]

    def check_color(self):
        # if self.properties_list["id_cell"]== TARGET_CELL_ID:
        #     self.view_color = (0, 255, 0)
        #     return

        #обычный бирюзовый цвет клетки
        if  self.properties_list['satiety'] == [1, 0, 0] and \
                self.properties_list['can_colide'] == True and \
                self.properties_list['can_move'] == True:
            self.properties_list['color'] = (0, 125, 125)
            self.view_color = (0, 125, 125)

            # наступил голод
        # фиолетовый
        #Должно идти выше чем покраска шара в красный при недавнем столкновении, т.к. важнее и иначе красный будет перекрывать его
        elif self.properties_list['satiety'] == [0, 1, 0]:
            self.properties_list['color'] = (255, 0, 255)
            self.view_color = (255, 0, 255)

        #потенциально скоро погибнет, если еще раз в этом состоянии столкнется
        #красный
        elif self.properties_list['can_colide'] == False and self.properties_list['can_move'] == True:
            self.properties_list['color'] = (255, 0, 0)
            self.view_color = (255, 0, 0)
        #мертвый шар
        #черный
        elif self.properties_list['satiety'] == [0,0,1]:
            self.properties_list['color'] = (0, 0, 0)
            self.view_color = (0, 0, 0)
    def check_steps(self):
        #превышено максимальное количество шагов
        if self.properties_list['steps_amount']>self.properties_list['steps_max']:
            self.properties_list['satiety'] = [0, 0, 1]

        #
        # #если время с последней коллизии больше времени сытости то меняем состяние на голод
        # if time.time() - self.properties_list['last_colision_time']> self.properties_list['satiety_time'] and \
        #         self.properties_list['satiety'] != [0,1,0]:
        #     #print('смена на голод')
        #     self.properties_list['satiety'] = [0,1,0]
        # # если время с последней коллизии больше времени голода то меняем состяние на смерть
        # if time.time() - self.properties_list['last_colision_time'] > self.properties_list['hunger_time'] + self.properties_list['satiety_time']  and \
        #         self.properties_list['satiety'] != [0,0,1]:
        #     #print('смена на смерть')
        #     self.properties_list['satiety'] = [0, 0, 1]

#функция проверки поллизий
def is_check_colision(cell1, cell2):
    #потенциальные шары для столкновения. Условие обратное - для пропуска НЕ ПОТЕНЦИАЛЬНЫХ ШАРОВ
    if not(cell1.properties_list['x'] + cell1.properties_list['radius'] > \
            cell2.properties_list['x'] - cell2.properties_list['radius']):
        return False

    #вычисление разницы по x, y и суммы радиусов
    xdif = abs(cell1.properties_list['x'] - cell2.properties_list['x'])
    ydif = abs(cell1.properties_list['y'] - cell2.properties_list['y'])
    sum_radius = cell1.properties_list['radius'] + cell2.properties_list['radius']
    # Коллизия шаров (расстояние между клетками меньше суммы их радиусов)
    if xdif ** 2 + ydif ** 2 <= sum_radius ** 2:
        return True
    return False

#создание клетки в свободном месте
def create_cell( x=None,y=None):
    global cell_list, id_cell, positions_list

    dx = 1#-1 if random.randint(0, 1) == 0 else 1
    dy = 1#-1 if random.randint(0, 1) == 0 else 1


    if x is None and y is None:
        # берем случайный элемент из списка возможных позиций [x,y]
        posx_posy = random.choice(positions_list)
        positions_list.remove(posx_posy)
        cell_list.append(Cell(posx_posy[0], posx_posy[1], dx, dy, RADIUS, 2*RADIUS, [1, 0, 0], False, give_me_time(), False,id_cell))
        id_cell+=1

        return
    cell_list.append(Cell(x,y, dx, dy,RADIUS,2*RADIUS,[1,0,0],False, give_me_time(),False, id_cell))
    id_cell += 1
    #print("Создана!!!",cell.properties_list)


def make_cell_dead(cell):
    cell.properties_list['satiety']=[0,0,1]
def set_collision_values(cell):
    # print(cell.properties_list['id_cell'],give_me_time(),START_TIME,cell.properties_list['creation_time'], give_me_time(give_me_time()-START_TIME - cell.properties_list['creation_time']))
    cell.properties_list['last_colision_time'] =give_me_time(give_me_time()-START_TIME - cell.properties_list['creation_time'])#+ cell.properties_list['creation_time']
    cell.properties_list['satiety'] = [1, 0, 0]
    cell.properties_list['can_colide'] = False
    cell.properties_list['satiety_time'] = cell.satiety_time
    cell.properties_list['hunger_time'] = cell.hunger_time

    #cell.move()

def saving_to_db(values_list=[], is_last=False):
    global save_data_list, last_save_time, SAVE_PERIOD
    #Внутренняя функция сохранения двумерного списка данных в таблицу
    def saving_2d_list():
        global save_data_list
        for sublist in save_data_list:
           #print(sublist)
            DB_program.insert_db(row_names, sublist)
        DB_program.commit()
        save_data_list = []

    #Сохранение перед окончанием симуляции
    if is_last:
        #print (save_data_list)
        saving_2d_list()
        DB_program.make_csv_file()
        #DB_program.select_everything()
        DB_program.close()
        save_data_list=[]
        return

    save_data_list.append(values_list)

    #условие периодичного сохранения
    if  give_me_time() - last_save_time>SAVE_PERIOD:
        last_save_time = give_me_time()
        #print (save_data_list)
        saving_2d_list()
        return


is_can_move = True
def input_user_dir(dir):
    global is_can_move
    # смена направления движения для управляемой клетки

    if is_with_user and TARGET_CELL.properties_list['dir']!=dir and is_can_move:
        is_can_move = False

        TARGET_CELL.properties_list['user_impact']=[TARGET_CELL.properties_list['dir'],dir]
        #print(f"Значение таргета {TARGET_CELL.properties_list['user_impact']}")
        TARGET_CELL.change_dir(is_rnd=False, dir=dir)
        time.sleep(0.1)
        is_can_move = True

def display_info(info):
    font = pygame.font.Font(None, 30)

    score_text = font.render("Количество клеток на поле: " + str(info[0]), True, BLACK)
    screen.blit(score_text, (10, HEIGHT + 50))
    score_text = font.render("Потомки: " +str(info[1]), True, BLACK)
    screen.blit(score_text, (10, HEIGHT+100))
    score_text = font.render("Время жизни клетки: " + str(info[2]), True, BLACK)
    screen.blit(score_text, (200, HEIGHT + 100))
    # render text
    # label = myfont.render("Some text!", 1, (255, 255, 0))
    # screen.blit(label, (100, 100))







# for game_number in range(5000):
START_TIME = give_me_time()
BLACK = (0, 0, 0)
WHITE = (255,255,255)
BIEGE = (245, 245, 220)
# Инициализация Pygame окна
#размер окна
WIDTH = 500
HEIGHT = 500
RADIUS = 25
DIAMETER = RADIUS *2 + 1
N =15     # Number of cells
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT+150))
pygame.display.set_caption("Cells")
clock = pygame.time.Clock()
is_run = True





#настройки симуляции
is_with_user = input("Ручное управление? (y/n)")
is_with_user = True if is_with_user=="y" else False
#установка горячих клавиш
if is_with_user:
    keyboard.add_hotkey("d", lambda: input_user_dir(0))
    keyboard.add_hotkey("d+w", lambda: input_user_dir(1))
    keyboard.add_hotkey("w", lambda: input_user_dir(2))
    keyboard.add_hotkey("a+w", lambda: input_user_dir(3))
    keyboard.add_hotkey("a", lambda: input_user_dir(4))
    keyboard.add_hotkey("a+s", lambda: input_user_dir(5))
    keyboard.add_hotkey("s", lambda: input_user_dir(6))
    keyboard.add_hotkey("d+s", lambda: input_user_dir(7))



is_chg_dir_rnd = False
if not is_with_user :
    is_chg_dir_rnd = input("Случайно менять направление? (y/n)")
    is_chg_dir_rnd = True if is_chg_dir_rnd == "y" else False

if is_with_user:
    MARK = 'user_'
elif is_chg_dir_rnd:
    MARK = 'chng_rnd_'
else:
    MARK = 'realy_rnd_'
#time.sleep(3)



#подготовка списка для изначального распределения клеток
n_width = WIDTH//DIAMETER  #максимально возмонжое количество клеток распределнных по ширине
n_height = HEIGHT//DIAMETER   #максимально возмонжое количество клеток распределнных по длине
positions_list = []
#Создание списка потенциальных позиций
for y in range(n_height):
    for x in range(n_width):
        positions_list.append([x*DIAMETER + RADIUS, y*DIAMETER + RADIUS])

id_cell = 0 #начальный айди клетки
cell_list = []

#создание начальных клеток
for i in range(N):
    if len(positions_list)==0:
        break
    create_cell()



#целевой (управляемый) шар
TARGET_CELL_ID = random.randint(0,len(cell_list)-1  )
TARGET_CELL = cell_list[TARGET_CELL_ID]


#подготовка Базы Данных
MARK += str(TARGET_CELL_ID)

save_data_list = []     #двумерный список для временного хранения записей в бд
last_save_time = give_me_time() #последнее время сохранения записей в бд
SAVE_PERIOD = 3         #период сохранения данных в бд

DB_program.create_table(mark=MARK)
cell_temp = Cell(0,0, 0, 0, 0, 0, [0, 0, 0], False,  give_me_time(), False,0)
row_names = list(cell_temp.properties_list.keys())
row_names.append("FIELD_WIDTH")
row_names.append("FIELD_HEIGHT")
del cell_temp
row_values = []



while is_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False
            saving_to_db(is_last=True)
            break


    # if keyboard.is_pressed('right arrow') and keyboard.is_pressed('up arrow'):  # if key 'q' is pressed
    #     input_user_dir(1)
    # elif (keyboard.is_pressed('left arrow') and keyboard.is_pressed('up arrow')):
    #     input_user_dir(3)
    # elif (keyboard.is_pressed('left arrow') and keyboard.is_pressed('down arrow')):
    #     input_user_dir(5)
    # elif (keyboard.is_pressed('right arrow') and keyboard.is_pressed('down arrow')):
    #     input_user_dir(7)
    screen.fill((255, 255, 255))

    #конец программы
    if len (cell_list)<2:
        is_run = False
        saving_to_db(is_last= True)
        break
    #целевая клетка умерла
    if TARGET_CELL.properties_list['satiety'] == [0,0,1]:
        is_run = False
        saving_to_db(is_last= True)
        break



    if is_chg_dir_rnd:
        TARGET_CELL.properties_list['user_impact'] = [0,0]
        if not random.randint(0,20):
            new_dir = random.randint(0,7)
            TARGET_CELL.properties_list['user_impact'] = [TARGET_CELL.properties_list['dir'], new_dir]
            TARGET_CELL.change_dir(is_rnd=False,dir = new_dir)

    #print(len (cell_list))

    #проход по всему списку шаров
    for iter1, cell1 in enumerate(cell_list):
        # if TARGET_CELL.properties_list["user_impact"]!=[0,0]:
        #     print(TARGET_CELL.properties_list)

        #проверка на максимальное количество шагов
        cell1.check_steps()
        #проверка на голод
        cell1.check_satiety()
        cell1.check_can_colide_parameters()
        #Если время ожидания спавна вышло - умирает
        cell1.check_can_move()


        #проверка на смерть
        #if cell1.properties_list['id_cell']!=0 and cell1.properties_list['id_cell']!=1 and cell1.properties_list['satiety'] == [0,0,1]:     #6 параметр == satiety, сытость. Если равна 0,0,1 (последний параметр равен 1, то смерть шара)
        if  cell1.properties_list['satiety'] == [0,0,1]:
            del cell_list[iter1]
            continue

        # проверка на столкновение с краем карты
        #по X
        if cell1.properties_list['x'] - cell1.properties_list['radius'] < 0:
            #print(f"Левая граница, id cell = {cell1.properties_list['id_cell']}")

            #движение под углом
            if cell1.properties_list['dir']==3 :
                dir = 1      #(cell1.properties_list['dir']+2)%8
            elif cell1.properties_list['dir']==5:
                dir = 7     #(cell1.properties_list['dir']-2)%8
            # прямое движение или не включенные случаи
            else:
                dir = 0

            #print(cell1.properties_list['dir'], dir, f"id_cell = {cell1.properties_list['id_cell']}")
            cell1.change_dir(is_rnd=False, dir = (dir))
            #cell1.moveX_positive()
            # cell1.xbounce()

        if cell1.properties_list['x'] + cell1.properties_list['radius'] > WIDTH :
           # print(f"Правая граница, id cell = {cell1.properties_list['id_cell']}")

            # движение под углом
            if cell1.properties_list['dir'] == 1:
                dir = 3  # (cell1.properties_list['dir']+2)%8
            elif cell1.properties_list['dir'] == 7:
                dir = 5  # (cell1.properties_list['dir']-2)%8
            # прямое движение или не включенные случаи
            else:
                dir = 4

            cell1.change_dir(is_rnd=False, dir=(dir))

            # cell1.moveX_negative()
            # cell1.xbounce()
        #По Y
        if cell1.properties_list['y'] - cell1.properties_list['radius'] < 0:
           # print(f"верхняя граница, id cell = {cell1.properties_list['id_cell']}")

            # движение под углом
            if cell1.properties_list['dir'] == 3:
                dir = 5  # (cell1.properties_list['dir']+2)%8
            elif cell1.properties_list['dir'] == 1:
                dir = 7  # (cell1.properties_list['dir']-2)%8
            # прямое движение или не включенные случаи
            else:
                dir = 6

            cell1.change_dir(is_rnd=False, dir=(dir))            # cell1.moveY_positive()
            # cell1.ybounce()
        if cell1.properties_list['y'] + cell1.properties_list['radius'] > HEIGHT:
           # print(f"нижняя граница, id cell = {cell1.properties_list['id_cell']}")

            # движение под углом
            if cell1.properties_list['dir'] == 7:
                dir = 1  # (cell1.properties_list['dir']+2)%8
            elif cell1.properties_list['dir'] == 5:
                dir = 3  # (cell1.properties_list['dir']-2)%8
            # прямое движение или не включенные случаи
            else:
                dir = 2

            cell1.change_dir(is_rnd=False, dir=(dir))            # cell1.moveY_negative()
            # cell1.ybounce()

        #Проверка коллизий
        for iter2 in range(iter1 + 1, len(cell_list)):
            cell2 = cell_list[iter2]

            # вернуть возможность коллизии
            #cell_list[iter1].properties_list['can_colide'] = time.time() - cell_list[iter1].properties_list['last_colision_time'] > cell_list[iter1].properties_list['can_again_colide_time']
            #cell_list[iter2].properties_list['can_colide'] = time.time() - cell_list[iter2].properties_list['last_colision_time'] > cell_list[iter2].properties_list['can_again_colide_time']
            # if  (time.time() - cell_list[iter1].properties_list['last_colision_time'] > cell_list[iter1].properties_list['cant_colide_period']):
            #     cell_list[iter1].properties_list['can_colide'] = True
            # if (time.time() - cell_list[iter2].properties_list['last_colision_time'] > cell_list[iter2].properties_list['cant_colide_period']):
            #     cell_list[iter2].properties_list['can_colide'] = True

            #Проверка True/False - столкнулись ли шары
            #is_colision = is_check_colision(cell_list[iter1], cell_list[iter2])
            #если столкнулись шары - три случая
            # 1)обоим нельзя сталкиваться,
            # 2) одному нельзя сталикваться
            # 3)второму нельзя ставликваться
            # 4)оба могут столкнуться
            if is_check_colision(cell1, cell2) :
                #Пропуск, если клетки не могут двигаться (формально ещё не заспавнились)
                if not cell1.properties_list['can_move']:
                    continue
                if not cell2.properties_list['can_move']:
                    continue

                if not cell1.properties_list['can_colide'] and not cell2.properties_list['can_colide']:
                    make_cell_dead(cell1)
                    make_cell_dead(cell2)
                #если одному из них нельзя сталкиваться
                elif not cell1.properties_list['can_colide']:
                    make_cell_dead(cell1)
                    set_collision_values(cell2)
                #если второму из них нельзя сталкиваться
                elif not cell2.properties_list['can_colide']:
                    make_cell_dead(cell2)
                    set_collision_values(cell1)
                #обработка коллизий обоих
                else :
                    set_collision_values(cell2)
                    set_collision_values(cell1)
                    cell1.properties_list['children_amount']+=1
                    cell2.properties_list['children_amount']+=1


                    x_pos = (cell1.properties_list['x']+cell2.properties_list['x'])/2
                    y_pos = (cell1.properties_list['y']+cell2.properties_list['y'])/2
                    #print("created")
                    create_cell(x_pos, y_pos)



                cell_list[iter1].change_dir(is_rnd=False, dir = (cell_list[iter1].properties_list['dir']+4)%8)
                cell_list[iter2].change_dir(is_rnd=False, dir = (cell_list[iter2].properties_list['dir']+4)%8)

            #Коллизии не было. Проверка если было клетке нельзя двигаться, то она может начинать двигаться
            #наступает как только новая клетка перестала пересекаться с другими живыми
            else:
                if not cell1.properties_list['can_move']:
                    # # Подсчет с кем будет колизия
                    # colisions_count = 0
                    # # кого не учитывать при колизиях
                    # not_counted = 0



                    is_can_move = True
                    for cell in cell_list:
                        if is_check_colision(cell, cell1) and cell.properties_list['id_cell'] != cell1.properties_list["id_cell"]:
                            is_can_move = False



                    #         colisions_count += 1
                    #     if cell.properties_list['can_move']==False:
                    #         not_counted+=1
                    #
                    # if cell1.id == 0:
                    #     print(cell1.id, colisions_count, not_counted, len(cell_list))

                    if is_can_move:
                        cell1.properties_list['can_move'] =True
                        cell1.properties_list['creation_time'] = give_me_time(give_me_time() - START_TIME)
                        cell1.creation_time =   give_me_time(give_me_time() - START_TIME)
                        set_collision_values(cell1)

                if not cell2.properties_list['can_move']:

                    # #Подсчет с кем будет колизия
                    # colisions_count = 0
                    # #кого не учитывать при колизиях
                    # not_counted = 0
                    # for cell in cell_list:
                    #     if is_check_colision(cell, cell2):
                    #         colisions_count += 1
                    #     if cell.properties_list['can_move']==False:
                    #         not_counted+=1
                    #
                    # if cell2.id == 1:
                    #     print (cell2.id, colisions_count,not_counted, len(cell_list))
                    is_can_move = True
                    for cell in cell_list:
                        if is_check_colision(cell, cell2) and cell.properties_list['id_cell'] != cell2.properties_list["id_cell"]:
                            is_can_move = False

                    if is_can_move:
                        # print(cell2.properties_list)
                        # print(cell1.properties_list['cell'])
                        cell2.properties_list['can_move'] =True
                        cell2.properties_list['creation_time'] = give_me_time(give_me_time() - START_TIME)
                        cell2.creation_time =   give_me_time(give_me_time() - START_TIME)
                        set_collision_values(cell2)

        #условие при котором двигать шар
        if cell1.properties_list['steps_skip']==0:
            cell1.move1()
            # увеличение счетчика шагов каждого круга
            cell1.properties_list['steps_amount'] += 1
        elif cell1.properties_list['can_move']==True:
            cell1.properties_list['steps_skip']-=1


        cell1.check_color()


        #запись в БД
        row_values = []
        #print("запись")
        # if cell1.properties_list['id_cell']==TARGET_CELL_ID:
        #     print(cell1.properties_list)
        for val in cell1.properties_list:

            row_values.append(cell1.properties_list[val])
        row_values.append(WIDTH)
        row_values.append(HEIGHT)
        saving_to_db(row_values)

        # print(cell1.properties_list)
        # print(len(cell_list))

    if is_with_user and TARGET_CELL.properties_list['user_impact']!=[0,0]:
        #print(f"зануление значения {TARGET_CELL.properties_list['user_impact']}")
        TARGET_CELL.properties_list['user_impact'] = [0,0]

    # Drawing Rectangle
    pygame.draw.rect(screen, BIEGE, pygame.Rect(0, 0, WIDTH, HEIGHT))
    # Отображение шаров на экране
    for cell in cell_list:
        pygame.draw.circle(screen, cell.view_color, (cell.properties_list['x'], cell.properties_list['y']), cell.properties_list['radius'])
        if cell.properties_list['id_cell']==TARGET_CELL_ID:
            pygame.draw.circle(screen, (0, 255, 0), (cell.properties_list['x'], cell.properties_list['y']),
                               cell.properties_list['radius']/3)
    #pygame.draw.circle(screen, (0,0,0), (50,0), 50)
    info_list = [
                  len(cell_list),
                  TARGET_CELL.properties_list["children_amount"],
                    give_me_time(give_me_time() - TARGET_CELL.properties_list["creation_time"]- START_TIME)
                  ]
    display_info(info_list)

    pygame.display.flip()
    clock.tick(60)  # Ограничение кадров в секунду


pygame.quit()
#is_waiting_input = False
# print('конец симуляции №', game_number+1)
