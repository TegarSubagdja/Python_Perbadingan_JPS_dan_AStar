import math, time, heapq
import pygame
import sys
import numpy as np

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


def blocked(currentX, currentY, moveX, moveY, matrix):
    if currentX + moveX < 0 or currentX + moveX >= matrix.shape[0]:
        return True
    if currentY + moveY < 0 or currentY + moveY >= matrix.shape[1]:
        return True
    if moveX != 0 and moveY != 0:
        if matrix[currentX + moveX][currentY] == 1 and matrix[currentX][currentY + moveY] == 1:
            return True
        if matrix[currentX + moveX][currentY + moveY] == 1:
            return True
    else:
        if moveX != 0:
            if matrix[currentX + moveX][currentY] == 1:
                return True
        else:
            if matrix[currentX][currentY + moveY] == 1:
                return True
    return False


def dblock(currentX, currentY, moveX, moveY, matrix):
    if matrix[currentX - moveX][currentY] == 1 and matrix[currentX][currentY - moveY] == 1:
        return True
    else:
        return False


def direction(currentX, currentY, parentX, parentY):
    moveX = int(math.copysign(1, currentX - parentX))
    moveY = int(math.copysign(1, currentY - parentY))
    if currentX - parentX == 0:
        moveX = 0
    if currentY - parentY == 0:
        moveY = 0
    return (moveX, moveY)


def nodeNeighbours(currentX, currentY, parent, matrix):
    neighbours = []
    if type(parent) != tuple:
        for moveX, moveY in [
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]:
            if not blocked(currentX, currentY, moveX, moveY, matrix):
                neighbours.append((currentX + moveX, currentY + moveY))

        return neighbours
    moveX, moveY = direction(currentX, currentY, parent[0], parent[1])

    if moveX != 0 and moveY != 0:
        if not blocked(currentX, currentY, 0, moveY, matrix):
            neighbours.append((currentX, currentY + moveY))
        if not blocked(currentX, currentY, moveX, 0, matrix):
            neighbours.append((currentX + moveX, currentY))
        if (not blocked(currentX, currentY, 0, moveY, matrix)
            or not blocked(currentX, currentY, moveX, 0, matrix)
        ) and not blocked(currentX, currentY, moveX, moveY, matrix):
            neighbours.append((currentX + moveX, currentY + moveY))
        if blocked(currentX, currentY, -moveX, 0, matrix) and not blocked(
            currentX, currentY, 0, moveY, matrix
        ):
            neighbours.append((currentX - moveX, currentY + moveY))
        if blocked(currentX, currentY, 0, -moveY, matrix) and not blocked(
            currentX, currentY, moveX, 0, matrix
        ):
            neighbours.append((currentX + moveX, currentY - moveY))

    else:
        if moveX == 0:
            if not blocked(currentX, currentY, moveX, 0, matrix):
                if not blocked(currentX, currentY, 0, moveY, matrix):
                    neighbours.append((currentX, currentY + moveY))
                if blocked(currentX, currentY, 1, 0, matrix):
                    neighbours.append((currentX + 1, currentY + moveY))
                if blocked(currentX, currentY, -1, 0, matrix):
                    neighbours.append((currentX - 1, currentY + moveY))

        else:
            if not blocked(currentX, currentY, moveX, 0, matrix):
                if not blocked(currentX, currentY, moveX, 0, matrix):
                    neighbours.append((currentX + moveX, currentY))
                if blocked(currentX, currentY, 0, 1, matrix):
                    neighbours.append((currentX + moveX, currentY + 1))
                if blocked(currentX, currentY, 0, -1, matrix):
                    neighbours.append((currentX + moveX, currentY - 1))
    return neighbours


def jump(cX, cY, dX, dY, matrix, goal):
    nX = cX + dX
    nY = cY + dY

    if blocked(cX, cY, dX, dY, matrix):
        return None
    if (nX, nY) == goal:
        step((nX, nY), 5)
        return (nX, nY)

    oX, oY = nX, nY

    if dX != 0 and dY != 0:
        while True:
            step((oX, oY), 5)
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
                step((oX, oY), 5)
                return (oX, oY)
    else:
        if dX != 0:
            while True:
                step((oX, nY), 5)
                if ((not blocked(oX, nY, dX, 1, matrix) and blocked(oX, nY, 0, 1, matrix)) or
                    (not blocked(oX, nY, dX, -1, matrix) and blocked(oX, nY, 0, -1, matrix))):
                    return (oX, nY)
                oX += dX
                if blocked(oX, nY, 0, 0, matrix):
                    return None
                if (oX, nY) == goal:
                    step((oX, nY), 5)
                    return (oX, nY)
        else:
            while True:
                step((nX, oY), 5)
                if ((not blocked(nX, oY, 1, dY, matrix) and blocked(nX, oY, 1, 0, matrix)) or
                    (not blocked(nX, oY, -1, dY, matrix) and blocked(nX, oY, -1, 0, matrix))):
                    return (nX, oY)
                oY += dY
                if blocked(nX, oY, 0, 0, matrix):
                    return None
                if (nX, oY) == goal:
                    step((nX, oY), 5)
                    return (nX, oY)

    return jump(nX, nY, dX, dY, matrix, goal)


def identifySuccessors(currentX, currentY, came_from, matrix, goal):
    successors = []
    neighbours = nodeNeighbours(currentX, currentY, came_from.get((currentX, currentY), 0), matrix)

    for cell in neighbours:
        moveX = cell[0] - currentX
        moveY = cell[1] - currentY

        print(f"movex : {moveX}, movey : {moveY} currenx: {currentX}, currenty: {currentY}")

        jumpPoint = jump(currentX, currentY, moveX, moveY, matrix, goal)

        if jumpPoint != None:
            successors.append(jumpPoint)
        
    return successors


def method(matrix, start, goal, hchoice):

    came_from = {}
    close_list = set()
    gn = {start: 0}
    fn = {start: heuristic(start, goal, hchoice)}

    open_list = []

    heapq.heappush(open_list, (fn[start], start))

    starttime = time.time()

    while open_list:

        current = heapq.heappop(open_list)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data = data[::-1]
            endtime = time.time()
            #print(gn[goal])
            return (data, round(endtime - starttime, 6)), close_list, open_list

        close_list.add(current)

        successors = identifySuccessors(
            current[0], current[1], came_from, matrix, goal
        )

        for successor in successors:
            jumpPoint = successor

            if (
                jumpPoint in close_list
            ):  # and tentative_gn >= gn.get(jumpPoint,0):
                continue

            tentative_gn = gn[current] + lenght(
                current, jumpPoint, hchoice
            )

            if tentative_gn < gn.get(
                jumpPoint, 0
            ) or jumpPoint not in [j[1] for j in open_list]:
                came_from[jumpPoint] = current
                gn[jumpPoint] = tentative_gn
                fn[jumpPoint] = tentative_gn + heuristic(
                    jumpPoint, goal, hchoice
                ) 
                heapq.heappush(open_list, (fn[jumpPoint], jumpPoint))
        endtime = time.time()
    return (0, round(endtime - starttime, 6))


def lenght(current, jumppoint, hchoice):
    moveX, moveY = direction(current[0], current[1], jumppoint[0], jumppoint[1])
    moveX = math.fabs(moveX)
    moveY = math.fabs(moveY)
    lX = math.fabs(current[0] - jumppoint[0])
    lY = math.fabs(current[1] - jumppoint[1])
    if hchoice == 1:
        if moveX != 0 and moveY != 0:
            lenght = lX * 14
            return lenght
        else:
            lenght = (moveX * lX + moveY * lY) * 10
            return lenght
    if hchoice == 2:
        return math.sqrt(
            (current[0] - jumppoint[0]) ** 2 + (current[1] - jumppoint[1]) ** 2
        )
    
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

def step(posisi, color=0, delay=10):
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
    for i in range(0, 15):
        for j in range(0, 15):
            if (matrix[i][j] == 2):
                start = (i, j)
            elif (matrix[i][j] == 3):
                goal = (i, j)

    draw_grid()
    pygame.display.flip()

    print(f"start : {start}, goal : {goal}")

    path = method(matrix, start, goal, 2)  # Mulai dengan arah diagonal kanan bawah
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main()