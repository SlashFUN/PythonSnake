from tkinter import *
import random
class Segment(object):

    def __init__(self,x,y):  # __init__ метод перегрузки оператора (конструктор) self - екземпляр самого объекта
        self.instance = grass.create_rectangle(
                        x, y,
                         x+SEG_SIZE, y+SEG_SIZE,
                         fill="yellow")
class Snake(object):
    def __init__(self, segments):
        self.segments = segments

        # список всіх доступних напрямів
        self.mapping = {"Down": (0, 1), "Up": (0, -1),
                        "Left": (-1, 0), "Right": (1, 0)}
        # Початковий рух - вправо
        self.vector = self.mapping["Right"]

    def move(self): #Рухає змійку в заданому напрямі

        # перебір всіх сегментів крім останнього
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = grass.coords(self.segments[index + 1].instance)
            # задаєм кожному сегменту позицію сегмента який стоїть після нього
            grass.coords(segment, x1, y1, x2, y2)

        # координати сегмента перед "головою"
        x1, y1, x2, y2 = grass.coords(self.segments[-2].instance)

        # розміщуєм "голову" в напрямку який вказаний вектором руху (right)
        grass.coords(self.segments[-1].instance,
                     x1 + self.vector[0] * SEG_SIZE,
                     y1 + self.vector[1] * SEG_SIZE,
                     x2 + self.vector[0] * SEG_SIZE,
                     y2 + self.vector[1] * SEG_SIZE)

    def change_direction(self, event):
        #Зміна напряму руху

        # event передасть нам символ натиснутої клавіші
        # І якщо ця клавіша в доступних напрямках
        # змінюєм напрямок
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def add_segment(self):


        # определяем последний сегмент
        last_seg = grass.coords(self.segments[0].instance)

        # определяем координаты куда поставить следующий сегмент
        x = last_seg[2] - SEG_SIZE  #починаючи з х2 (кінцевої точки) сегменту
        y = last_seg[3] - SEG_SIZE  #починаючи з y2 (кінцевої точки) сегменту

        # добавляєм змійці ще один сегмент в заданих координатах
        self.segments.insert(0, Segment(x, y))

# ширина экрана
WIDTH = 1200
# высота экрана
HEIGHT = 720
# Размер сегмента змейки
SEG_SIZE = 20
# Переменная отвечающая за состояние игры
IN_GAME = True

def create_block():
    #Створює блок (яблоко) в случайній позиції
    global BLOCK
    posx = SEG_SIZE * (random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
    posy = SEG_SIZE * (random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))

    # блок - червоний круг
    BLOCK = grass.create_oval(posx, posy,
                          posx + SEG_SIZE,
                          posy + SEG_SIZE,
                          fill="red")


def main():
    global IN_GAME

    if IN_GAME:
        # Рухаєм змійку
        s.move()

        # Координати голови
        head_coords = grass.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # Зіткнення з межами сітки
        if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # з`їдання яблук
        elif head_coords == grass.coords(BLOCK):
            s.add_segment()
            grass.delete(BLOCK)
            create_block()

        # Самопоїдання
        else:
            # проходим по всім сегментам змії
            for index in range(len(s.segments) - 1):
                if grass.coords(s.segments[index].instance) == head_coords:
                    IN_GAME = False
        root.after(100, main)
    # Програш
    else:
        grass.create_text(WIDTH / 2, HEIGHT / 2,
                      text="GAME OVER!",
                      font="Arial 40",
                      fill="#ff0000")


root = Tk() #create window
root.title("Python Snake") #window tittle
# creating Canvas example and make window green
grass = Canvas(root, width=WIDTH, height=HEIGHT, bg="blue")
grass.grid() #Сітка
grass.focus_set()
# создаем набор сегментов
segments = [Segment(SEG_SIZE, SEG_SIZE),
            Segment(SEG_SIZE*2, SEG_SIZE),
            Segment(SEG_SIZE*3, SEG_SIZE)]
# собственно змейка
s = Snake(segments)
# Make focus on Canvas to click on items
grass.focus_set()
grass.bind("<Key>", s.change_direction)

create_block()
main()
root.mainloop()