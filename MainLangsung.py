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

Grid = np.array(
    [[0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]]
)

# Define start and goal positions
start = (0, 0)
goal = (2, 4)

# Call the JPS method
print('A-star Konversional', '='*500)
print(Astar_Komentar.method(Grid, start, goal, 2))
print('JPS', '='*500)
print(JPS_Komentar.method(Grid, start, goal, 2))

