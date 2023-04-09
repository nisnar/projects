import pygame
from pygame.locals import *  #import things like KEYDOWN
import time  #for DELAY
import random  #for random apple movement

#variables
block_size = 25
bg_color = (110, 110, 5)

class Apple:  #apple class
    def __init__(self, surface):  #apple constructor
        self.surface = surface  
        self.apple = pygame.image.load("apple.png")  #loading block image
        self.apple = pygame.transform.scale(self.apple, (25, 25))  #resizing image
        self.x = block_size*3
        self.y = block_size*3
    
    def draw(self):  #draw an apple
        self.surface.blit(self.apple, (self.x, self.y))
        pygame.display.flip()  #updating
    
    def move(self):  #move to random position
        self.x = random.randint(1, 19)*block_size
        self.y = random.randint(1, 19)*block_size


class Snake:  #snake class
    def __init__(self, surface, length):  #snake constructor
        self.surface = surface  
        self.block = pygame.image.load("block.jpg")  #loading block image
        self.block = pygame.transform.scale(self.block, (block_size, block_size))  #resizing image
        self.direction = 'down'  #starting point

        self.length = length
        self.x = [block_size]*length  #starting point
        self.y = [block_size]*length  #starting point
    
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    #movement functions
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    
    def walk(self): 
        for i in range(self.length-1, 0, -1):  # (i = 0, i < self.length -1, i--)
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= block_size
        if self.direction == 'down':
            self.y[0] += block_size
        if self.direction == 'left':
            self.x[0] -= block_size
        if self.direction == 'right':
            self.x[0] += block_size
        self.draw()
    
    def draw(self):  #draw a block (piece of snake)
        self.surface.fill(bg_color)
        for i in range(self.length):  #create multiple blocks. the move function will unravel the snake.
            self.surface.blit(self.block, (self.x[i], self.y[i]))  #draw an single block
            if i == 0:  #draw eyes on first block
                if self.direction == 'right' or self.direction == 'left':
                    pygame.draw.circle(self.surface, (0, 0, 0), (self.x[i]+block_size/2, self.y[i]+block_size/2 - 5), 2)
                    pygame.draw.circle(self.surface, (0, 0, 0), (self.x[i]+block_size/2, self.y[i]+block_size/2 + 5), 2)
                else:
                    pygame.draw.circle(self.surface, (0, 0, 0), (self.x[i]+block_size/2 - 5, self.y[i]+block_size/2), 2)
                    pygame.draw.circle(self.surface, (0, 0, 0), (self.x[i]+block_size/2 + 5, self.y[i]+block_size/2), 2)
        pygame.display.flip()  #updating

class Game:  #Game class
    def __init__(self):  #Game constructor
        pygame.init()  #initialize library

        pygame.mixer.init()  #initalize sound module
        self.play_bg_music()

        self.surface = pygame.display.set_mode((500, 500))  #window size
        self.snake = Snake(self.surface, 1)  #create snake object on surface
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + block_size:
            if y1 >= y2 and y1 < y2 + block_size:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (350, 10))

    def play_bg_music(self):
        pygame.mixer.music.load("bg_music.mp3")
        pygame.mixer.music.play()

    def play_sound(self, name):
        sound = pygame.mixer.Sound(f"{name}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()  #snake moves without key press
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("munch")
            self.snake.increase_length()
            self.apple.move()
        
        #snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("hiss")
                raise "Game over" 

    def show_game_over(self):
        self.surface.fill(bg_color)
        font = pygame.font.SysFont('arial', 20)
        line1 = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(line1, (40, 200))
        line2 = font.render("To play again, press Enter. To exit, press Escape!", True, (200, 200, 200))
        self.surface.blit(line2, (40, 250))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
            
    def run(self):  #run the game
        running = True
        pause = False
        while running:  #event loop
            for event in pygame.event.get():  #an event is a keyboard/mouse input
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  #if press escape, quit
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if event.key == K_UP:  #movement keys
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)  #snake moves every 0.2 seconds


if __name__ == "__main__":  #if being used as a main.py program...
    game = Game()
    game.run()
    

