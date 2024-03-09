import pygame
import sys
import random

# Define the Snake class
class Snake(object):
    # Initialize the Snake object
    def __init__(self):
        # Initialize snake attributes
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        # Choose a random initial direction
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        # Set snake color
        self.color = (124, 252, 0)

    # Get the position of the head of the snake
    def get_head_pos(self):
        return self.positions[0]

    # Change the direction of the snake
    def turn(self, point):
         # Check if snake is not turning back on itself
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            # Update snake direction
            self.direction = point

    # Move the snake
    def move(self):
        current = self.get_head_pos()
        x, y = self.direction
        # Calculate new position based on current position and direction
        new = (((current[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (current[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        # Check if snake collides with itself
        if len(self.positions) > 2 and new in self.positions[2:]:
            # Reset the game if collision occurs
            self.reset()
        else:
            # Insert new position to snake positions list
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                # Remove the tail of the snake if it exceeds the length
                self.positions.pop()

    # Reset the snake to initial state
    def reset(self):
        self.length = 1
        # Reset snake position to the center of the screen
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        # Choose a random initial direction
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # Draw the snake on the surface
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            # Draw the snake's body
            pygame.draw.rect(surface, self.color, r)
            # Draw outline around each snake segment
            pygame.draw.rect(surface, (255, 255, 0), r, 1)

    # Handle the keyboard events
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

# Define the Food class
class Food(object):
    # Initialize the Food object
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        # Randomize initial position of the food
        self.randomize()

    # Randomize the position of the food
    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    # Draw the food on the surface
    def draw(self, surface):
        # Draw the food as a circle
        pygame.draw.circle(surface, self.color, (self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2), GRID_SIZE // 2)
        # Draw outline around the food
        pygame.draw.circle(surface, (255, 255, 0), (self.position[0] + GRID_SIZE // 2, self.position[1] + GRID_SIZE // 2), GRID_SIZE // 2, 1)

# Function to draw the grid on the surface
def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                # Draw grid cells with alternating colors
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (128, 128, 128), r)
            else:
                rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (169, 169, 169), rr)

# Define screen dimensions and grid properties
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

# Define directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Main function
def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    # Draw the initial grid
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace", 20, bold=True)

    score = 0

    # Main game loop
    while True:
      clock.tick(10)
      snake.handle_keys()
      drawGrid(surface)
      snake.move()
      if snake.get_head_pos() == food.position:
          snake.length += 1
          score += 1
          food.randomize()
      snake.draw(surface)
      food.draw(surface)
      screen.blit(surface, (0, 0))
      text = myfont.render("Score: " + str(score), True, (0, 0, 0))
      screen.blit(text, (5, 10))
      pygame.display.update()

main()
