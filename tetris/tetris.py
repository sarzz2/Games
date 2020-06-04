import pygame
import random
import curses

pygame.font.init()

# Screen Width and height
s_width = 1000
s_height = 700
# Play width and height
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    # gives the position of the shape to be displayed after rotation
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            # for every 0 in the list we add it to the position list at the current location of the piece
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    # offsetting
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # flattens the list or makes it 1-D
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            # when they x and y values are negative the pieces are not allowed to move
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# returns a new random shape
def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (230, 600))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))
    # tetris font display
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render("Tetris", 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 30))

    # Tetris score display
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("SCORE: " + str(score), 1, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # to draw the playable rectangle
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)
    # pygame.display.update()


def main(win):
    locked_position = {}
    grid = create_grid(locked_position)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.4
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_position)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # To increase the speed of falling blocks
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_SPACE:
                    try:
                        current_piece.y += 5
                        if not (valid_space(current_piece, grid)):
                            current_piece.y -= 5
                    except:
                        continue

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_position[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_position) * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_position):
            win.fill((0, 0, 0))
            font = pygame.font.SysFont("Timesnewroman", 60, bold=True)
            score_font = pygame.font.SysFont("Timesnewroman", 40)
            high_score_file = open("tetris_score.txt")
            high_score = int(high_score_file.read())
            high_score_file.close()
            with open("tetris_score.txt", "w") as db:
                if score > high_score:
                    db.write(f"{score}")
                    high_score_text = score_font.render(f"High score: {score}", 80, (255, 255, 255), win)
                    win.blit(high_score_text, (350, 300))
                else:
                    db.write(f"{high_score}")
                    high_score_text = score_font.render(f"High score: {high_score}", 80, (255, 255, 255), win)
                    win.blit(high_score_text, (350, 300))

            label = font.render("GAME OVER", 100, (255, 255, 255), win)
            win.blit(label, (350, 100))
            dis_score = score_font.render(f"Your Score: {score}", 80, (255, 255, 255), win)
            win.blit(dis_score, (350, 350))
            draw_text_middle("Press Any Key To Play", 60, (255, 255, 255), win)
            pygame.display.update()
            run = False


def main_menu(win):
    run = True
    i = 0
    while run:
        i += 1
        if i <= 1:
            startup = pygame.transform.scale2x(pygame.image.load("img.png"))
            win.blit(startup, (0, 0))
            draw_text_middle("Press Any Key To Play", 60, (255, 255, 255), win)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                elif event.type == pygame.KEYDOWN:
                    main(win)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                elif event.type == pygame.KEYDOWN:
                    main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(win)  # start game
