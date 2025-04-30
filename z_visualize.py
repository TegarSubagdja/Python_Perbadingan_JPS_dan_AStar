import pygame
import sys
import numpy as np

CELL_SIZE = 30

# Warna RGB
colors = {
    0: (255, 255, 255),  # Ruang kosong
    1: (23, 37, 42),     # Rintangan
    2: (58, 175, 169),   # Start
    3: (255, 0, 33),     # Goal
    4: (63, 97, 132),    # Garis
    5: (255, 255, 0),    # Open List
    6: (255, 165, 0),    # Close List
    7: (119, 136, 153),  # Abu-abu
    8: (232, 23, 93),    # Pink
}

def draw_grid(screen, matrix):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i][j]
            color = colors.get(value, (0, 0, 0))  # Default ke hitam jika tidak dikenal
            pygame.draw.rect(
                screen,
                color,
                (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            # Garis grid
            pygame.draw.rect(
                screen,
                (200, 200, 200),
                (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )

def main(matrix):
    pygame.init()

    GRID_HEIGHT, GRID_WIDTH = matrix.shape
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Matrix Visualization")

    draw_grid(screen, matrix)
    pygame.display.flip()

    # Window loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
