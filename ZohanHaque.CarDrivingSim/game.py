import pygame
import random
import time

# Initialize pygame
pygame.init()

# Load splash screen image
splash_image = pygame.image.load("assets/splash.png")

# Get screen size for maximizing
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Create a temporary window for splash screen
splash_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Loading...")

# Show splash screen
splash_screen.blit(pygame.transform.scale(splash_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
pygame.display.update()
time.sleep(3)  # Display splash screen for 3 seconds

# Now load the main game
pygame.display.set_caption("Car Driving Simulator")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

# Load game assets
car_image = pygame.image.load("assets/car.png")
car_image = pygame.transform.scale(car_image, (50, 80))

background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (1600, 1200))

# Load and play car driving noise
pygame.mixer.init()
pygame.mixer.music.load("sound/ambience.mp3")
pygame.mixer.music.play(-1)  # Loop the sound indefinitely

# Game Constants
CAR_SPEED = 5
OBSTACLE_COUNT = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define classes
class Car:
    def __init__(self, x, y):
        self.image = car_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = CAR_SPEED
        self.crashed = False

    def move(self, keys):
        if not self.crashed:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, RED, (self.rect.x - camera_x, self.rect.y - camera_y, 50, 50))

# Initialize player and obstacles
player = Car(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
obstacles = [Obstacle(random.randint(100, 1500), random.randint(100, 1100)) for _ in range(OBSTACLE_COUNT)]

# Camera position
camera_x, camera_y = 0, 0

# Game Loop
running = True
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to exit
                running = False
        elif event.type == pygame.VIDEORESIZE:  # Handle resizing
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    # Move player
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Camera follows player
    camera_x = max(0, min(player.rect.x - SCREEN_WIDTH // 2, background.get_width() - SCREEN_WIDTH))
    camera_y = max(0, min(player.rect.y - SCREEN_HEIGHT // 2, background.get_height() - SCREEN_HEIGHT))

    # Check for collisions
    for obs in obstacles:
        if player.rect.colliderect(obs.rect):
            player.crashed = True

    # Draw background
    screen.blit(background, (-camera_x, -camera_y))

    # Draw everything
    player.draw(screen, camera_x, camera_y)
    for obs in obstacles:
        obs.draw(screen, camera_x, camera_y)

    # Show game over if crashed
    if player.crashed:
        font = pygame.font.Font(None, 50)
        text = font.render("CRASHED! GAME OVER", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False  # Stop the game loop permanently

    pygame.display.update()

# Stop car sound when game closes
pygame.mixer.music.stop()

pygame.quit()


