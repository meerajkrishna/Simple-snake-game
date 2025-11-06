import tkinter as tk
import random

# Game settings
WIDTH = 400
HEIGHT = 400
SNAKE_ITEM_SIZE = 20
SPEED = 100  # milliseconds

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Snake Game By MR")
        
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.snake_squares = []
        self.direction = 'Right'
        self.food_position = ()
        self.food_square = None
        self.game_over = False
        
        self.create_snake()
        self.create_food()
        self.master.bind("<Key>", self.change_direction)
        self.move_snake()
    
    def create_snake(self):
        for position in self.snake_positions:
            square = self.canvas.create_rectangle(position[0], position[1], position[0] + SNAKE_ITEM_SIZE, position[1] + SNAKE_ITEM_SIZE, fill='green')
            self.snake_squares.append(square)

    def create_food(self):
        x = random.randint(0, (WIDTH - SNAKE_ITEM_SIZE) // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_ITEM_SIZE) // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
        self.food_position = (x, y)
        self.food_square = self.canvas.create_oval(x, y, x + SNAKE_ITEM_SIZE, y + SNAKE_ITEM_SIZE, fill='red')

    def move_snake(self):
        if self.game_over:
            return
        
        head_x, head_y = self.snake_positions[0]

        if self.direction == 'Left':
            new_head = (head_x - SNAKE_ITEM_SIZE, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + SNAKE_ITEM_SIZE, head_y)
        elif self.direction == 'Up':
            new_head = (head_x, head_y - SNAKE_ITEM_SIZE)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + SNAKE_ITEM_SIZE)
        
        # Check for collisions with walls
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            self.end_game()
            return
        
        # Check for collision with self
        if new_head in self.snake_positions:
            self.end_game()
            return
        
        # Insert new head in the snake body
        self.snake_positions = [new_head] + self.snake_positions[:-1]
        
        # Check if food eaten
        if new_head == self.food_position:
            self.snake_positions.append(self.snake_positions[-1])  # Grow snake tail
            self.canvas.delete(self.food_square)
            self.create_food()

        self.redraw_snake()
        self.master.after(SPEED, self.move_snake)

    def redraw_snake(self):
        for square in self.snake_squares:
            self.canvas.delete(square)
        self.snake_squares.clear()
        for position in self.snake_positions:
            square = self.canvas.create_rectangle(position[0], position[1], position[0] + SNAKE_ITEM_SIZE, position[1] + SNAKE_ITEM_SIZE, fill='green')
            self.snake_squares.append(square)

    def change_direction(self, event):
        new_direction = event.keysym
        all_directions = ['Left', 'Right', 'Up', 'Down']
        opposites = {'Left':'Right', 'Right':'Left', 'Up':'Down', 'Down':'Up'}
        if new_direction in all_directions and new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def end_game(self):
        self.game_over = True
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill='red', font=('Arial', 24))

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
