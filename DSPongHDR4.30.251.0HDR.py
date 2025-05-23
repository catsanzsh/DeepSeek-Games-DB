import pygame
import random
import numpy as np

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init(frequency=44100)

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Sound synthesis functions
def create_sound(frequency=440, duration=0.1, waveform='square'):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    if waveform == 'square':
        wave = 0.5 * np.sign(np.sin(2 * np.pi * frequency * t))
    elif waveform == 'sawtooth':
        wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
    else:  # sine
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    wave = np.int16(wave * 32767)
    return pygame.mixer.Sound(buffer=wave)

# Game sounds
paddle_hit_sound = create_sound(880, 0.05, 'square')
wall_hit_sound = create_sound(440, 0.05, 'square')
score_sound = create_sound(660, 0.2, 'square')

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle positions
left_paddle = pygame.Rect(20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball properties
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

# Scores
left_score = 0
right_score = 0

# Font for scoring
font = pygame.font.Font(None, 74)

clock = pygame.time.Clock()

def reset_ball():
    """Reset ball to center with random direction"""
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))
    score_sound.play()

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= 7
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += 7
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= 7
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += 7

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        wall_hit_sound.play()

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        paddle_hit_sound.play()
        # Add slight speed increase on hit
        ball_speed_x *= 1.05
        ball_speed_y *= 1.05

    # Scoring
    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball()

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Draw scores
    left_text = font.render(str(left_score), True, WHITE)
    screen.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(right_text, (3*WIDTH//4 - right_text.get_width()//2, 20))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
