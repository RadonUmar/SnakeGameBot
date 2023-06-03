import pygame
import random

# Initialize pygame
pygame.init()

# Set up game window
screen_width, screen_height = 600, 600
square_size = 25
num_squares = 24
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Define colors
green = (0, 128, 0)
dark_green = (0, 100, 0)
red = (255, 0, 0)
snake_color = (255, 165, 0)  # Orange

# Set up snake variables
snake_size = square_size - 2  # Adjust size to leave gap between squares
snake_speed = 1
snake_x = random.randint(2, num_squares - 3) * square_size
snake_y = random.randint(2, num_squares - 3) * square_size
snake_dx = snake_speed
snake_dy = 0
snake_body = [[snake_x, snake_y]]

# Set up food variables
food_x = random.randint(1, num_squares - 2) * square_size
food_y = random.randint(1, num_squares - 2) * square_size

# Set up game variables
score = 0
game_over = False
start_screen = True

# Set up game loop
clock = pygame.time.Clock()

# Function to display start screen
def show_start_screen():
    screen.fill(green)
    start_text = pygame.font.SysFont(None, 48).render("Click to Start", True, dark_green)
    screen.blit(
        start_text,
        (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - start_text.get_height() // 2),
    )
    pygame.display.update()

# Function to display game over screen
def show_game_over_screen():
    screen.fill(green)
    game_over_text = pygame.font.SysFont(None, 48).render(
        f"Game Over! Score: {score}", True, dark_green
    )
    screen.blit(
        game_over_text,
        (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50),
    )
    restart_text = pygame.font.SysFont(None, 32).render(
        "Click to Restart", True, dark_green
    )
    screen.blit(
        restart_text,
        (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50),
    )
    pygame.display.update()

# Function to reset the game
def reset_game():
    global snake_x, snake_y, snake_dx, snake_dy, snake_body, food_x, food_y, score, game_over
    snake_x = random.randint(2, num_squares - 3) * square_size
    snake_y = random.randint(2, num_squares - 3) * square_size
    snake_dx = snake_speed
    snake_dy = 0
    snake_body = [[snake_x, snake_y]]
    food_x = random.randint(1, num_squares - 2) * square_size
    food_y = random.randint(1, num_squares - 2) * square_size
    score = 0
    game_over = False

# Game loop
while not game_over:
    if start_screen:
        show_start_screen()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN and start_screen:
            start_screen = False
        elif event.type == pygame.KEYDOWN and not start_screen:
            if event.key == pygame.K_UP and snake_dy != 1:
                snake_dx = 0
                snake_dy = -1
            elif event.key == pygame.K_DOWN and snake_dy != -1:
                snake_dx = 0
                snake_dy = 1
            elif event.key == pygame.K_LEFT and snake_dx != 1:
                snake_dx = -1
                snake_dy = 0
            elif event.key == pygame.K_RIGHT and snake_dx != -1:
                snake_dx = 1
                snake_dy = 0
            elif event.key == pygame.K_RETURN and game_over:
                reset_game()

    if not start_screen:
        # Update snake position
        snake_x += snake_dx * square_size
        snake_y += snake_dy * square_size

        # Check if snake hits the walls
        if (
            snake_x < square_size
            or snake_x >= screen_width - square_size
            or snake_y < square_size
            or snake_y >= screen_height - square_size
        ):
            game_over = True

        # Check if snake hits its own body
        for body_part in snake_body[1:]:
            if body_part[0] == snake_x and body_part[1] == snake_y:
                game_over = True

        # Check if snake eats the food
        if snake_x == food_x and snake_y == food_y:
            score += 1
            food_x = random.randint(1, num_squares - 2) * square_size
            food_y = random.randint(1, num_squares - 2) * square_size
            snake_body.append([snake_x, snake_y])

        # Update snake body
        snake_body.insert(0, [snake_x, snake_y])
        if len(snake_body) > score + 1:
            snake_body.pop()

        # Clear the screen
        screen.fill(green)

        # Draw the checkerboard pattern
        for row in range(num_squares):
            for col in range(num_squares):
                square_color = green if (row + col) % 2 == 0 else dark_green
                square_rect = pygame.Rect(
                    col * square_size, row * square_size, square_size, square_size
                )
                pygame.draw.rect(screen, square_color, square_rect)

        # Draw the snake
        for body_part in snake_body:
            pygame.draw.rect(
                screen, snake_color, (body_part[0], body_part[1], snake_size, snake_size)
            )

        # Draw the food
        pygame.draw.rect(screen, red, (food_x, food_y, snake_size, snake_size))

        # Update display
        pygame.display.update()

        # Control game speed
        clock.tick(10)

    # Show game over screen
    if game_over:
        show_game_over_screen()

# Quit the game
pygame.quit()
