from Algoritma import jps
from Algoritma import astar
from MethodOptimasi.PathPolylineOptimization import prunning
import numpy as np
import ast
import z_visualize as visual
import random

def read_matrix():
    with open("Output/grid_output.txt", "r") as file:
        content = file.read()
        grid_list = ast.literal_eval(content)
        matrix = np.array(grid_list)
        return matrix

def save_matrix(matrix):
    matrix[(matrix == 6) | (matrix == 5) | (matrix == 8)] = 0
    with open("Output/grid_output.txt", "w") as file:
        file.write("[\n")
        for row in matrix:  # loop per baris
            # Ubah setiap elemen ke int biasa (bukan np.int32 misalnya)
            row_list = [int(item) for item in row]
            file.write(f"    {row_list},\n")
        file.write("]\n")
        print("Berhasil disimpan")

def generate_matrix(rows, cols, num_obstacles=0):
    matrix = np.zeros((rows, cols), dtype=int)
    total_cells = rows * cols
    num_obstacles = min(cols*2 if num_obstacles == 0 else num_obstacles, total_cells)
    obstacle_indices = random.sample(range(total_cells), num_obstacles)

    for index in obstacle_indices:
        i = index // cols  # baris
        j = index % cols   # kolom
        matrix[i][j] = 1

    save_matrix(matrix)

    return matrix

# matrix = generate_matrix(2**4, 2**4)
matrix = read_matrix()

start = None
goal = None

height, width = matrix.shape[:]

matrix[1][1] = 2
matrix[height-3][width-3] = 3

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if (matrix[i][j] == 2):
            start = (i, j)
        elif (matrix[i][j] == 3):
            goal = (i, j)


pathASTAR, close, open = astar.method(matrix, start, goal, 2)
pathJPS, close, open, gn, fn = jps.method(matrix, start, goal, 2)
path = prunning(pathJPS[0], matrix)

for x, y in close:
    matrix[x][y] = 6

for _, (x, y) in open:
    matrix[x][y] = 5

print(f"Panjang openlist : {len(open)}")
print(f"Panjang closelist : {len(close)}")

visual.main(matrix, pathJPS[0], path, False, start, goal, gn, fn)

