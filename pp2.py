import pygame
import random
import time
import math

# Initialize pygame
pygame.init()

# Get screen width and height
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Mania")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Pac-Man attributes
pacman_radius = int(min(screen_width, screen_height) * 0.02)
pacman_x = screen_width // 2
pacman_y = screen_height // 2
pacman_speed = 1
pacman_score = 0
pacman_lives = 5

# High score
high_score = 0

# Ghost attributes
ghost_radius = int(min(screen_width, screen_height) * 0.015)
ghost_speed = 0.1
ghosts = []

# Game Fonts
font = pygame.font.SysFont(None, int(min(screen_width, screen_height) * 0.02))

# Time tracking variables
start_time = time.time()
last_ghost_time = start_time
last_scoreboard_time = start_time
last_speed_increase_time = start_time

def render_stuff():
    pygame.draw.circle(screen, YELLOW, (int(pacman_x), int(pacman_y)), pacman_radius)
    for ghost in ghosts:
        pygame.draw.circle(screen, RED, (int(ghost[0]), int(ghost[1])), ghost_radius)

    # Draw score, lives, and high score
    score_text = font.render("Score: " + str(pacman_score), True, WHITE)
    screen.blit(score_text, (int(screen_width * 0.01), int(screen_height * 0.01)))

    lives_text = font.render("Lives: " + str(pacman_lives), True, WHITE)
    screen.blit(lives_text, (int(screen_width * 0.01), int(screen_height * 0.05)))

    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(high_score_text, (int(screen_width * 0.01), int(screen_height * 0.09)))

    pygame.display.update()

def circle_collision(circle1, circle2):
    distance_squared = (circle1[0] - circle2[0]) ** 2 + (circle1[1] - circle2[1]) ** 2
    return distance_squared <= (circle1[2] + circle2[2]) ** 2

def show_game_over():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))
    pygame.display.update()
    time.sleep(2)

# Function to move ghost towards pacman
def move_ghost_towards_pacman(ghost_x, ghost_y, pacman_x, pacman_y):
    distance = math.sqrt((ghost_x - pacman_x) ** 2 + (ghost_y - pacman_y) ** 2)
    if distance != 0:
        move_x = ((pacman_x - ghost_x) / distance)
        move_y = ((pacman_y - ghost_y) / distance)
        ghost_x += move_x * ghost_speed
        ghost_y += move_y * ghost_speed
    return ghost_x, ghost_y

# Main game loop
playing = True
while playing:
    screen.fill(BLACK)
    game_over = False

    # Reset game variables
    pacman_x = screen_width // 2
    pacman_y = screen_height // 2
    pacman_speed = 1
    pacman_score = 0
    pacman_lives = 5
    ghosts = []
    ghost_speed = 0.1

    # Main game loop
    while not game_over:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                playing = False

        # Move Pac-Man to follow the cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pacman_dx = mouse_x - pacman_x
        pacman_dy = mouse_y - pacman_y
        distance = math.sqrt(pacman_dx ** 2 + pacman_dy ** 2)
        if distance > 0:
            move_x = pacman_dx / distance
            move_y = pacman_dy / distance
            pacman_x += move_x * pacman_speed
            pacman_y += move_y * pacman_speed

        # Increase Pac-Man's speed every 150 seconds
        elapsed_time = time.time() - last_speed_increase_time
        if elapsed_time >= 75:
            last_speed_increase_time = time.time()
            pacman_speed += .5

        # Move Ghosts
        for i in range(len(ghosts)):
            ghost_x, ghost_y = ghosts[i][0], ghosts[i][1]
            ghost_x, ghost_y = move_ghost_towards_pacman(ghost_x, ghost_y, pacman_x, pacman_y)
            ghosts[i] = [ghost_x, ghost_y]

        # Collision detection with ghosts
        for i in range(len(ghosts)):
            for j in range(i+1, len(ghosts)):
                if circle_collision(ghosts[i] + [ghost_radius], ghosts[j] + [ghost_radius]):
                    # Swap velocities to simulate bouncing off
                    ghosts[i][0] = random.randint(0,screen_width)
                    ghosts[i][1] = random.randint(0,screen_height)

        # Move the ghosts within the screen boundaries
        for ghost in ghosts:
            ghost[0] = max(min(ghost[0], screen_width - ghost_radius), ghost_radius)
            ghost[1] = max(min(ghost[1], screen_height - ghost_radius), ghost_radius)

        # Collision detection with ghosts
        for ghost in ghosts:
            if circle_collision(ghost + [ghost_radius], [pacman_x, pacman_y, pacman_radius]):
                pacman_lives -= 1
                if pacman_lives == 0:
                    print("Game Over!")
                    if pacman_score > high_score:
                        high_score = pacman_score
                    game_over = True
                    show_game_over()
                else:
                    print("Pac-Man lost a life!")
                    pacman_x = random.randint(0, screen_width)
                    pacman_y = random.randint(0, screen_height)
                    render_stuff()
                    time.sleep(1)

        # Add a new ghost every 30 seconds
        elapsed_time = time.time() - last_ghost_time
        if elapsed_time >= 15:
            last_ghost_time = time.time()
            ghosts.append([random.randint(0, screen_width), random.randint(0, screen_height), random.uniform(-1, 1), random.uniform(-1, 1)])
            ghost_speed += 0.1
            render_stuff()
            time.sleep(1)

        # Move the scoreboard up every 30 seconds
        elapsed_time = time.time() - last_scoreboard_time
        if elapsed_time >= 15:
            last_scoreboard_time = time.time()
            pacman_score += 1

        # Render Pac-Man and Ghosts
        render_stuff()

# Quit pygame
pygame.quit()

