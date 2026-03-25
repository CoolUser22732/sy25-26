import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Player properties
player_pos = [WIDTH // 2, HEIGHT - 50]
player_size = 50

# Enemy properties
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_speed = 10

score = 0
game_over = False

def draw_handdrawn_rect(surface, color, rect):
    """Draws a rectangle with a hand-drawn effect."""
    x, y, w, h = rect
    pygame.draw.polygon(surface, color, [
        (x + random.randint(-3, 3), y + random.randint(-3, 3)),
        (x + w + random.randint(-3, 3), y + random.randint(-3, 3)),
        (x + w + random.randint(-3, 3), y + h + random.randint(-3, 3)),
        (x + random.randint(-3, 3), y + h + random.randint(-3, 3))
    ], 0)
    # Add an outline for a sketchy effect
    pygame.draw.lines(surface, BLACK, True, [
        (x + random.randint(-3, 3), y + random.randint(-3, 3)),
        (x + w + random.randint(-3, 3), y + random.randint(-3, 3)),
        (x + w + random.randint(-3, 3), y + h + random.randint(-3, 3)),
        (x + random.randint(-3, 3), y + h + random.randint(-3, 3))
    ], 2)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Movement Logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5  # Move left
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5  # Move right

    # Keep player within screen bounds
    player_pos[0] = max(0, min(WIDTH - player_size, player_pos[0]))

    # Update enemy position
    enemy_pos[1] += enemy_speed

    if enemy_pos[1] > HEIGHT:
        enemy_pos[1] = 0
        enemy_pos[0] = random.randint(0, WIDTH - enemy_size)
        score += 1
        print(f"Score: {score}")

    # Collision Detection
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)
    if player_rect.colliderect(enemy_rect):
        print("Game Over!")
        game_over = True

    # Drawing
    screen.fill(WHITE)  # White background for a paper-like look
    
    # Draw the enemy and player with a hand-drawn effect
    draw_handdrawn_rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    draw_handdrawn_rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    pygame.display.update()
    clock.tick(30)

pygame.quit()