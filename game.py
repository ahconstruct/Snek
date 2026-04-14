import pygame
import random
import sys

from settings import (
    CELL, COLUMNS, ROWS, WIDTH, HEIGHT, FPS,
    BLACK, GREEN, DARK_GREEN, RED, GRAY, ORANGE,
    UP, DOWN, LEFT, RIGHT,
)
from screens import draw_text, draw_game_over


def draw_tile(surface, color, x, y, border=False):
    rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
    pygame.draw.rect(surface, color, rect)
    if border:
        pygame.draw.rect(surface, BLACK, rect, 1)


def random_food(snake):
    while True:
        pos = (random.randint(0, COLUMNS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    # Game state
    snake = [(COLUMNS // 2, ROWS // 2)]
    direction = RIGHT
    next_direction = RIGHT
    food = random_food(snake)
    score = 0
    alive = True  # False = game over

    while True:
        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not alive:
                    # Press any key to restart
                    return game_loop()
                if event.key in (pygame.K_UP, pygame.K_w) and direction != DOWN:
                    next_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != UP:
                    next_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != RIGHT:
                    next_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != LEFT:
                    next_direction = RIGHT

        if alive:
            direction = next_direction

            # Move head
            head_x, head_y = snake[0]
            new_x = head_x + direction[0]
            new_y = head_y + direction[1]
            new_head = (new_x, new_y)

            # Check wall collision
            if not (0 <= new_x < COLUMNS and 0 <= new_y < ROWS):
                alive = False
            # Check self collision
            elif new_head in snake:
                alive = False
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                else:
                    snake.pop()

        # --- Drawing ---
        screen.fill(GRAY)

        # Draw grid (subtle)
        for col in range(COLUMNS):
            for row in range(ROWS):
                rect = pygame.Rect(col * CELL, row * CELL, CELL, CELL)
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)

        # Draw food
        draw_tile(screen, RED, food[0], food[1])

        # Draw snake
        for i, (x, y) in enumerate(snake):
            color = GREEN if i > 0 else DARK_GREEN
            draw_tile(screen, color, x, y, border=True)

        # Draw score
        draw_text(screen, f"Score: {score}", 22, 8, 6, ORANGE)

        # Game over overlay
        if not alive:
            draw_game_over(screen, score)

        pygame.display.flip()
        clock.tick(FPS)
