"""Happy Fly: Circle 7 times, land, then celebrate."""

import math
import pygame

# [1 SETUP] Create the window and reusable tools.
pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Fly V2")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

LIGHT_GRAY = (180, 180, 180)
BROWN = (130, 85, 45)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
GREEN = (20, 100, 40)

# [2 DATA] Position, speed and animation state.
center_x, center_y = WIDTH / 2, HEIGHT / 2

radius = 120
loops_required = 7
angular_speed = 3.0      # Radians per second.
landing_speed = 140.0   # Pixels per second.

target_x, target_y = center_x, center_y + 150

angle = 0.0
completed_circles = 0
fly_x, fly_y = center_x + radius, center_y

state = "flying"
running = True

while running:
    # [3 INPUT] Measure time and process window events.
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                angle = 0.0
                completed_circles = 0
                fly_x, fly_y = center_x + radius, center_y
                state = "flying"

    if not running:
        break

    # [4 UPDATE] Fly in circles, then move to the target.
    if state == "flying":
        angle = min(
            angle + angular_speed * dt,
            loops_required * math.tau
        )

        completed_circles = min(
            int(angle / math.tau),
            loops_required
        )

        fly_x = center_x + radius * math.cos(angle)
        fly_y = center_y + radius * math.sin(angle)

        if angle >= loops_required * math.tau:
            state = "landing"

    elif state == "landing":
        dx = target_x - fly_x
        dy = target_y - fly_y

        distance = math.hypot(dx, dy)
        step = landing_speed * dt

        if distance <= step:
            fly_x, fly_y = target_x, target_y
            state = "happy"
        else:
            fly_x += dx / distance * step
            fly_y += dy / distance * step

    # [5 DRAW] Paint a complete fresh frame.
    screen.fill(LIGHT_GRAY)

    pygame.draw.circle(
        screen, BROWN,
        (int(target_x), int(target_y)), 30
    )

    pygame.draw.rect(
        screen, BROWN,
        (int(target_x) - 40, int(target_y) + 10, 80, 15)
    )

    x, y = round(fly_x), round(fly_y)

    pygame.draw.circle(screen, WHITE, (x - 7, y - 8), 7)
    pygame.draw.circle(screen, WHITE, (x + 7, y - 8), 7)
    pygame.draw.circle(screen, BLACK, (x, y), 10)

    label = f"Circles: {completed_circles}/{loops_required}"
    screen.blit(font.render(label, True, BLACK), (25, 20))

    if state == "happy":
        message = font.render(
            "The Fly is Happy! BZZZ! YUMMY!",
            True, GREEN
        )

        screen.blit(
            message,
            message.get_rect(center=(WIDTH // 2, 80))
        )

    hint = font.render("R: restart    Esc: quit", True, BLACK)
    screen.blit(hint, (25, HEIGHT - 40))

    pygame.display.flip()

# [6 EXIT] Release the window when the loop finishes.
pygame.quit()