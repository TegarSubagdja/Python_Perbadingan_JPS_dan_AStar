import pygame
import sys
import numpy as np

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

def animate_step(x, y, delay=60):
    draw_cell(x, y, GREEN)
    pygame.display.flip()
    pygame.time.delay(delay)

# Fungsi jump() dengan animasi
def jump(cX, cY, dX, dY, matrix, goal):
    nX = cX + dX
    nY = cY + dY

    if blocked(cX, cY, dX, dY, matrix):
        return None
    if (nX, nY) == goal:
        animate_step(nX, nY)
        return (nX, nY)

    oX, oY = nX, nY

    if dX != 0 and dY != 0:
        while True:
            animate_step(oX, oY)
            if ((not blocked(oX, oY, -dX, dY, matrix) and blocked(oX, oY, -dX, 0, matrix)) or
                (not blocked(oX, oY, dX, -dY, matrix) and blocked(oX, oY, 0, -dY, matrix))):
                return (oX, oY)

            if (jump(oX, oY, dX, 0, matrix, goal) is not None or
                jump(oX, oY, 0, dY, matrix, goal) is not None):
                return (oX, oY)

            oX += dX
            oY += dY

            if blocked(oX, oY, 0, 0, matrix) or dblock(oX, oY, dX, dY, matrix):
                return None
            if (oX, oY) == goal:
                animate_step(oX, oY)
                return (oX, oY)
    else:
        if dX != 0:
            while True:
                animate_step(oX, nY)
                if ((not blocked(oX, nY, dX, 1, matrix) and blocked(oX, nY, 0, 1, matrix)) or
                    (not blocked(oX, nY, dX, -1, matrix) and blocked(oX, nY, 0, -1, matrix))):
                    return (oX, nY)
                oX += dX
                if blocked(oX, nY, 0, 0, matrix):
                    return None
                if (oX, nY) == goal:
                    animate_step(oX, nY)
                    return (oX, nY)
        else:
            while True:
                animate_step(nX, oY)
                if ((not blocked(nX, oY, 1, dY, matrix) and blocked(nX, oY, 1, 0, matrix)) or
                    (not blocked(nX, oY, -1, dY, matrix) and blocked(nX, oY, -1, 0, matrix))):
                    return (nX, oY)
                oY += dY
                if blocked(nX, oY, 0, 0, matrix):
                    return None
                if (nX, oY) == goal:
                    animate_step(nX, oY)
                    return (nX, oY)

    return jump(nX, nY, dX, dY, matrix, goal)

# Menemukan posisi start dan goal dari matrix
def find_start_goal(matrix):
    start = None
    goal = None
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if matrix[y][x] == 2:
                start = (x, y)
            elif matrix[y][x] == 3:
                goal = (x, y)
    return start, goal

# Main loop
def main():
    start, goal = find_start_goal(matrix)

    draw_grid()
    pygame.display.flip()

    jump(start[0], start[1], 1, 1, matrix, goal)  # Mulai dengan arah diagonal kanan bawah

    # Loop agar window tetap terbuka
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main()
