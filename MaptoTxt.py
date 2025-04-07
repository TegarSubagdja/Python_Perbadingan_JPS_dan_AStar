grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

with open("grid_output.txt", "w") as file:
    file.write("[\n")
    for row in grid:
        file.write(f"    {row},\n")
    file.write("]\n")
