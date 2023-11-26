
from functions import *
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Клеточный автомат")
font = pygame.font.Font(None, 36)
# Создаем двумерный массив для хранения цвета каждой ячейки сетки
if flag_manual_mode!=False:
    grid_colors = [[WHITE for _ in range(size_grid)] for _ in range(size_grid)]
else:
    grid_colors = [[ WHITE if random.randint(0, 1)==1 else BLACK for _ in range(size_grid)]
                   for _ in range(size_grid)]
    for i in range(size_grid):
        grid_colors[0][i] = WHITE
        grid_colors[size_grid-1][i] = WHITE
        grid_colors[i][0] = WHITE
        grid_colors[i][size_grid-1] = WHITE

started=True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Получаем координаты мыши и определяем, в какую ячейку попали
            x, y = event.pos
            if y >= window_height // 4:
                row = (y - window_height // 4) // cell_size  # Игнорируем верхние 1/4 окна
                col = x // cell_size
                # Меняем цвет ячейки на черный
                if grid_colors[row][col]==WHITE:
                    grid_colors[row][col] = BLACK
                else:
                    grid_colors[row][col] = WHITE
                mouse_buttons = pygame.mouse.get_pressed()


            if click_inside_start(x,y): # внутри старт
                # Позиция мыши находится внутри эллипса
                binary_grid = [[0 if color == WHITE else 1 for color in row] for row in grid_colors]
                matrix_obj = Matrix(binary_grid)
                help_counter=0
                print("Позиция мыши внутри зеленого эллипса")
                while help_counter<8:
                    #help_counter+=1
                    matrix_obj.run_one_takt_roles()
                    grid_colors=[[WHITE if color == 0 else 1 for color in row] for row in  matrix_obj.matrix]
                    draw_greed(screen,grid_colors)
                    time.sleep(pause)
                    pygame.display.flip()
                    events_inside = pygame.event.get()
                    for event_inside in events_inside:
                        if event_inside.type == pygame.MOUSEBUTTONDOWN and event_inside.button == 1:
                            x_inside, y_inside = event_inside.pos
                            if click_iside_stop(x_inside, y_inside):
                                help_counter = 100

            if click_iside_stop(x,y):  # внутри стоп
                started = False
                # Позиция мыши находится внутри эллипса
                print("Позиция мыши внутри красного эллипса")



    screen.fill(WHITE)

    draw_greed(screen,grid_colors)
    # Рисуем зеленую овальную кнопку "Старт"
    draw_start(screen,font)
    draw_stop(screen,font)


    # Обновляем экран
    pygame.display.flip()

pygame.quit()
sys.exit()