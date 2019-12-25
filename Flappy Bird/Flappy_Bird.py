import pygame
import os
import random
pygame.font.init()
WIN_WIDTH = 575
WIN_HEIGHT = 900

# Loads the Images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird:
    IMGS = BIRD_IMGS
    # to tilt the head of the bird up by 25 degree
    MAX_ROTATION = 25
    ROT_VEL = 35
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -9  # Change this number to adjust the speed
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        # when vel = -10.5 and count = 1 it moves upward by -9 and keeps increasing as tick_count increases until it
        # reaches 0 and start becomes positive then it starts moving downwards
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        # if d >= 16 then the value of d doesn't increase more so it doesn't go down too fast
        if d >= 12:
            d = 12
        # To fine tune the movements
        if d < 0:
            d -= 2
        self.y = self.y + d
        # If the bird is above the starting position then keep the head tilted up until it goes below the starting postion
        if d < 0 or self.y < self.height + 50:
            # Makes sure that the head of the bird doesn't tilt more than 25 degree when it's going up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
            # Makes the bird seem like it's nosediving at an 90 degree angle
            elif self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        # To set the frame
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 5:
            self.img = self.IMGS[0]
            self.img_count = 0
        # To set the the image of the bird when it's going down so it doesn't flap or skip a frame
        if self.tilt <= - 90:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        # To rotate the image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 8

    # The bird doesn't move the object i.e. the pipe moves therefore initialising the vel variable
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        # The pipes on the top of the screen
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        # The pipe on the bottom of the screen
        self.PIPE_BOTTOM = PIPE_IMG
        self.BASE = BASE_IMG
        self.passed = False
        # the function to set the gap between the pipes
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        # Sets the top pipe position
        self.top = self.height - self.PIPE_TOP.get_height()
        # Sets the bottom pipe position
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        # Mask identifies the pixels to get a perfect collision
        bird_mask = bird.get_mask()
        # Getting the pixels of the pipes
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        base_mask = pygame.mask.from_surface(self.BASE)
        # Gets the coordinates of the pipes
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        # Checks if the bird and pipe collides
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        base_point = bird_mask.overlap(base_mask, top_offset)
        if t_point or b_point or base_point:
            return True
        return False


class Base:
    VEL = 8
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        # There are 2 images one on screen and one which is not visible on screen
        # When 1st image starts moving out the 2nd image starts moving in
        # When the 1st image is completely off the screen it takes place of the 2nd image and starts moving in again.
        # off screen --|on screen|-- off screen
        #              |1st      |--   2nd
        #            1st    --   2nd
        #       1st    |    2nd  |
        #              | 2nd     | 1st
        # and the process repeats
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
    # Blit draws the window
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    # For the score to display on the screen
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))            # So that the score doesn't go off the screen

    base.draw(win)
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    start = True
    run = True

    while start:
        win.blit(BG_IMG, (0, 0))
        start_text = pygame.font.SysFont('Consolas', 100).render("PRESS ANY KEY TO START", True, pygame.color.Color('White'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                start = False
            if event.type == pygame.KEYDOWN:
                start = False
            win.blit(start_text, (10, 220))
            pygame.display.update()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:  # Mouse button pressed DOWN( Up would be at release)
                if event.key == pygame.K_p:
                    pause_text = pygame.font.SysFont('Consolas', 90).render('PAUSED', True, pygame.color.Color('White'))
                    pause = True
                    while pause:
                        clock.tick(30)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    pause = False
                        win.blit(pause_text, (40, 250))
                        pygame.display.update()
            if event.type == pygame.KEYUP:
                bird.jump()

        add_pipe = False
        rem = []

        for pipe in pipes:
            if pipe.collide(bird):
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            pause = False
                        elif event.type == pygame.KEYDOWN:
                            main()
                    game_over = pygame.font.SysFont('Consolas', 100).render('GAME OVER', True, pygame.color.Color('White'))
                    win.blit(game_over, (100,100))
                    pygame.display.update()

            # Stores the pipe to be removed
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            # To create a new pipe when bird has passed through the previous pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1              # Increments the score
            pipes.append(Pipe(700))
        # Removes the pipe
        for r in rem:
            pipes.remove(r)
        # when the bird hits the floor
        if bird.y + bird.img.get_height() >= 730:
            pass
        bird.move()
        base.move()
        draw_window(win, bird, pipes, base, score)
    pygame.quit()
    quit()


main()
