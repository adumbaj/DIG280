import pygame 
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Light Catcher")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_RED = (139, 0, 0)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Player setup
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - player_size * 2]
player_speed = 5

# Object setup
OBJECT_SIZE = 30
light_objects = []
heavy_objects = []
object_speed = 5

# Score and lives
score = 0
lives = 3

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Load sound effects
collect_sound = pygame.mixer.Sound("Collect.mp3")  # Play when collecting light objects
hit_sound = pygame.mixer.Sound("Hit.mp3")  # Play when hit by heavy objects
game_over_sound = pygame.mixer.Sound("Defeat.mp3")  # Sound played on game over

# Adjust volume of the sounds
collect_sound.set_volume(0.7)  # Set volume to 70% for collecting sound
hit_sound.set_volume(0.7)  # Set volume to 70% for hit sound
game_over_sound.set_volume(0.3)  # Set volume to 30% for game over sound

# Function to create light/heavy objects
def create_object(obj_list, color):
    while True:
        x_pos = random.randint(0, WIDTH - OBJECT_SIZE)
        y_pos = random.randint(-HEIGHT, 0)
        rect = pygame.Rect(x_pos, y_pos, OBJECT_SIZE, OBJECT_SIZE)

        # Check for collisions with existing objects
        overlap = False
        for existing_rect, _ in obj_list:
            if rect.colliderect(existing_rect):
                overlap = True
                break
        
        if not overlap:
            obj_list.append((rect, color))
            break  # Exit the loop once a valid position is found

# Update object positions
def update_objects(objects):
    for obj in objects[:]:
        obj[0].y += object_speed  # Move downwards
        if obj[0].top > HEIGHT:
            objects.remove(obj)

# Check for collisions using precise Rect hitboxes
def check_collisions(objects, is_light):
    global score, player_speed, lives
    player_rect = pygame.Rect(*player_pos, player_size, player_size)

    for obj in objects[:]:
        if player_rect.colliderect(obj[0]):
            objects.remove(obj)
            if is_light:
                score += 1
                player_speed = min(8, player_speed + 1)  # Cap speed at 8
                collect_sound.play()  # Play sound for collecting light objects
                increase_difficulty()  # Check if difficulty should increase
            else:
                lives -= 1
                player_speed = max(2, player_speed - 1)  # Floor speed at 2
                hit_sound.play()  # Play sound for hitting heavy objects

# Increase difficulty every 20 collected light objects
def increase_difficulty():
    global object_speed
    if score % 20 == 0:
        object_speed += 1  # Increase object speed

# Game Over screen with option to play again or quit
def game_over():
    global score, lives, object_speed, light_objects, heavy_objects, player_pos, player_speed
    
    # Play the game over sound
    game_over_sound.play()

    screen.fill(BLACK)
    
    # Display game over message and options
    game_over_text = font.render("Game Over!", True, WHITE)
    play_again_text = small_font.render("Press R to Play Again or Q to Quit", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2 + 20))
    
    pygame.display.flip()
    
    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    reset_game()  # Reset game state
                    return  # Exit the function to start the game loop again
                if event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    sys.exit()

# Reset the game state
def reset_game():
    global score, lives, object_speed, light_objects, heavy_objects, player_pos, player_speed
    score = 0
    lives = 3
    object_speed = 5
    light_objects.clear()
    heavy_objects.clear()
    player_pos[0] = WIDTH // 2
    player_pos[1] = HEIGHT - player_size * 2
    player_speed = 5  # Reset player speed
    pygame.mixer.stop()  # Stop all sounds when restarting

# Menu screen
def show_menu():
    while True:
        screen.fill(BLACK)

        # Draw title and instructions
        title = font.render("Light Catcher", True, WHITE)
        instructions = small_font.render(
            "Collect blue squares to score points. Avoid the red squares!", True, WHITE
        )
        movement_info = small_font.render(
            "Use arrow keys to move left and right.", True, WHITE
        )
        pause_info = small_font.render(
            "Press P to pause.", True, WHITE
        )
        continue_text = small_font.render("Click any button to continue.", True, WHITE)

        # Draw title, instructions, and continue text
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(movement_info, (WIDTH // 2 - movement_info.get_width() // 2, HEIGHT // 2))
        screen.blit(pause_info, (WIDTH // 2 - pause_info.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 100))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return  # Start the game

        pygame.display.flip()
        clock.tick(FPS)

# Main game loop
def game_loop():
    global player_pos, lives

    is_paused = False  # Pause state

    while True:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over()
                if event.key == pygame.K_p:  # Toggle pause
                    is_paused = not is_paused

        if not is_paused:  # Only update game if not paused
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
                player_pos[0] += player_speed

            # Create objects randomly
            if random.randint(1, 30) == 1:
                create_object(light_objects, LIGHT_BLUE)
            if random.randint(1, 50) == 1:
                create_object(heavy_objects, DARK_RED)

            # Update object positions
            update_objects(light_objects)
            update_objects(heavy_objects)

            # Check for collisions
            check_collisions(light_objects, True)
            check_collisions(heavy_objects, False)

            # Draw player
            player_rect = pygame.Rect(*player_pos, player_size, player_size)
            pygame.draw.rect(screen, WHITE, player_rect)

            # Draw objects
            for obj in light_objects:
                pygame.draw.rect(screen, obj[1], obj[0])
            for obj in heavy_objects:
                pygame.draw.rect(screen, obj[1], obj[0])

            # Draw score and lives
            score_text = font.render(f"Score: {score}", True, WHITE)
            lives_text = font.render(f"Lives: {lives}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))

            # Check for Game Over
            if lives <= 0:
                game_over()

        # Draw the PAUSED text if paused
        if is_paused:
            paused_text = font.render("PAUSED", True, WHITE)
            screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.flip()
        clock.tick(FPS)

# Start the game
show_menu()
game_loop()
