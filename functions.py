import copy
import os
import time
import pygame
import random
import sys
vector_roles=[0,1,1,0,0,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,0]+[0 for _ in range(1,12)]
os.environ['TERM'] = 'xterm-256color'
class Matrix:
    def __init__(self,n):
        self.n=n
        self.matrix=[[0 for _ in range(n)] for _ in range(n)]
    def __init__(self,matrix):
        self.n=len(matrix)
        self.matrix=copy.deepcopy(matrix)

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.matrix:
            print(" ".join(map(str, row)))                # map - применяет функцию str к каждому элементу из списка row
                                                          # join - метод строк, который объединяет все элементы списка, соединяя их пробелом
    def change_value(self, row, col):
        if 0 <= row < self.n and 0 <= col < self.n:
            self.matrix[row][col] = 1 if self.matrix[row][col]==0 else 0
        else:
            print("Некорректные индексы")

    def get_amount_neighbors_life(self, row, col):
        neighbors_count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                # Проверяем, что соседние клетки находятся в пределах матрицы и не выходят за ее границы
                if 0 <= i < self.n and 0 <= j < self.n:
                    # Проверяем, что значение соседней клетки равно 1
                    if self.matrix[i][j] == 1:
                        neighbors_count += 1
        if(self.matrix[row][col]==1):
            neighbors_count-=1
        return neighbors_count

    def get_value_neighbors_fon_neiman(self, row, col):
        value=0
        value += self.matrix[row][col] *16
        if 0<=row-1<self.n:
            value+=self.matrix[row - 1][col]*2

        if 0<=row+1<self.n:
            value += self.matrix[row + 1][col]*4
        if 0 <= col - 1 < self.n:
            value += self.matrix[row][col - 1] * 8
        if 0 <= col + 1 < self.n:
            value += self.matrix[row][col + 1] * 1
        return value



    def run_one_takt_life(self):
        matrix=copy.deepcopy(self.matrix)
        for i in range(self.n):
            for j in range(self.n):
                amount=self.get_amount_neighbors_life(i, j)
                if(self.matrix[i][j]==0 and amount==3):
                    matrix[i][j]=1
                else:
                    if(self.matrix[i][j]==1 and (amount!=2 and amount!=3)):
                        matrix[i][j]=0
        self.matrix=matrix

    def run_one_takt_roles(self):
        matrix = copy.deepcopy(self.matrix)
        for i in range(1,self.n-1):
            for j in range(1,self.n-1):
                amount = self.get_value_neighbors_fon_neiman(i, j)
                matrix[i][j] = vector_roles[amount]
        self.matrix = matrix


def start(binary_grid):
    matrix_obj=Matrix(binary_grid)
    while (True):
        matrix_obj.run_one_takt_life()
        time.sleep(1)
    return 1
def GetSize():
    print("Введите размер квадратного поля: ")
    try:
        size_grid = int(input())
    except ValueError:
        size_grid = 20
        print("Неверный ввод. Задано значение по умолчанию.")
    return size_grid
def GetPause():
    print("Введите продолжительность такта в секундах (<10): ")
    try:
        p = float(input())
    except ValueError:
        p = 0.5
        print("Неверный ввод. Задано значение по умолчанию.")

    if p>10:
       p=10
    return p
def GetChooseMode():
    print("Для задания начальных значений самостоятельно, нажмите 1.")
    print("Иначе, начальные условья будут созданы автоматически")
    try:
        p = int(input())
    except ValueError:
        p = 0
        print("Неверный ввод. Задано значение по умолчанию.")
    if p==1:
        return True
    else:
        return False


size_grid=GetSize()
pause=GetPause()
flag_manual_mode=GetChooseMode()
window_width = 600
window_height = window_width*4//3  # 4/3 размера окна
cell_size=window_width//size_grid
# размеры элипсов
start_x=50
start_y=30
start_width=200
start_height=80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (153, 0, 0)

def click_inside_start(x,y):
    return (x - start_x - start_width / 2) ** 2 / (start_width / 2) ** 2 + (y - start_y - start_height / 2) ** 2 / (
            start_height / 2) ** 2 <= 1
def click_iside_stop(x,y):
    return (x - (start_x + 300) - start_width / 2) ** 2 / (start_width / 2) ** 2 + (
                            y - start_y - start_height / 2) ** 2 / (
                            start_height / 2) ** 2 <= 1
def draw_start( screen,font):
    pygame.draw.ellipse(screen, GREEN, (start_x, start_y, start_width, start_height))
    start_text = font.render("Старт", True, BLACK)
    screen.blit(start_text, (start_x+65, start_y+25))
def draw_stop(screen,font):
    pygame.draw.ellipse(screen, RED, (start_x + 300, start_y, start_width, start_height))
    start_text = font.render("Стоп", True, BLACK)
    screen.blit(start_text, (start_x + 300 + 65, start_y + 25))


def draw_greed(screen,grid_colors):
    for row in range(size_grid):
        for col in range(size_grid):
            pygame.draw.rect(screen, grid_colors[row][col],
                             (col * cell_size, row * cell_size + window_height // 4, cell_size, cell_size))

    # Рисуем горизонтальные и вертикальные линии сетки
    for i in range(size_grid + 1):
        pygame.draw.line(screen, BLACK, (0, (i * cell_size + window_height // 4)),
                         (window_width, i * cell_size + window_height // 4), 1)  # Горизонтальные линии
        pygame.draw.line(screen, BLACK, (i * cell_size, window_height // 4), (i * cell_size, window_height),
                         1)  # Вертикальные линии