import math, heapq, time
import pygame
import sys
import numpy as np


def blocked(cX, cY, dX, dY, matrix):
    if cX + dX < 0 or cX + dX >= matrix.shape[0]:
        return True
    if cY + dY < 0 or cY + dY >= matrix.shape[1]:
        return True
    if dX != 0 and dY != 0:
        if matrix[cX + dX][cY] == 1 and matrix[cX][cY + dY] == 1:
            return True
        if matrix[cX + dX][cY + dY] == 1:
            return True
    else:
        if dX != 0:
            if matrix[cX + dX][cY] == 1:
                return True
        else:
            if matrix[cX][cY + dY] == 1:
                return True
    return False


def heuristic(start, goal, hchoice):
    if hchoice == 1:
        xdist = math.fabs(goal[0] - start[0])
        ydist = math.fabs(goal[1] - start[1])
        if xdist > ydist:
            return 14 * ydist + 10 * (xdist - ydist)
        else:
            return 14 * xdist + 10 * (ydist - xdist)
    if hchoice == 2:
        return math.sqrt((goal[0] - start[0]) ** 2 + (goal[1] - start[1]) ** 2)


def method(matrix, start, goal, hchoice):
    close_list = set()
    came_from = {}
    gn = {start: 0}
    fn = {start: heuristic(start, goal, hchoice)}

    open_list = []

    heapq.heappush(open_list, (fn[start], start))

    starttime = time.time()

    while open_list:

        current = heapq.heappop(open_list)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::]
            #print(gscore[goal])
            endtime = time.time()
            return (path, round(endtime - starttime, 6)), close_list, open_list 

        close_list.add(current)
        for dX, dY in [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]:

            if blocked(current[0], current[1], dX, dY, matrix):
                continue

            neighbour = current[0] + dX, current[1] + dY

            if hchoice == 1:
                if dX != 0 and dY != 0:
                    tentative_gn = gn[current] + 14
                else:
                    tentative_gn = gn[current] + 10
            elif hchoice == 2:
                if dX != 0 and dY != 0:
                    tentative_gn = gn[current] + math.sqrt(2)
                else:
                    tentative_gn = gn[current] + 1

            if (
                neighbour in close_list
            ):  # and tentative_g_score >= gscore.get(neighbour,0):
                continue

            if tentative_gn < gn.get(neighbour, 0) or neighbour not in [i[1] for i in open_list]:
                came_from[neighbour] = current
                gn[neighbour] = tentative_gn
                fn[neighbour] = tentative_gn + heuristic(
                    neighbour, goal, hchoice
                )
                heapq.heappush(open_list, (fn[neighbour], neighbour))
                step(current, 6)
        endtime = time.time()
    return (0, round(endtime - starttime, 6))


# Definisi grid/matrix (0 = jalan, 1 = rintangan, 2 = start, 3 = goal)
matrix = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
)

# Konfigurasi otomatis dari matrix
CELL_SIZE = 30
GRID_HEIGHT, GRID_WIDTH = matrix.shape

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
GRAY = (200, 200, 200)

# Inisialisasi Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption("JPS Jump Animation")
clock = pygame.time.Clock()

# Fungsi bantu
def blocked(x, y, dx, dy, matrix):
    tx, ty = x + dx, y + dy
    if 0 <= tx < GRID_WIDTH and 0 <= ty < GRID_HEIGHT:
        return matrix[ty][tx] == 1
    return True

def dblock(x, y, dx, dy, matrix):
    return blocked(x, y, dx, 0, matrix) or blocked(x, y, 0, dy, matrix)

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            value = matrix[y][x]
            if value == 1:
                color = BLACK
            elif value == 2:
                color = GREEN
            elif value == 3:
                color = BLUE
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_cell(x, y, color):
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def step(posisi, color=0, delay=60,):
    y, x = posisi
    draw_cell(x, y, colors[color])
    pygame.display.flip()
    pygame.time.delay(delay)

colors = {
    0: "#FFFFFF",  # Ruang kosong
    1: "#17252a",  # Rintangan
    2: "#3aafa9",  # Start
    3: "#FF0021",  # Goal
    4: "#3f6184",  # Garis
    5: "#FFFF00",  # Open List (kuning)
    6: "#FFA500",  # Close List (oranye)
    7: "#778899",  # Warna abu-abu
    8: "#e8175d",  # Warna pink
}

# Main loop
def main():
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if (matrix[i][j] == 2):
                start = (i, j)
            elif (matrix[i][j] == 3):
                goal = (i, j)

    draw_grid()
    pygame.display.flip()

    path = method(matrix, start, goal, 2)  # Mulai dengan arah diagonal kanan bawah

    # Loop agar window tetap terbuka
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main()