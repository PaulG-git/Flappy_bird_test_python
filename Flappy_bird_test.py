import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 1000
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_GAP = 200
PIPE_WIDTH = 100
PIPE_SPEED = 3
BIRD_X = 80
GROUND_HEIGHT = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load assets
bird_img = pygame.image.load("art/bird.png")
pipe_img = pygame.image.load("art/pipe.png")
bg_img = pygame.image.load("art/background.png")

# Load sounds
flap_sound = pygame.mixer.Sound("sounds/flap.wav")
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
score_sound = pygame.mixer.Sound("sounds/score.wav")

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird test")
font = pygame.font.Font(None, 24)

class Bird:
    def __init__(self):
        self.y = HEIGHT // 2
        self.vel = 0
        self.angle = 0  # Bird rotation

    def jump(self):
        self.vel = JUMP_STRENGTH
        flap_sound.play()

    def move(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.angle = max(-30, min(30, -self.vel * 3))  # Tilt up/down

    def draw(self):
        rotated_bird = pygame.transform.rotate(bird_img, self.angle)
        screen.blit(rotated_bird, (BIRD_X, self.y))

    def get_rect(self):
        return pygame.Rect(BIRD_X, self.y, bird_img.get_width(), bird_img.get_height())

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - 200)
        self.passed = False  # For scoring

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        screen.blit(pipe_img, (self.x, self.height + PIPE_GAP))  # Bottom pipe
        screen.blit(pygame.transform.flip(pipe_img, False, True), (self.x, self.height - pipe_img.get_height()))  # Top pipe

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)

    def get_bottom_rect(self):
        return pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)

def check_collision(bird, pipes):
    bird_rect = bird.get_rect()
    if bird.y >= HEIGHT - GROUND_HEIGHT:  # Ground collision
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe.get_top_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):
            return True
    return False

def show_game_over(score):
    text = font.render(f"Game Over! Score: {score} | Y = Restart | N = Quit", True, RED)
    screen.blit(text, (WIDTH // 10, HEIGHT // 2))
    pygame.display.update()

def game():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(WIDTH + i * 400) for i in range(3)]
    running = True
    game_over = False
    score = 0

    while running:
        screen.fill(WHITE)
        screen.blit(bg_img, (0, 0))  # Background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    game()  # Restart
                elif event.key == pygame.K_n:
                    running = False

        if not game_over:
            bird.move()
            bird.draw()

            for pipe in pipes:
                pipe.move()
                pipe.draw()

                if pipe.x + PIPE_WIDTH < BIRD_X and not pipe.passed:
                    pipe.passed = True
                    score += 1
                    score_sound.play()

            pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]
            if pipes[-1].x < WIDTH - 400:
                pipes.append(Pipe(WIDTH))

            if check_collision(bird, pipes):
                hit_sound.play()
                game_over = True

            # Display score
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
        else:
            show_game_over(score)

        pygame.display.update()
        clock.tick(30)

game()
pygame.quit()
