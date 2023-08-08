import pygame as pg
from pygame.math import Vector2
import sys, random

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pg.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pg.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pg.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pg.image.load('Graphics/head_left.png').convert_alpha()
            
        self.tail_up = pg.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pg.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pg.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pg.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pg.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pg.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pg.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pg.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pg.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pg.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pg.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        #for block in self.body:
        #    x_pos = int(block.x * cell_size)
        #    y_pos = int(block.y * cell_size)
        #    block_rect = pg.Rect(x_pos,y_pos,cell_size,cell_size)
        #    pg.draw.rect(screen,(73,121,192),block_rect) # none of this is needed with images
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pg.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect) # chooses which image to display based on relation
                                                            # too other peices around it

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            self.new_block = False
            body_copy = self.body[:] # does not remove final block
        else:
            body_copy = self.body[:-1]

        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy[:] # moves snake head by direction

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

class FRUIT:
    def __init__(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

    def draw_fruit(self):
        fruit_rect = pg.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        #pg.draw.rect(screen,(255,26,74),fruit_rect) # not needed when using an image
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.draw_score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize() # makes sure apple does not spawn in snake

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over() # check if snake head is outside boundry
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pg.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (167,209,61)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pg.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pg.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pg.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pg.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, 255)
        score_x = (cell_size * cell_number - 60)
        score_y = (cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midleft = (score_rect.right, score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(apple,apple_rect)

pg.mixer.pre_init(44100, -16, 2, 512) # reduces sound buffering by pygame
pg.init()
width, height = 400,500
cell_size = 40
cell_number = 20
screen = pg.display.set_mode((cell_number*cell_size,cell_number*cell_size)) # create window
clock = pg.time.Clock() # framerate
apple = pg.image.load('Graphics/apple.png').convert_alpha()
game_font = pg.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE,125) # event is triggered every x ms

main_game = MAIN()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit() # quit
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pg.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pg.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pg.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)

    screen.fill((175,215,70))
    main_game.draw_elements()
    pg.display.update() # update display
    clock.tick(120)