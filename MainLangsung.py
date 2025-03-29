import JPS_Komentar
import Astar_Komentar
import numpy as np

# Define the grid manually
# Grid = np.array([
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
#     [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
#     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ])

def blocked(cX, cY, dX, dY, matrix):
    # Memeriksa apakah posisi berada di luar batas matriks
    if cX + dX < 0 or cX + dX >= matrix.shape[0]:
        return True
    if cY + dY < 0 or cY + dY >= matrix.shape[1]:
        return True
        
    # Menangani pergerakan diagonal
    if dX != 0 and dY != 0:
        # Memeriksa apakah kedua sel yang berdekatan terhalang (tidak bisa lewat)
        if matrix[cX + dX][cY] == 1 and matrix[cX][cY + dY] == 1:
            return True
        # Memeriksa apakah sel diagonal target terhalang
        if matrix[cX + dX][cY + dY] == 1:
            return True
    else:
        # Menangani pergerakan lurus (horizontal atau vertikal)
        if dX != 0:  # Pergerakan horizontal
            if matrix[cX + dX][cY] == 1:
                return True
        else:  # Pergerakan vertikal
            if matrix[cX][cY + dY] == 1:
                return True
    return False

def dblock(cX, cY, dX, dY, matrix):
    # Memeriksa apakah kedua sel yang berdekatan dengan gerakan diagonal terhalang
    if matrix[cX - dX][cY] == 1 and matrix[cX][cY - dY] == 1:
        return True
    return False

def jump(cX, cY, dX, dY, matrix, goal):
    # Menghitung posisi berikutnya
    nX = cX + dX
    nY = cY + dY
    
    # Memeriksa apakah posisi berikutnya terhalang atau adalah tujuan
    if blocked(nX, nY, 0, 0, matrix):
        return None
    if (nX, nY) == goal:
        return (nX, nY)

    oX = nX
    oY = nY

    # Menangani pergerakan diagonal
    if dX != 0 and dY != 0:
        while True:
            # Memeriksa tetangga paksa
            if (not blocked(oX, oY, -dX, dY, matrix) and blocked(oX, oY, -dX, 0, matrix)
                or not blocked(oX, oY, dX, -dY, matrix) and blocked(oX, oY, 0, -dY, matrix)):
                return (oX, oY)

            # Memeriksa arah horizontal dan vertikal secara rekursif
            if (jump(oX, oY, dX, 0, matrix, goal) != None
                or jump(oX, oY, 0, dY, matrix, goal) != None):
                return (oX, oY)

            # Bergerak diagonal
            oX += dX
            oY += dY

            # Memeriksa apakah posisi baru valid
            if blocked(oX, oY, 0, 0, matrix):
                return None
            if dblock(oX, oY, dX, dY, matrix):
                return None
            if (oX, oY) == goal:
                return (oX, oY)
    else:
        # Menangani pergerakan lurus
        if dX != 0:  # Horizontal
            while True:
                # Memeriksa tetangga paksa
                if (not blocked(oX, nY, dX, 1, matrix) and blocked(oX, nY, 0, 1, matrix)
                    or not blocked(oX, nY, dX, -1, matrix) and blocked(oX, nY, 0, -1, matrix)):
                    return (oX, nY)

                oX += dX

                if blocked(oX, nY, 0, 0, matrix):
                    return None
                if (oX, nY) == goal:
                    return (oX, nY)
        else:  # Vertikal
            while True:
                # Memeriksa tetangga paksa
                if (not blocked(nX, oY, 1, dY, matrix) and blocked(nX, oY, 1, 0, matrix)
                    or not blocked(nX, oY, -1, dY, matrix) and blocked(nX, oY, -1, 0, matrix)):
                    return (nX, oY)

                oY += dY

                if blocked(nX, oY, 0, 0, matrix):
                    return None
                if (nX, oY) == goal:
                    return (nX, oY)

    return jump(nX, nY, dX, dY, matrix, goal)


Grid = np.array(
    [[0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0]]
)

# Define start and goal positions
start = (0, 0)
goal = (2, 4)

# Call the JPS method
# print('A-star Konversional', '='*500)
# print(Astar_Komentar.method(Grid, start, goal, 2))
# print('JPS', '='*500)
# print(JPS_Komentar.method(Grid, start, goal, 2))

directions = [(1,0), (1, 1), (0, 1)]

for direction in directions:
    dx = direction[0]
    dy = direction[1]
    print(f"Arah ({dx}, {dy})")
    print(jump(start[0], start[1], dx, dy, Grid, goal))


 