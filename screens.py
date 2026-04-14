import pygame
from settings import WHITE, RED, WIDTH, HEIGHT


def draw_text(surface, text, size, x, y, color=WHITE, centered=False):
    font = pygame.font.SysFont("segoeui", size, bold=True)
    rendered = font.render(text, True, color)
    if centered:
        rect = rendered.get_rect(center=(x, y))
    else:
        rect = rendered.get_rect(topleft=(x, y))
    surface.blit(rendered, rect)


def draw_game_over(surface, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
    draw_text(surface, "GAME OVER", 54, WIDTH // 2, HEIGHT // 2 - 40, RED, centered=True)
    draw_text(surface, f"Score: {score}", 34, WIDTH // 2, HEIGHT // 2 + 20, WHITE, centered=True)
    draw_text(surface, "Press any key to play again", 20, WIDTH // 2, HEIGHT // 2 + 70, (180, 180, 180), centered=True)
