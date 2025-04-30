from Algoritma import jps
import numpy as np
import ast
import z_visualize as visual

with open("Output/grid_output.txt", "r") as file:
    content = file.read()
    grid_list = ast.literal_eval(content)
    matrix = np.array(grid_list)

start = None
goal = None

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[0]):
        if (matrix[i][j] == 2):
            start = (i, j)
        elif (matrix[i][j] == 3):
            goal = (i, j)


path, close, open = jps.method(matrix, start, goal, 2)

for x, y in close:
    matrix[x][y] = 5

for _, (x, y) in open:
    matrix[x][y] = 6
        
matrix[start[0]][start[1]] = 2
matrix[goal[0]][goal[1]] = 3

print(f"Panjang openlist : {len(open)}")
print(f"Panjang closelist : {len(close)}")

visual.main(matrix)

