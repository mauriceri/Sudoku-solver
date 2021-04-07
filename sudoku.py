import sys
import pygame as pg

pg.init()

screen_size = 750, 800

font = pg.font.SysFont(None, 80)
text = pg.font.SysFont(None, 40)

text_surface = text.render("Press Space to show solution", False, (0, 0, 0))

screen = pg.display.set_mode(screen_size)

game_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


def draw_background():
    # Set background to white
    screen.fill(pg.Color("white"))

    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)

    # draw grid
    i = 1
    while (i * 80) < 720:
        line_width = 5 if i % 3 > 0 else 10
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15),
                     pg.Vector2((i * 80) + 15, 735), line_width)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15),
                     pg.Vector2(735, (i * 80) + 15), line_width)

        i += 1


def draw_numbers():
    row = 0
    offset = 37
    while row < 9:
        col = 0
        while col < 9:
            out = game_grid[row][col]

            if out > 0:
                number_text = font.render(str(out), True, pg.Color("black"))
                screen.blit(number_text, pg.Vector2((col * 80) + offset+3, (row*80)+offset-5))
            col += 1

        row += 1


def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return i, j

    return None


def is_valid_input(y, x, n):
    global game_grid
    # check if input number n is already in y or x axis
    for i in range(0, 9):
        if game_grid[y][i] == n:
            return False

    for i in range(0, 9):
        if game_grid[i][x] == n:
            return False

    # calculate pos of 3x3 field
    x0 = (x//3) * 3
    y0 = (y//3) * 3

    for i in range(0, 3):
        for j in range(0, 3):
            if game_grid[y0+i][x0+j] == n:
                return False
    return True


def solve(grid):
    find = find_empty(grid)

    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid_input(row, col, i):
            grid[row][col] = i

            if solve(grid):
                return True

            grid[row][col] = 0

    return False


def game_loop():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                solve(game_grid)

    draw_background()
    draw_numbers()
    screen.blit(text_surface, (190, 760))
    pg.display.flip()


while True:
    game_loop()

