import pygame
import random
import sys

# --- Settings ---
CELL        = 20        # Size of each tile in pixels
COLUMNS     = 30        # Number of columns
ROWS        = 25        # Number of rows
WIDTH       = CELL * COLUMNS
HEIGHT      = CELL * ROWS
FPS         = 10        # Speed (tiles per second)

# Colors
BLACK       = (  0,   0,   0)
WHITE       = (255, 255, 255)
GREEN       = ( 50, 205,  50)
DARK_GREEN  = ( 34, 139,  34)
RED         = (220,  20,  60)
GRAY        = ( 40,  40,  40)
ORANGE      = (255, 165,   0)

# Directions
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)


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


def draw_text(surface, text, size, x, y, color=WHITE, centered=False):
    font = pygame.font.SysFont("segoeui", size, bold=True)
    rendered = font.render(text, True, color)
    if centered:
        rect = rendered.get_rect(center=(x, y))
    else:
        rect = rendered.get_rect(topleft=(x, y))
    surface.blit(rendered, rect)


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
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            draw_text(screen, "GAME OVER", 54, WIDTH // 2, HEIGHT // 2 - 40, RED, centered=True)
            draw_text(screen, f"Score: {score}", 34, WIDTH // 2, HEIGHT // 2 + 20, WHITE, centered=True)
            draw_text(screen, "Press any key to play again", 20, WIDTH // 2, HEIGHT // 2 + 70, (180, 180, 180), centered=True)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    game_loop()
