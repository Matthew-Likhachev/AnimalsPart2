import time
import pygame
import random

class Cell_properties():
  def __init__(self,x=0,y=0,dx=0,dy=0,radius=25, view_field=50, satiety = [1,0,0], can_colide = False, last_colision_time=0, can_proliferation = False):
    #x=0,y=0,dx=0,dy=0,radius=25, view_field=50, satiety = [1,0,0], can_colide = false, last_colision_time=0, can_proliferation = false
    self.x=x
    self.y=y
    self.dx=dx
    self.dy=dy
    self.radius = radius        #размер шара
    self.view_field = view_field  #поле зрения шара
    self.satiety = satiety      #сытость. [1,0,0] – сытая клетка, [0,1,0] – голодная, [0,0,1] – смерть
    self.can_colide = can_colide # true false - может или нет сталкиваться с другими шарами. Если столкнулся - умирает
    self.cant_colide_period = 3 #через 3 секунды снова может сталкиваться
    self.last_colision_time = last_colision_time #последнее время коллизии
    self.can_proliferation=can_proliferation  #может ли размножаться true - может, false - не может

    self.satiety_time = 5 #5 секунд для сытости
    self.hunger_time = 10 #10 секунд голода
    self.spawn_time = 3 #3 секунд ожидания до спавна
    self.can_move = False #Может или нет двигаться клетка, сделано для новых клеток чтобы был кулдаун движения
    #self.hngr_and_stty_time = self.satiety+self.hunger_time

    self.properties_list = {'x' : self.x,'y' :self.y ,
            'dx' : self.dx, 'dy' : self.dy,
            'radius' : self.radius,
            'view_field' : self.view_field,
            'satiety' : self.satiety,
            'can_colide' : self.can_colide,
            'last_colision_time' : self.last_colision_time,
            'can_proliferation' : self.can_proliferation,
            'satiety_time':self.satiety_time,
            'hunger_time':self.hunger_time,
            'cant_colide_period':self.cant_colide_period,
            'spawn_time':self.spawn_time,
            'can_move':self.can_move,

    }
  def get_Properties_List(self):
    return [self.x,self.y ,
            self.dx,self.dy,
            self.radius,
            self.view_field,
            self.satiety,
            self.can_colide,
            self.last_colision_time,
            self.can_proliferation]

class Cell(Cell_properties):
    def __init__(self,x,y,dx,dy,radius, view_field, satiety, can_colide, last_colision_time, can_proliferation):
      super().__init__(x,y,dx,dy,radius, view_field, satiety, can_colide, last_colision_time, can_proliferation)
      # self.satiety_time = self.properties_list['satiety_time']
      # self.hunger_time = self.properties_list['hunger_time']
      #self.properties_list = self.get_Properties_List()
    def move1(self):
        rnd = random.randint(1,8)
        #print(rnd)
        if rnd == 1:
            self.moveX_positive()
        elif rnd == 2:
            self.moveX_negative()
        elif rnd == 3:
            self.moveY_positive()
        elif rnd == 4:
            self.moveY_negative()
        elif rnd == 5:
            self.moveXY1()
        elif rnd == 6:
            self.moveXY2()
        elif rnd == 7:
            self.moveXY3()
        elif rnd == 8:
            self.moveXY4()

    def move(self):
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
        self.properties_list['y'] += self.properties_list['dy']
    def moveY_negative(self):
        self.properties_list['y'] -= self.properties_list['dy']
    def moveXY1(self):
        self.properties_list['x'] += self.properties_list['dx']*0.5
        self.properties_list['y'] += self.properties_list['dy']*0.5
    def moveXY2(self):
        self.properties_list['x'] -= self.properties_list['dx']*0.5
        self.properties_list['y'] += self.properties_list['dy']*0.5
    def moveXY3(self):
        self.properties_list['x'] -= self.properties_list['dx']*0.5
        self.properties_list['y'] -= self.properties_list['dy']*0.5
    def moveXY4(self):
        self.properties_list['x'] += self.properties_list['dx']*0.5
        self.properties_list['y'] -= self.properties_list['dy']*0.5

    def check_satiety(self):
        #print(self.properties_list['satiety_time']+self.properties_list['hunger_time'], self.satiety_time+self.hunger_time)
        #уменьшение времени. сумма времени + секунды прошедшие после столкновения больше стандартной суммы времени
        #15+1 > 15
        #14+2 > 15
        #...
        sum_time = self.properties_list['satiety_time']+self.properties_list['hunger_time']
        if sum_time + int(time.time()-self.properties_list['last_colision_time']) > self.satiety_time+self.hunger_time:
            if self.properties_list['satiety_time'] > 0:
                #print("УМЕНЬШЕНИЕ ВРЕМЕНИ")
                self.properties_list['satiety_time']-=1
            elif self.properties_list['hunger_time']>0:
                #print("УМЕНЬШЕНИЕ ВРЕМЕНИ")
                self.properties_list['hunger_time']-=1

        #Установка значения состояния голода
        if self.properties_list['satiety_time']==0 and self.properties_list['satiety'] != [0,1,0]:
            self.properties_list['satiety'] = [0, 1, 0]

        if self.properties_list['hunger_time']==0 and self.properties_list['satiety'] != [0,0,1]:
            self.properties_list['satiety'] = [0, 0, 1]
    def check_can_colide_parameters(self):
        if (time.time() - self.properties_list['last_colision_time'] > self.properties_list['cant_colide_period']) and \
                not self.properties_list['can_colide']:
            self.properties_list['can_colide'] = True
        #print(self.properties_list['can_colide'])


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
def create_cell(x=None,y=None):
    global cell_list
    if x is None and y is None:
        cell_list.append(Cell(random.uniform(25, WIDTH-25),random.uniform(25, HEIGHT-25), 1, 1, 25, 50, [1, 0, 0], False, time.time(), False))
        return
    #print ("added")
    cell = Cell(random.uniform(25, WIDTH-25),random.uniform(25, HEIGHT-25),1,1,25,50,[1,0,0],False,time.time(),False)
    cell_list.append(cell)

def make_cell_dead(cell):
    cell.properties_list['satiety']=[0,0,1]
def set_collision_values(cell):
    cell.properties_list['last_colision_time'] = time.time()
    cell.properties_list['satiety'] = [1, 0, 0]
    cell.properties_list['can_colide'] = False
    cell.properties_list['satiety_time'] = cell.satiety_time
    cell.properties_list['hunger_time'] = cell.hunger_time

    #cell.move()
#размер окна
WIDTH = 500
HEIGHT = 500

cell_list = []
#создаю 2 клетки
for i in range(25):
    create_cell()
# #одна клетка движется
# cell_list[0].properties_list['dx']=1   #dx
# cell_list[0].properties_list['dy']=1   #dy

# Инициализация Pygame окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()


is_run = True
while is_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False

    screen.fill((255, 255, 255))

    #конец программы
    if len (cell_list)<2:
        is_run = False
        break
    #print(len (cell_list))

    #проход по всему списку шаров
    for iter1, cell1 in enumerate(cell_list):
        #проверка на голод
        cell1.check_satiety()
        cell1.check_can_colide_parameters()
        #проверка на смерть
        if cell1.properties_list['satiety'] == [0,0,1]:     #6 параметр == satiety, сытость. Если равна 0,0,1 (последний параметр равен 1, то смерть шара)
            del cell_list[iter1]
            continue

        # проверка на столкновение с краем карты
        #по X
        if cell1.properties_list['x'] - cell1.properties_list['radius'] < 0:
            #cell1.moveX_positive()
            cell1.xbounce()

        if cell1.properties_list['x'] + cell1.properties_list['radius'] > WIDTH :
            #cell1.moveX_negative()
            cell1.xbounce()
            # проверка если за картой шар
        #По Y
        if cell1.properties_list['y'] - cell1.properties_list['radius'] < 0:
            #cell1.moveY_positive()
            cell1.ybounce()
        if cell1.properties_list['y'] + cell1.properties_list['radius'] > HEIGHT:
            #cell1.moveY_negative()
            cell1.ybounce()

        #Проверка коллизий
        for iter2 in range(iter1 + 1, len(cell_list)):
            cell1 = cell_list[iter1]
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
            #если столкнулись шары
            if is_check_colision(cell1, cell2) :
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
                    x_pos = (cell1.properties_list['x']+cell2.properties_list['x'])/2
                    y_pos = (cell1.properties_list['y']+cell2.properties_list['y'])/2
                    #print("created")
                    create_cell(x_pos, y_pos)


                cell_list[iter1].bounce()
                cell_list[iter2].bounce()

        cell1.move()

    # Отображение шаров на экране
    for cell in cell_list:
        pygame.draw.circle(screen, (0,125,125), (cell.properties_list['x'], cell.properties_list['y']), cell.properties_list['radius'])
        #print()

    pygame.display.flip()
    clock.tick(60)  # Ограничение кадров в секунду
    # print(pygame.time.get_ticks())
pygame.quit()

print('конец программы')
