#!/usr/bin/env python3
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (169, 169, 169)
yellow = (255, 255, 0)
green = (0, 255, 0)
brown = (139, 69, 19)

# Car settings
car_width = 50
car_height = 80
car_x = screen_width // 2
car_y = screen_height - car_height - 10
car_speed = 5

# Obstacle settings
obstacle_width = 50
obstacle_height = 80
obstacle_speed = 5
obstacles = [
    {"x": random.randint(0, screen_width - obstacle_width), "y": -obstacle_height},
    {"x": random.randint(0, screen_width - obstacle_width), "y": -obstacle_height - 300}
]

# Road line settings
line_height = 20
line_width = 10
line_gap = 20
line_speed = 5
lines = [{"x": screen_width // 2 - line_width // 2, "y": i} for i in range(0, screen_height, line_height + line_gap)]

# Font settings
font = pygame.font.SysFont(None, 36)

# Lives settings
lives = 3

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < screen_width - car_width:
        car_x += car_speed

    screen.fill(gray)

    # Draw continuous line on the left side
    pygame.draw.line(screen, yellow, (50, 0), (50, screen_height), 5)

    # Draw continuous line on the right side
    pygame.draw.line(screen, yellow, (750, 0), (750, screen_height), 5)

    # Move and draw road lines
    for line in lines:
        line["y"] += line_speed
        if line["y"] > screen_height:
            line["y"] = -line_height
        pygame.draw.rect(screen, yellow, (line["x"], line["y"], line_width, line_height))

    # Draw car
    pygame.draw.rect(screen, black, (car_x, car_y, car_width, car_height))

    # Move and draw obstacles
    for obstacle in obstacles:
        obstacle["y"] += obstacle_speed
        if obstacle["y"] > screen_height:
            obstacle["y"] = -obstacle_height
            obstacle["x"] = random.randint(0, screen_width - obstacle_width)
        pygame.draw.rect(screen, red, (obstacle["x"], obstacle["y"], obstacle_width, obstacle_height))

        # Check for collision
        if car_y < obstacle["y"] + obstacle_height:
            if (car_x > obstacle["x"] and car_x < obstacle["x"] + obstacle_width) or (car_x + car_width > obstacle["x"] and car_x + car_width < obstacle["x"] + obstacle_width):
                lives -= 1
                if lives > 0:
                    draw_text("You have an accident!", font, red, screen, screen_width // 2 - 100, screen_height // 2)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    car_x = screen_width // 2
                    car_y = screen_height - car_height - 10
                else:
                    draw_text("You lose!", font, red, screen, screen_width // 2 - 50, screen_height // 2)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    running = False

    # Display lives
    draw_text(f"Lives: {lives}", font, white, screen, screen_width - 120, 10)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
