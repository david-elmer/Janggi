# This is the pygame driver for the JanggiGame backend
#
# Includes functions for converting x-y coordinates on the screen
# to 'algebraic notation' where game board rows are numbers
# from 1 to 10 and columns are letters from a to i.

import pygame
import JanggiGame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG_X_OFFSET, BG_Y_OFFSET, \
    FILL_COLOR, BLUE, RED, XY_WINNER, XY_PLAYER, XY_PLAYER_COLOR


def get_algebraic_from_mouse(x_coord, y_coord):
    """
    Translates mouse coordinates to algebraic notation.

    :param x_coord: int - x coordinate of the mouse
    :param y_coord: int - y coordinate of the mouse
    :return: string - letter and number in algebraic notation
    """
    letter = ''
    number = ''
    x_coord -= BG_X_OFFSET
    y_coord -= BG_Y_OFFSET

    # x to letter
    if x_coord < 0 or x_coord > 603:
        print('x coordinate is off the board')
    elif x_coord <= 67:
        letter = 'a'
    elif x_coord <= 134:
        letter = 'b'
    elif x_coord <= 201:
        letter = 'c'
    elif x_coord <= 268:
        letter = 'd'
    elif x_coord <= 335:
        letter = 'e'
    elif x_coord <= 402:
        letter = 'f'
    elif x_coord <= 469:
        letter = 'g'
    elif x_coord <= 536:
        letter = 'h'
    else:
        letter = 'i'

    # y to number
    if y_coord < 0 or y_coord > 670:
        print("y coordinate is off of the board")
    elif y_coord <= 67:
        number = '1'
    elif y_coord <= 134:
        number = '2'
    elif y_coord <= 201:
        number = '3'
    elif y_coord <= 268:
        number = '4'
    elif y_coord <= 335:
        number = '5'
    elif y_coord <= 402:
        number = '6'
    elif y_coord <= 469:
        number = '7'
    elif y_coord <= 536:
        number = '8'
    elif y_coord <= 603:
        number = '9'
    else:
        number = '10'

    return letter + number


def get_xy_from_algebraic(location):
    """
    Translates algebraic notation into x, y location.
    Location in algebraic notation is a string containing the
    column and row in order where column is a letter a-i
    and row is a number 1-10. Example: "b7"
    Location in (x, y) notation gives the upper-left corner
    of the square denoted by the string. x and y are offset
    based on the location of the game board on the screen.

    :param location: A string containing the algebraic notation
                     to convert
    :return: (x_coord, y_coord) where x and y are integers
                     and represent a location on the display
    """
    x_key = {
        "a": 0,
        "b": 67,
        "c": 134,
        "d": 201,
        "e": 268,
        "f": 335,
        "g": 402,
        "h": 469,
        "i": 536
    }

    y_key = {
        "1": 0,
        "2": 67,
        "3": 134,
        "4": 201,
        "5": 268,
        "6": 335,
        "7": 402,
        "8": 469,
        "9": 536,
        "10": 603
    }

    column = x_key[location[0]]

    if len(location) == 3:
        row = y_key[location[1:]]
    else:
        row = y_key[location[1]]

    x_coord = column + BG_X_OFFSET
    y_coord = row + BG_Y_OFFSET

    return x_coord, y_coord


# initialize pygame
pygame.init()
game = JanggiGame.JanggiGame()

# -----------------------------------------------------------------------------
# TEST CODE - Plays a game where blue wins
# -----------------------------------------------------------------------------

# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('a7', 'b7')
# game.make_move('i4', 'h4')
# game.make_move('h10', 'g8')
# game.make_move('c1', 'd3')
# game.make_move('h8', 'e8')
# game.make_move('i1', 'i2')
# game.make_move('e7', 'f7')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('b3', 'e3')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('g10', 'e7')
# game.make_move('e4', 'd4')
# game.make_move('c10', 'd8')
# game.make_move('g1', 'e4')
# game.make_move('f10', 'f9')
# game.make_move('h1', 'g3')
# game.make_move('a10', 'a6')
# game.make_move('d4', 'd5')
# game.make_move('e9', 'f10')
# game.make_move('h3', 'f3')
# game.make_move('e8', 'h8')
# game.make_move('i2', 'h2')
# game.make_move('h8', 'f8')
# game.make_move('f1', 'f2')
# game.make_move('b8', 'e8')
# game.make_move('f3', 'f1')
# game.make_move('i7', 'h7')
# game.make_move('f1', 'c1')
# game.make_move('d10', 'e9')
# game.make_move('a4', 'b4')
# game.make_move('a6', 'a1')
# game.make_move('c1', 'a1')
# game.make_move('f8', 'd10')
# game.make_move('d5', 'c5')
# game.make_move('i10', 'i6')
# game.make_move('b1', 'd4')
# game.make_move('c7', 'c6')
# game.make_move('c5', 'b5')
# game.make_move('b10', 'd7')
# game.make_move('d4', 'f7')
# game.make_move('g7', 'f7')
# game.make_move('a1', 'f1')
# game.make_move('g8', 'f6')
# game.make_move('f1', 'f5')
# game.make_move('f6', 'd5')
# game.make_move('e3', 'e5')
# game.make_move('f7', 'f6')
# game.make_move('f5', 'f7')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('f10', 'e10')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('e2', 'f1')
# game.make_move('i6', 'i3')
# game.make_move('h2', 'g2')
# game.make_move('i3', 'i1')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('f1', 'e2')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('f6', 'f5')
# game.make_move('c4', 'd4')
# game.make_move('f5', 'e5')
# game.make_move('f7', 'd7')
# game.make_move('e7', 'g4')
# game.make_move('d4', 'd5')
# game.make_move('e5', 'e4')
# game.make_move('d3', 'e5')
# game.make_move('e4', 'e3')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('e2', 'd2')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('e3', 'e2')
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# print(game.make_move('d2', 'd3'))
# print(game.is_in_check('red'))
# print(game.is_in_check('blue'))
# game.make_move('e8', 'e4')
# game.make_move('f2', 'e2')
# game.make_move('i1', 'd1')
# game.make_move('e2', 'd2')
# print(game.make_move('d1', 'f3'))
# print(game.get_game_state())
# game.print_board()

# -----------------------------------------------------------------------------

# display title and icon
pygame.display.set_caption('Janggi: Korean Chess')
icon = pygame.image.load('images/Red_King.png')
pygame.display.set_icon(icon)

# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# add the background
background = pygame.image.load('images/janggi_board_603x670.png')

# FONTS
# current player
font_player = pygame.font.Font('fonts/Montserrat/Montserrat-SemiBold.ttf', 18)
# title
font_title = pygame.font.Font('fonts/KaushanScript-Regular.ttf', 40)
# winner
font_winner = pygame.font.Font('fonts/Montserrat/Montserrat-Bold.ttf', 64)

# initialize variables
source_square = None
destination_square = None
highlight = None

# game loop
running = True

while running:
    game_over = False
    # generate window fill, title, and background
    screen.fill(FILL_COLOR)
    screen.blit(background, (BG_X_OFFSET, BG_Y_OFFSET))
    title = font_title.render('Janggi', True, (0, 0, 0))
    screen.blit(title, (250, 0))

    # if game is in progress, display current player, otherwise display winner
    # generate current player message
    if game.get_game_state() == "UNFINISHED":
        current_player = game.get_current_player().get_color().upper()
        text_player = font_player.render(f'Current player:', True, (0, 0, 0))
        screen.blit(text_player, XY_PLAYER)
        if current_player == 'BLUE':
            text_current_player = font_player.render(current_player, True, BLUE)
        else:
            text_current_player = font_player.render(current_player, True, RED)
        screen.blit(text_current_player, XY_PLAYER_COLOR)
    # generate winner message
    else:
        if game.get_game_state() == 'BLUE_WON':
            winner = font_winner.render('BLUE WON', True, BLUE)
        else:
            winner = font_winner.render('RED WON', True, RED)
        game_over = True

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if source_square is None:
                source_square = get_algebraic_from_mouse(x, y)
                game.get_board().set_highlight(source_square)

            else:
                destination_square = get_algebraic_from_mouse(x, y)
                game.make_move(source_square, destination_square)
                source_square = None
                game.get_board().clear_highlight()

    # draw game pieces
    game.get_board().draw_board(screen)

    # display winner if game over
    if game_over:
        screen.blit(winner, XY_WINNER)

    pygame.display.update()
