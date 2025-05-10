# Import necessary libraries
import pygame
import random
import os

# Initialize pygame and mixer for sounds
pygame.init()
pygame.mixer.init()

# Game settings
WIDTH, HEIGHT = 400, 600
gravity = 0.6
flap_strength = -10
pipe_gap = 250
pipe_width = 60
pipe_speed = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 128, 0)

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load background image
background_img = pygame.image.load(r"C:\Users\Excalibur\Downloads\Yeni klasör (3)\background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load floor (ground) image
floor_img = pygame.image.load(r"C:\Users\Excalibur\Downloads\Yeni klasör (3)\floor.png")
floor_img = pygame.transform.scale(floor_img, (WIDTH, 100))
floor_height = 100
floor_x = 0

# Load sound effects
try:
    flap_sound = pygame.mixer.Sound(r"C:\Users\Excalibur\Downloads\Yeni klasör (3)\flap.wav")
    fall_sound = pygame.mixer.Sound(r"C:\Users\Excalibur\Downloads\Yeni klasör (3)\fall.wav")
    flap_sound.set_volume(1.0)
    fall_sound.set_volume(1.0)
except Exception as e:
    print(f"Sound file error: {e}")
    flap_sound = None
    fall_sound = None

# Bird class definition
class Bird:
    def _init_(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        BIRD_IMAGE_PATH = r"C:\Users\Excalibur\Downloads\Yeni klasör (3)\bird.png"

        # Load and scale bird image
        if os.path.exists(BIRD_IMAGE_PATH):
            self.image = pygame.image.load(BIRD_IMAGE_PATH)
            self.image = pygame.transform.scale(self.image, (50, 35))
        else:
            raise FileNotFoundError(f"{BIRD_IMAGE_PATH} not found!")

        self.width = 50
        self.height = 35

    def update(self):
        # Update bird's position with gravity
        self.velocity += gravity
        self.y += self.velocity

    def flap(self):
        # Make the bird jump
        self.velocity = flap_strength
        if flap_sound:
            flap_sound.play()

    def draw(self):
        # Draw bird on the screen
        screen.blit(self.image, (self.x, int(self.y)))

# Pipe class definition
class Pipe:
    def _init_(self, x):
        self.x = x
        margin = 100  # Safe margin at top and bottom
        self.center = random.randint(margin + pipe_gap // 2, HEIGHT - margin - pipe_gap // 2)

    def update(self):
        # Move pipes to the left
        self.x -= pipe_speed

    def draw(self):
        # Draw top and bottom pipes
        top_height = self.center - pipe_gap // 2
        bottom_y = self.center + pipe_gap // 2
        bottom_height = HEIGHT - bottom_y

        pygame.draw.rect(screen, LIGHT_GREEN, (self.x, 0, pipe_width, top_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, bottom_y, pipe_width, bottom_height))

# Initialize game variables
bird = Bird()
pipes = [Pipe(WIDTH + i * 250) for i in range(3)]
score = 0
high_score = 0
running = True

# Game loop
while running:
    # Draw background
    screen.blit(background_img, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.flap()

    # Update bird
    bird.update()
    bird.draw()

    # Update and draw pipes
    for pipe in pipes:
        pipe.update()
        pipe.draw()
        if pipe.x + pipe_width < 0:
            pipes.remove(pipe)
            pipes.append(Pipe(WIDTH))
            score += 1

        # Check collision
        if (bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe_width):
            top_height = pipe.center - pipe_gap // 2
            bottom_y = pipe.center + pipe_gap // 2
            if bird.y < top_height or bird.y + bird.height > bottom_y:
                if fall_sound:
                    fall_sound.play()
                running = False

    # Check if bird hits ground or flies off-screen
    if bird.y + bird.height > HEIGHT or bird.y < 0:
        if fall_sound:
            fall_sound.play()
        running = False

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 30))

    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 60))

    # Update floor (moving ground)
    floor_x -= 1
    if floor_x <= -WIDTH:
        floor_x = 0

    screen.blit(floor_img, (floor_x, HEIGHT - floor_height))
    screen.blit(floor_img, (floor_x + WIDTH, HEIGHT - floor_height))

    # Game over handling
    if not running:
        if score > high_score:
            high_score = score

        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, BLACK)
        quit_text = font.render("Press Q to Quit", True, BLACK)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT * 2 // 3))

        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        waiting_for_input = False
                    elif event.key == pygame.K_r:
                        # Restart game
                        bird = Bird()
                        pipes = [Pipe(WIDTH + i * 250) for i in range(3)]
                        score = 0
                        running = True
                        waiting_for_input = False

            pygame.display.flip()
            clock.tick(30)

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Quit pygame
pygame.quit()








