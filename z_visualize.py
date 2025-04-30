import pygame
import sys
import numpy as np

CELL_SIZE = 40  # Ukuran setiap sel grid

# Warna RGB
colors = {
    0: (255, 255, 255),  # Kosong
    1: (23, 37, 42),     # Rintangan
    2: (58, 175, 169),   # Start
    3: (255, 0, 33),     # Goal
    4: (63, 97, 132),    # Garis
    5: (255, 255, 0),    # Open List
    6: (255, 165, 0),    # Close List
    7: (119, 136, 153),  # Abu-abu
    8: (232, 23, 93),    # Pink (jalur yang akan dihubungkan)
}

def draw_grid(screen, matrix, show_coords=False):
    font = pygame.font.SysFont(None, 16) if show_coords else None
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i][j]
            color = colors.get(value, (0, 0, 0))
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            if show_coords:
                coord_text = font.render(f'({i},{j})', True, (0, 0, 0))
                text_rect = coord_text.get_rect(center=rect.center)
                screen.blit(coord_text, text_rect)


def draw_lines_between_points(screen, path, color):

    if color == 1:
        color = (255, 0, 0)
    else:
        color = (0, 255, 0)

    if len(path) >= 2:
        # Konversi path menjadi koordinat piksel tengah
        pixel_path = [(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2) for i, j in path]
        for idx in range(len(pixel_path) - 1):
            pygame.draw.line(screen, color, pixel_path[idx], pixel_path[idx + 1], 2)
        # Tambahkan lingkaran hitam kecil di setiap titik
        for px, py in pixel_path:
            pygame.draw.circle(screen, (0, 0, 0), (px, py), 4)

def main(matrix, path1, path2=None, show_coords=False):
    pygame.init()
    GRID_HEIGHT, GRID_WIDTH = matrix.shape
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    pygame.display.set_caption("Matrix Visualization")

    draw_grid(screen, matrix, show_coords)
    draw_lines_between_points(screen, path1, 1)
    if path2:
        draw_lines_between_points(screen, path2, 2)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
