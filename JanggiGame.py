# Author:   David Elmer
# Date:     03/03/2021
# Description:  Creates a virtual version of a game called Janggi,
#   or Korean Chess. Declares classes called JanggiGame, Player, Board,
#   a parent class Piece and subclasses of Piece for each of the seven
#   game pieces. The game interface is played through the JanggiGame
#   class which communicates with the other classes to implement game
#   functionality.


import pygame
from constants import BG_X_OFFSET, BG_Y_OFFSET
from termcolor import colored


class JanggiGame:
    """
    JanggiGame is the user interface for the game. It initializes the
    game state for a new game. JanggiGame objects communicate with
    the Player class and the Board class. It creates Player objects
    for each side and a Board object to represent the game board.
    JanggiGame handles input from the user to make moves, return the
    game state, and return whether a specified player is in check.
    """

    def __init__(self):
        """
        Constructs a JanggiGame object and creates two player objects
        (blue and red), a game board object and initializes,
        sets the game state to 'UNFINISHED', ands sets the current
        player to blue.
        """
        self._blue = Player("blue")
        self._red = Player("red")
        self._board = Board(self)
        self._board.initialize_board()
        self._game_state = "UNFINISHED"
        self._current_player = self._blue

    def get_blue(self):
        """
        Returns the player object held in self._blue.
        Used by a board object to determine attackers and defenders
        in the board.is_in_check and the board.checkmate methods.

        :return: Player object
        """
        return self._blue

    def get_red(self):
        """
        Returns the player object held in self._red.
        Used by a board object to determine attackers and defenders
        in the board.is_in_check and the board.checkmate methods.

        :return: Player object
        """
        return self._red

    def get_board(self):
        """
        Returns the Board object held in self._board.
        Used by the print board method.

        :return: Board object
        """
        return self._board

    def print_board(self):
        """
        Calls the print_board method of the board object.
        Prints the game board to the console screen. Included
        for debugging purposes.

        :return: None
        """
        self._board.print_board()

    def get_game_state(self):
        """
        Returns the current game state.

        :return: string:    'UNFINISHED',
                            'RED_WON', or
                            'BLUE_WON'
        """
        return self._game_state

    def set_game_state(self, game_state):
        """
        Sets the current game state. Called by self.make_move()
        when there is a change in the state of the game. The state
        of the game changes when a checkmate occurs.

        :param game_state: string   'UNFINISHED',
                                    'RED_WON', or
                                    'BLUE_WON'
        :return: None
        """
        self._game_state = game_state

    def get_current_player(self):
        """
        Returns the Player object whose turn it is currently.
        Used by self.make_move() and various methods of the Board class.
        :return: Player object referenced by self._blue or self._red
        """
        return self._current_player

    def set_current_player(self, player):
        """
        Takes a player object and sets the current player to that
        object. Used by self.make_move() when there is a change
        of turn in the game.

        :param player: Player object self._blue or self._red
        :return: None
        """
        self._current_player = player

    def toggle_players(self):
        """
        Determines who is the current player and switches to the other
        player. Takes no arguments and returns None.
        Used by self.make_move.

        :return: None
        """
        if self.get_current_player() is self.get_blue():
            self.set_current_player(self.get_red())
        else:
            self.set_current_player(self.get_blue())

    def is_in_check(self, color):
        """
        Returns whether a given player is in check or not. This method
        is implemented by calling Board.is_in_check() and passing it a
        a player object. self.is_in_check determines which player
        object to pass by decoding the string parameter passed to it.

        :param color:   string: 'red' or 'blue'
        :return:    True if the given player is in check, or
                    False if the given player is not in check.
        """
        if color == 'blue':
            return self.get_board().is_in_check(self.get_blue())
        else:
            return self.get_board().is_in_check(self.get_red())

    def make_move(self, source, destination):
        """
        Performs the mechanics of making a move in the game. This
        method is called by the user who passes two strings--a
        source and a destination. The make_move method determines
        which player is making the move and determines whether it
        is a legal move. If the move is legal, the move is recorded
        along with any consequences of the move, i.e. a piece is
        captured or a checkmate occurs. The method returns True if
        a legal move has been requested and False otherwise.

        :param source: string containing the algebraic notation
                       for where the piece is moving from.
        :param destination: string containing the algebraic notation
                            for where the piece is moving to.
        :return: True if:  the move is legal and has been recorded.
                 False if: the wrong player is attempting to move,
                           the move is not legal, or
                           the game has already been won.
        """
        # test print statement for debugging with Gradescope
        # print(f"game.make_move('{source}', '{destination}')")

        # check and handle game already over
        if self.get_game_state() != "UNFINISHED":
            return False

        # check and handle player passing turn
        if source == destination:
            # if passing player is in check, move is not allowed
            if self.is_in_check(self.get_current_player().get_color()):
                return False
            # otherwise, toggle players and return true
            else:
                self.toggle_players()
                return True

        # check and handle no piece on source square
        if self.get_board().get_occupant(source) is None:
            return False

        # check and handle wrong player attempting to move
        if (self.get_board().get_occupant(source).get_owner()
                is not self.get_current_player()):
            return False

        # check if the requested move is legal
        if self.get_board().is_legal(source, destination):
            # if the move is legal, move the piece
            self.get_board().move_piece(source, destination)
            # toggle players and check for checkmate
            self.toggle_players()
            # if the newly current player is in checkmate,
            # the other player has won
            if self.get_board().is_in_checkmate(self.get_current_player()):
                if self.get_current_player() is self.get_blue():
                    self.set_game_state("RED_WON")
                else:
                    self.set_game_state("BLUE_WON")
            return True

        else:  # if the requested move is not legal
            return False


class Player:
    """
    Represents a player in a game of Janggi. A player has a color and
    a collection of game pieces (referred to as the player's 'cart').
    A player object is created by the JanggiGame class and interacts
    with the Board class. JanggiGame assigns a player's color.
    The Board class will add and remove pieces from the player's cart,
    get the player's General piece object, and get the player's color.
    """

    def __init__(self, color):
        """
        Constructs a Player object and initializes variables. A Player
        object is created by a JanggiGame object which assigns it the
        color 'blue' or 'red'. The player's cart is initialized as
        an empty list to which Piece objects are added and removed.

        :param color:   string: 'blue' or 'red'
        """
        self._color = color
        self._cart = []

    def __repr__(self):
        """
        Printing the player object will display the string describing
        the player's color.

        :return: string: 'blue' or 'red'
        """
        return repr(self._color)

    def get_color(self):
        """
        Returns a string describing the player's color. Used by
        Board.is_in_check() to determine which player object is
        being evaluated.

        :return: string:    'red' or 'blue'
        """
        return self._color

    def get_cart(self):
        """
        Returns a list containing all of the piece objects that are
        in the player's holdings. Used by the Board class for
        evaluating check and checkmate scenarios.
        :return: list containing Piece objects belonging to the player.
        """
        return self._cart

    def add_piece(self, piece):
        """
        Adds a given piece object to the player's cart.
        Called by a board object when initializing the game board.

        :param piece: Piece object
        :return: None
        """
        self._cart.append(piece)

    def remove_piece(self, piece):
        """
        Removes a given piece object from the player's cart.
        Called by board.make_move when a piece is captured.

        :param piece: Piece object
        :return: None
        """
        if piece in self.get_cart():
            self._cart.remove(piece)

    def get_general(self):
        """
        Returns the General object belonging to the player. Used by
        the Board class for evaluating check and checkmate scenarios.

        :return: General object
        """
        general = None

        for piece in self.get_cart():
            if piece.get_name() == "GN":  # "GN" specifies a General
                general = piece

        return general


class Board:
    """
    Represents the game board in a game of Janggi. The Board class
    performs the bulk of the computation in the game. It is responsible
    for keeping track of the state of the game board as well as
    evaluating if moves are legal and determining whether a player is
    in check or checkmate. The Board class interacts with the JanggiGame,
    Player, and Piece classes. The JanggiGame object creates the Board
    object and calls Board methods to determine whether moves are legal,
    whether a player is in check, and whether a player is in checkmate.
    The Board class creates Piece objects for the initial game setup
    and adds those pieces to the player's cart. The Board class also
    calls methods in the Piece classes to evaluate legal moves
    for each piece and provide a list of spaces that a piece will
    move through on a given move.
    The game board is implemented as a list of lists, where each
    sublist represents a row on the board and each element in the
    sublist represents a column in that row. A space which is
    occupied contains a Piece object and an empty space contains
    the value None. Addressing of the board within in the Board class
    and between the Board and the Piece classes is communicated
    as indexes of the list of lists. There is a decode_location
    function and an encode_location function that translate the
    strings containing algebraic notation (i.e. 'a1') to and from
    row and column notation (i.e. (0,0)).
    """

    def __init__(self, game):
        """
        Constructs a Board object and initializes variables.
        The Board object is passed a reference to the game object
        that created it so that the Board object can access the
        game.get_current_player method for use in the
        board.is_legal method. Also creates a variable _board that
        holds the game board.
        _board is initialized to an empty list and there is an
        initialize_board method to populate the board with the
        opening setup.

        :param game: a JanggiGame object
        """
        self._game = game
        self._board = []
        self._temp = None  # temporary storage for undoing move
        self._highlight = None

    def __repr__(self):
        """
        Included for debugging purposes. When game board object is
        printed, result will be "Game Board"

        :return: "Game Board"
        """
        return "Game Board"

    def initialize_board(self):
        """
        Creates Piece objects (i.e. Guard, Soldier, etc.) for each
        player and populates the game board according to the opening
        setup of the game. A Piece object is created in
        each of the spaces that they occupy at the beginning of the
        game and None is assigned to any empty spaces. The board
        is created by using row, column notation and any strings
        containing algebraic notation will have to be converted.
        After creating the game board, piece objects are also
        added to their respective player's cart.

        :return: None
        """
        red = self.get_game().get_red()
        blue = self.get_game().get_blue()

        self._board = [
            [
                Chariot("CH", "a1", red, self),
                Elephant("EL", "b1", red, self),
                Horse("HO", "c1", red, self),
                Guard("GD", "d1", red, self),
                None,
                Guard("GD", "f1", red, self),
                Elephant("EL", "g1", red, self),
                Horse("HO", "h1", red, self),
                Chariot("CH", "i1", red, self)
            ],
            [
                None, None, None, None,
                General("GN", "e2", red, self),
                None, None, None, None
            ],
            [
                None, Cannon("CA", "b3", red, self),
                None, None, None, None, None,
                Cannon("CA", "h3", red, self), None
            ],
            [
                Soldier("SD", "a4", red, self), None,
                Soldier("SD", "c4", red, self), None,
                Soldier("SD", "e4", red, self), None,
                Soldier("SD", "g4", red, self), None,
                Soldier("SD", "i4", red, self)
            ],
            [
                None, None, None, None, None, None, None, None, None
            ],
            [
                None, None, None, None, None, None, None, None, None
            ],
            [
                Soldier("SD", "a7", blue, self), None,
                Soldier("SD", "c7", blue, self), None,
                Soldier("SD", "e7", blue, self), None,
                Soldier("SD", "g7", blue, self), None,
                Soldier("SD", "i7", blue, self)
            ],
            [
                None, Cannon("CA", "b8", blue, self),
                None, None, None, None, None,
                Cannon("CA", "h8", blue, self), None
            ],
            [
                None, None, None, None,
                General("GN", "e9", blue, self),
                None, None, None, None
            ],
            [
                Chariot("CH", "a10", blue, self),
                Elephant("EL", "b10", blue, self),
                Horse("HO", "c10", blue, self),
                Guard("GD", "d10", blue, self),
                None,
                Guard("GD", "f10", blue, self),
                Elephant("EL", "g10", blue, self),
                Horse("HO", "h10", blue, self),
                Chariot("CH", "i10", blue, self)
            ]
        ]

        # add pieces to respective players' carts
        board = self.get_board()
        for row in range(len(board)):

            for column in range(len(board[row])):
                piece = board[row][column]

                if piece is not None:
                    if piece.get_owner() is blue:
                        blue.add_piece(piece)  # add to blue's cart
                    else:
                        red.add_piece(piece)  # add to red's cart

    def print_board(self):
        """
        Used for debugging purposes.
        Prints the game board to the console screen.
        Each sublist is printed directly to the screen, so piece
        abbreviations must match the number of characters in None
        so that columns will line up with each other.

        :return: None
        """
        print("     a     b     c     d     e     f     g     h     i")

        for i in range(len(self.get_board()) - 1):
            print(f" {i + 1}", self.get_board()[i])

        print("10", self.get_board()[9])

    def draw_board(self, window):
        """
        Used by the game interface to draw the game board.
        Loads a piece image for each piece on the board
        and writes them to the display. If highlight contains
        a piece location, then load and display the highlighted
        image for that piece.

        :param window: Display window from pygame
        :param highlight: string - algebraic notation of piece
                          to highlight
        :return: None
        """
        board = self.get_board()
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                # draw the image for the piece
                if piece is None:
                    continue
                else:
                    image = pygame.image.load(piece.get_image())
                    location = piece.get_location()
                    x, y = self.get_xy_from_algebraic(location)
                    window.blit(image, (x, y))

        # draw the highlighted piece
        highlight = self.get_highlight()
        if highlight is not None:
            piece = self.get_occupant(highlight)
            if piece is not None:  # if not empty square
                image = pygame.image.load(piece.get_image_highlight())
                x, y = self.get_xy_from_algebraic(highlight)
                window.blit(image, (x, y))

    def get_board(self):
        """
        Returns the _board data member of the board object.
        Used by Piece objects for determining legal moves.

        :return: self._board - a list of lists representing
                                the game board
        """
        return self._board

    def get_game(self):
        """
        Returns the _game data member of the board object.

        :return: self._game - the game object that created this board
                              object
        """
        return self._game

    def get_temp(self):
        """
        Returns the piece (or None) stored in temporary storage
        for the purposes of undoing a temporary move.

        :return: Piece object
        """
        return self._temp

    def set_temp(self, piece):
        """
        Stores a piece temporarily for the purposes of undoing a
        temporary move.

        :param piece: Piece object
        :return: None
        """
        self._temp = piece

    def get_highlight(self):
        """
        Returns the value of _highlight. Highlight contains the
        location in algebraic notation of a selected piece to
        highlight when drawing the baord.

        :return: _highlight - a string containing the highlighted
            location or None if no location is highlighted
        """
        return self._highlight

    def set_highlight(self, location):
        """
        Sets the value of _highlight. Highlight contains the
        location in algebraic notation of a selected piece to
        highlight when drawing the board.

        :param location: string - location in algebraic notation
                         of piece to highlight
        :return: None
        """
        self._highlight = location

    def clear_highlight(self):
        """
        Sets the value of _highlight to None. Highlight contains the
        location in algebraic notation of a selected piece to
        highlight when drawing the board.

        :return: None
        """
        self._highlight = None

    def prep_temp_move(self, destination):
        """
        Stores the piece at the destination square in preparation
        for making a temporary move.
        To make and undo a temporary move:
        1) call prep_temp_move to save the piece at the destination
        2) call move_piece with the intended source and destination
        3) insert whatever logic is desired before restoring
        to before the temporary move
        4) call undo_temp_move to put the pieces back where they were
        before the temporary move.

        :param destination: string - algebraic notation for a location
            on the board, determines the piece to save for restoration
        :return: None
        """
        row, column = self.decode_location(destination)
        self.set_temp(self.get_board()[row][column])

    def undo_temp_move(self, source, destination):
        """
        Reverses a temporary move by restoring the pieces to where they
        where when prep_temp_move was called.
        To make and undo a temporary move:
        1) call prep_temp_move to save the piece at the destination
        2) call move_piece with the intended source and destination
        3) insert whatever logic is desired before restoring
        to before the temporary move
        4) call undo_temp_move to put the pieces back where they were
        before the temporary move.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: None
        """
        # set up variables
        board = self.get_board()
        temp_piece = self.get_temp()
        source_row, source_column = self.decode_location(source)
        dest_row, dest_column = self.decode_location(destination)

        # restore piece back to source
        board[source_row][source_column] = board[dest_row][dest_column]
        board[source_row][source_column].set_location(source)

        # restore piece to destination (restores to empty square
        # if there was no piece there originally)
        board[dest_row][dest_column] = temp_piece
        # if there was a piece to restore:
        if temp_piece is not None:
            # add piece back to owner's cart
            temp_piece.get_owner().add_piece(temp_piece)
        # empty temporary piece storage
        self.set_temp(None)

    def get_occupant(self, location):
        """
        Returns the piece object at a given location. Used by
        Piece objects for determining legal moves.

        :param location: string - algebraic notation for a location
                                    on the board
        :return: Piece object located on the given location
        """
        row, column = self.decode_location(location)
        return self.get_board()[row][column]

    def move_piece(self, source, destination):
        """
        Moves a Piece object from a specified source location to a
        specified destination location. This method will remove a
        captured piece (if any) from the destination, place the source
        piece on the destination, and remove the piece from the source.
        Note that there is no legal move validation performed through
        this method. Legal move validation is handled through the
        JanggiGame.make_move method which calls this method.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: None
        """
        board = self.get_board()
        blue = self.get_game().get_blue()
        red = self.get_game().get_red()
        source_row, source_column = self.decode_location(source)
        dest_row, dest_column = self.decode_location(destination)
        source_piece = board[source_row][source_column]
        dest_piece = board[dest_row][dest_column]

        # if the destination square is occupied, that piece is captured
        # and removed from the owner's cart
        if dest_piece is not None:
            if dest_piece.get_owner() is blue:
                blue.remove_piece(dest_piece)
            else:
                red.remove_piece(dest_piece)

        # the piece on the source is moved to the destination,
        # the piece's location is updated,
        # and the piece is removed from the source
        board[dest_row][dest_column] = source_piece
        source_piece.set_location(destination)
        board[source_row][source_column] = None

    def is_legal(self, source, destination):
        """
        Performs move validation for the JanggiGame make_move method.
        Asks the piece object at the source location if it can
        legally move to the destination location then checks if such
        a move puts that player in check (a player may not make a move
        that puts themself in check). To evaluate whether the move
        puts the player in check, the board state is saved and
        a temporary move is made so that is_in_check can be called.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: True if the move is legal
                 False if the move is not legal
        """
        # store variables for use throughout method
        source_row, source_column = self.decode_location(source)
        source_piece = self.get_board()[source_row][source_column]
        source_player = source_piece.get_owner()

        # ask the piece at the source if the move is a legal move
        # for that type of piece.

        # if the move is legal, check if it puts the player into
        # check (making it an illegal move)
        if source_piece.is_legal(source, destination):

            self.prep_temp_move(destination)  # store pieces for temp move
            self.move_piece(source, destination)  # make a temp move

            # check if this move put the player in check
            if self.is_in_check(source_player):
                self.undo_temp_move(source, destination)  # restore game board
                return False  # is not legal
            else:
                self.undo_temp_move(source, destination)  # restore game board
                return True  # is legal

        # if the move is not a legal move for the specified piece
        else:
            return False  # is not legal

    def is_in_check(self, player):
        """
        Determines whether a given player is in check. The method
        must be passed a player object (as opposed to the method
        in the JanggiGame class which is passed a string). This
        method is called by the JanggiGame object after decoding
        which player to evaluate.
        This method finds this player's general and then checks
        to see if any of the opposing player's pieces can make a
        legal move to capture this player's general.

        :param player: Player object to evaluate
        :return: True if the player is in check
                 False if the player is not in check
        """
        # find the player's opponent and save as variable
        if player.get_color() == 'blue':
            opponent = self.get_game().get_red()
        else:
            opponent = self.get_game().get_blue()

        # find the player's General's location
        general_location = player.get_general().get_location()

        # for every one of the opponent's pieces,
        # ask if they can make a legal move from their current location
        # to the defending general's location
        for piece in opponent.get_cart():
            current_location = piece.get_location()
            if piece.is_legal(current_location, general_location):
                return True

        # if we make it past the for-loop, the player is not in check
        return False

    def is_in_checkmate(self, player):
        """
        Determines whether a given player is in checkmate. The method
        must be passed a player object. This method is called by
        the JanggiGame object's make_move method.
        This method creates a list of pieces that are threatening
        the general, and determines if any of the defending player's
        pieces can capture or intercept the attacking pieces. The
        method also stores the game state and makes all legal moves
        for the defender's general to see if any of those moves get
        them out of check.

        :param player: Player object to evaluate
        :return: True if the player is in checkmate
                 False if the player is not in checkmate
        """
        # check if the player is in check
        if not self.is_in_check(player):
            return False

        # set up variables for use throughout method
        if player.get_color() == 'blue':
            opponent = self.get_game().get_red()
            palace = ["d8", "d9", "d10", "e8", "e9", "e10", "f8", "f9", "f10"]
        else:
            opponent = self.get_game().get_blue()
            palace = ["d1", "d2", "d3", "e1", "e2", "e3", "f1", "f2", "f3"]
        general = player.get_general()
        gen_loc = general.get_location()
        attacker_list = []

        # populate list of opponent pieces that threaten the general
        for piece in opponent.get_cart():
            if self.is_legal(piece.get_location(), gen_loc):
                attacker_list.append(piece)

        # for each piece in that list
        for attacker in attacker_list:
            # check if any of the defender's pieces can capture
            # the threatening piece
            for piece in player.get_cart():
                if self.is_legal(
                    piece.get_location(),
                    attacker.get_location()
                ):
                    return False
            # check if any of the defender's pieces can block
            # the threatening piece
            path = attacker.move_path(attacker.get_location(), gen_loc)
            for square in path:
                for piece in player.get_cart():
                    if self.is_legal(piece.get_location(), square):
                        return False

        # if the threatening pieces cannot be captured nor blocked,
        # attempt to move the General to move out of check
        for square in palace:
            if general.is_legal(gen_loc, square):
                # make a temporary move to see if the general is out of check
                self.prep_temp_move(square)
                self.move_piece(gen_loc, square)
                if not self.is_in_check(player):
                    self.undo_temp_move(gen_loc, square)
                    return False
                else:
                    self.undo_temp_move(gen_loc, square)

        # if the General cannot be moved out of check
        return True

    def decode_location(self, location):
        """
        Converts algebraic notation to row/column notation.
        Conversion is necessary for accessing the game board--which is
        a list of lists--and is accessed by index, starting at (0, 0)
        Location in algebraic notation is a string containing the
        column and row in order where column is a letter a-i
        and row is a number 1-10. Example: "b7"
        Location in row/column notation is a tuple (row, column).
        Row is the index of the row sublist of the board and
        column is the index of the element in that sublist that
        represents the column.
        In the above example, "b7" is converted to (1, 6)

        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :return: (row, column) where row and column are integers
        """
        column_key = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7,
            "i": 8
        }

        row_key = {
            "1": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
            "9": 8,
            "10": 9
        }

        column = column_key[location[0]]

        if len(location) == 3:
            row = row_key[location[1:]]
        else:
            row = row_key[location[1]]

        return row, column

    def encode_location(self, row, column):
        """
        Converts row/column notation to algebraic notation.
        Conversion is necessary for accessing the game board--which is
        a list of lists--and is accessed by index, starting at (0, 0)

        Location in row/column notation is a tuple (row, column).
        Row is the index of the row sublist of the board and
        column is the index of the element in that sublist that
        represents the column. Example: (6, 1)

        Location in algebraic notation is a string containing the
        column and row in order where column is a letter a-i
        and row is a number 1-10.

        In the above example, (6, 1) is converted to 'b7'


        :param row: int - index of the sublist of the game board
                          representing the row
        :param column: int - index of the element of the row sublist
                             of the game board representing the column
        :return: location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        """
        column_key = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
            8: 'i'
        }

        row_key = {
            0: '1',
            1: '2',
            2: '3',
            3: '4',
            4: '5',
            5: '6',
            6: '7',
            7: '8',
            8: '9',
            9: '10'
        }

        column = column_key[column]
        row = row_key[row]
        location = column + row

        return location

    def get_xy_from_algebraic(self, location):
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


class Piece:
    """
    Represents a piece in a Janggi game.
    Piece is the parent class of all of the individual pieces
    in the game. Piece objects interact with Board objects--which
    create them--and Player objects.
    Piece objects have a name, location, owner, and a reference to
    the board object that created them.
    Piece objects can determine their legal moves and can create a list
    of squares through which they must pass to achieve those moves.
    A Piece object must interact with the board object so it can get
    information on the location of other pieces on the board.
    Player objects must interact with the piece object so that they
    can determine which piece is their general.
    """

    def __init__(self, name, location, owner, board):
        """
        Constructs a Piece object and initializes variables.

        :param name: A string containing a two-letter abbreviation
                     for the piece.
        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :param owner: A player object who is the owner of the piece
        :param board: The board object that created the piece object
        """
        self._name = name
        self._location = location
        self._owner = owner
        self._board = board
        self._palace = [
            "d8", "d9", "d10", "e8", "e9", "e10", "f8", "f9", "f10",
            "d1", "d2", "d3", "e1", "e2", "e3", "f1", "f2", "f3"
        ]
        self._move_path = []

    def __repr__(self):
        """
        Included for printing the game board. Piece objects will be
        represented by the two-letter abbreviation for that piece.

        :return: example: for General, prints GN
        """
        return colored(repr(self._name), self._owner.get_color())

    def get_name(self):
        """
        Returns the name of the piece. The name is a two-letter
        abbreviation that denotes which type of piece it is. Get_name
        is used by player.get_general to determine which piece object
        is their General.

        :return: A string containing the name of the piece
        """
        return self._name

    def get_location(self):
        """
        Returns the location of the piece. The location is given in
        algebraic notation (i.e. 'a1'). Used by other piece objects
        to determine whether they can make a valid move.

        :return: A string containing the algebraic notation representation
                 of the piece object's location
        """
        return self._location

    def set_location(self, location):
        """
        Updates the location of the piece. Location given in algebraic
        notation (i.e. 'a1'). Used by board.move_piece.

        :param location: A string containing the algebraic notation
                        representation of the piece object's location
        :return: None
        """
        self._location = location

    def get_owner(self):
        """
        Returns the player object to which the piece belongs. Used by
        various Board methods to determine if a valid move is being
        made or if a piece has been captured.

        :return: Player object
        """
        return self._owner

    def get_board(self):
        """
        Returns the game board object that the piece belongs to.
        Used by is_legal methods to determine piece ownership
        and location.

        :return: Board object
        """
        return self._board

    def get_image(self):
        """
        Returns the filename for the piece's image.

        :return: string - filename
        """
        return self._image

    def get_image_highlight(self):
        """
        Returns the filename for the piece's highlighted image.

        :return: string - filename
        """
        return self._image_highlight

    def get_palace(self):
        """
        Returns the list of locations that are in either palace.

        :return: list containing locations of palace squares
        """
        return self._palace

    def get_move_path(self):
        """
        Move path holds a list of intermediate squares that a Piece
        will traverse to get to their destination.

        :return: list - self._move_path
        """
        return self._move_path

    def decode_location(self, location):
        """
        Converts algebraic notation to row/column notation.
        Conversion is necessary for accessing the game board--which is
        a list of lists--and is accessed by index, starting at (0, 0)

        Location in algebraic notation is a string containing the
        column and row in order where column is a letter a-i
        and row is a number 1-10. Example: 'b7'

        Location in row/column notation is a tuple (row, column).
        Row is the index of the row sublist of the board and
        column is the index of the element in that sublist that
        represents the column.

        In the above example, 'b7' is converted to (6, 1)

        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :return: (row, column) where row and column are integers
        """
        column_key = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7,
            "i": 8
        }

        row_key = {
            "1": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
            "9": 8,
            "10": 9
        }

        column = column_key[location[0]]

        if len(location) == 3:
            row = row_key[location[1:]]
        else:
            row = row_key[location[1]]

        return row, column

    def encode_location(self, row, column):
        """
        Converts row/column notation to algebraic notation.
        Conversion is necessary for accessing the game board--which is
        a list of lists--and is accessed by index, starting at (0, 0)

        Location in row/column notation is a tuple (row, column).
        Row is the index of the row sublist of the board and
        column is the index of the element in that sublist that
        represents the column. Example: (6, 1)

        Location in algebraic notation is a string containing the
        column and row in order where column is a letter a-i
        and row is a number 1-10.

        In the above example, (6, 1) is converted to 'b7'


        :param row: int - index of the sublist of the game board
                          representing the row
        :param column: int - index of the element of the row sublist
                             of the game board representing the column
        :return: location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        """
        column_key = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
            8: 'i'
        }

        row_key = {
            0: '1',
            1: '2',
            2: '3',
            3: '4',
            4: '5',
            5: '6',
            6: '7',
            7: '8',
            8: '9',
            9: '10'
        }

        column = column_key[column]
        row = row_key[row]
        location = column + row

        return location


class General(Piece):
    """
    Represents a General piece in a Janggi game with a name, location,
    owner, and board. Inherits from the Piece class.
    Additional methods are provided for determining valid moves and for
    generating a list of squares traversed in a move.
    """

    def __init__(self, name, location, owner, board):
        """
        Constructs a General object and initializes variables.

        :param name: A string containing a two-letter abbreviation
                     for the piece.
        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :param owner: A player object who is the owner of the piece
        :param board: The board object that created the piece object
        """
        super().__init__(name, location, owner, board)
        if owner.get_color() == 'blue':
            self._image = 'images/pieces/western/blue/blue_king_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/blue/blue_king_67x67.png'
        else:
            self._image = 'images/pieces/western/red/red_king_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/red/red_king_67x67.png'

    def is_legal(self, source, destination):
        """
        Determines if a move from the source to the destination is
        legal for this piece. Converts the source and destination
        from algebraic notation to row, column notation and performs
        logic appropriate to the movement rules for this piece.
        Interacts with a board object to determine whether there are
        pieces blocking the intended path.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: True if the move is legal
                 False if the move is not legal
        """
        # set up variables for use throughout method
        game_board = self.get_board().get_board()  # save game board
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        destination_square = game_board[to_row][to_col]
        destination_location = self.encode_location(to_row, to_col)
        palace_corners = ['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10']
        palace_centers = ['e2', 'e9']

        # if a friendly piece is blocking the move
        if destination_square is not None:
            if self.get_owner() is destination_square.get_owner():
                return False

        # if the destination is not in the palace
        if destination_location not in self.get_palace():
            return False

        # cannot move more than 1 square
        if (abs(to_row - from_row) > 1) or (abs(to_col - from_col) > 1):
            return False

        # handle diagonal moves
        if (abs(to_row - from_row) == 1) and (abs(to_col - from_col) == 1):
            # move from corners to center
            if source in palace_corners:
                if destination in palace_centers:
                    return True
                else:
                    return False
            # move from center to corners
            elif source in palace_centers:
                if destination in palace_corners:
                    return True
                else:
                    return False
            # no other diagonal moves are allowed
            else:
                return False

        return True

    def move_path(self, source, destination):
        """
        Returns a list of all of the squares traversed while making
        the specified move. The list is generated by implementing a
        move square by square and then appending each square to the
        list. The method is used by Board.is_in_checkmate to determine
        if a defender can intercept an attacker.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: List containing squares on the board (in algebraic
                 notation) that the piece will traverse during move.
                 Returns an empty list if there are no intermediate
                 squares on the move.
        """
        return self.get_move_path()  # General has no intermediate moves


class Guard(Piece):
    """
    Represents a Guard piece in a Janggi game with a name, location,
    owner, and board. Inherits from the Piece class.
    Additional methods are provided for determining valid moves and for
    generating a list of squares traversed in a move.
    """

    def __init__(self, name, location, owner, board):
        """
        Constructs a Guard object and initializes variables.

        :param name: A string containing a two-letter abbreviation
                     for the piece.
        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :param owner: A player object who is the owner of the piece
        :param board: The board object that created the piece object
        """
        super().__init__(name, location, owner, board)
        if owner.get_color() == 'blue':
            self._image = 'images/pieces/western/blue/blue_advisor_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/blue/blue_advisor_67x67.png'
        else:
            self._image = 'images/pieces/western/red/red_advisor_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/red/red_advisor_67x67.png'

    def is_legal(self, source, destination):
        """
        Determines if a move from the source to the destination is
        legal for this piece. Converts the source and destination
        from algebraic notation to row, column notation and performs
        logic appropriate to the movement rules for this piece.
        Interacts with a board object to determine whether there are
        pieces blocking the intended path.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: True if the move is legal
                 False if the move is not legal
        """
        # set up variables for use throughout method
        game_board = self.get_board().get_board()  # save game board
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        destination_piece = game_board[to_row][to_col]
        palace_corners = ['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10']
        palace_centers = ['e2', 'e9']

        # if a friendly piece is blocking the move
        if destination_piece is not None:
            if self.get_owner() is destination_piece.get_owner():
                return False

        # if the destination is not in the palace
        if destination not in self.get_palace():
            return False

        # cannot move more than 1 square
        if (abs(to_row - from_row) > 1) or (abs(to_col - from_col) > 1):
            return False

        # handle diagonal moves
        if (abs(to_row - from_row) == 1) and (abs(to_col - from_col) == 1):
            # move from corners to center
            if source in palace_corners:
                if destination in palace_centers:
                    return True
                else:
                    return False
            # move from center to corners
            elif source in palace_centers:
                if destination in palace_corners:
                    return True
                else:
                    return False
            # no other diagonal moves are allowed
            else:
                return False

        return True

    def move_path(self, source, destination):
        """
        Returns a list of all of the squares traversed while making
        the specified move. The list is generated by implementing a
        move square by square and then appending each square to the
        list. The method is used by Board.is_in_checkmate to determine
        if a defender can intercept an attacker.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: List containing squares on the board (in algebraic
                 notation) that the piece will traverse during move.
                 Returns an empty list if there are no intermediate
                 squares on the move.
        """
        return self.get_move_path()  # Guard has no intermediate moves


class Elephant(Piece):
    """
    Represents an Elephant piece in a Janggi game with a name, location,
    owner, and board. Inherits from the Piece class.
    Additional methods are provided for determining valid moves and for
    generating a list of squares traversed in a move.
    """

    def __init__(self, name, location, owner, board):
        """
        Constructs an Elephant object and initializes variables.

        :param name: A string containing a two-letter abbreviation
                     for the piece.
        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :param owner: A player object who is the owner of the piece
        :param board: The board object that created the piece object
        """
        super().__init__(name, location, owner, board)
        if owner.get_color() == 'blue':
            self._image = 'images/pieces/western/blue/blue_elephant_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/blue/blue_elephant_67x67.png'
        else:
            self._image = 'images/pieces/western/red/red_elephant_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/red/red_elephant_67x67.png'

    def is_legal(self, source, destination):
        """
        Determines if a move from the source to the destination is
        legal for this piece. Converts the source and destination
        from algebraic notation to row, column notation and performs
        logic appropriate to the movement rules for this piece.
        Interacts with a board object to determine whether there are
        pieces blocking the intended path.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: True if the move is legal
                 False if the move is not legal
        """
        # set up variables for use throughout method
        game_board = self.get_board().get_board()  # save game board
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        destination_piece = game_board[to_row][to_col]

        # if a friendly piece is on the destination
        if destination_piece is not None:
            if self.get_owner() is destination_piece.get_owner():
                return False

        # handle relational movement logic
        if (abs(to_row - from_row) == 3) and (abs(to_col - from_col) == 2):
            for square in self.move_path(source, destination):
                if self.get_board().get_occupant(square) is not None:
                    return False
            return True

        elif (abs(to_row - from_row) == 2) and (abs(to_col - from_col) == 3):
            for square in self.move_path(source, destination):
                if self.get_board().get_occupant(square) is not None:
                    return False
            return True

        else:  # move is not physically allowed
            return False

    def move_path(self, source, destination):
        """
        Returns a list of all of the squares traversed while making
        the specified move. The list is generated by implementing a
        move square by square and then appending each square to the
        list. The method is used by Board.is_in_checkmate to determine
        if a defender can intercept an attacker.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: List containing squares on the board (in algebraic
                 notation) that the piece will traverse during move.
                 Returns an empty list if there are no intermediate
                 squares on the move.
        """
        # set up variables for use throughout method
        move_path = []
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)

        # Elephants have 8 possible moves and travel through
        # 2 different squares to get to those each of those 8 moves.
        # They move either a) three rows and two columns, or
        # b) three columns and two rows.

        # if an Elephant moves up three rows, they travel through
        # the square one up from the start and one diagonal square
        if (to_row - from_row) == -3:
            # add the orthogonal square
            square = self.encode_location(from_row - 1, from_col)
            move_path.append(square)

            # add the diagonal square
            if (to_col - from_col) == 2:
                square = self.encode_location(from_row - 2, from_col + 1)
                move_path.append(square)
            else:
                square = self.encode_location(from_row - 2, from_col - 1)
                move_path.append(square)

        # if an Elephant moves down three rows, they travel through
        # the square one down from the start and one diagonal square
        if (to_row - from_row) == 3:
            # add the orthogonal square
            square = self.encode_location(from_row + 1, from_col)
            move_path.append(square)

            # add the diagonal square
            if (to_col - from_col) == 2:
                square = self.encode_location(from_row + 2, from_col + 1)
                move_path.append(square)
            else:
                square = self.encode_location(from_row + 2, from_col - 1)
                move_path.append(square)

        # if an Elephant moves right three columns, they travel through
        # the square one right from the start and one diagonal square
        if (to_col - from_col) == 3:
            # add the orthogonal square
            square = self.encode_location(from_row, from_col + 1)
            move_path.append(square)

            # add the diagonal square
            if (to_row - from_row) == 2:
                square = self.encode_location(from_row + 1, from_col + 2)
                move_path.append(square)
            else:
                square = self.encode_location(from_row - 1, from_col + 2)
                move_path.append(square)

        # if an Elephant moves left three columns, they travel through
        # the square one left from the start and one diagonal square
        if (to_col - from_col) == -3:
            # add the orthogonal square
            square = self.encode_location(from_row, from_col - 1)
            move_path.append(square)

            # add the diagonal square
            if (to_row - from_row) == 2:
                square = self.encode_location(from_row + 1, from_col - 2)
                move_path.append(square)
            else:
                square = self.encode_location(from_row - 1, from_col - 2)
                move_path.append(square)

        return move_path


class Horse(Piece):
    """
    Represents a Horse piece in a Janggi game with a name, location,
    owner, and board. Inherits from the Piece class.
    Additional methods are provided for determining valid moves and for
    generating a list of squares traversed in a move.
    """

    def __init__(self, name, location, owner, board):
        """
        Constructs a Horse object and initializes variables.

        :param name: A string containing a two-letter abbreviation
                     for the piece.
        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :param owner: A player object who is the owner of the piece
        :param board: The board object that created the piece object
        """
        super().__init__(name, location, owner, board)
        if owner.get_color() == 'blue':
            self._image = 'images/pieces/western/blue/blue_horse_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/blue/blue_horse_67x67.png'
        else:
            self._image = 'images/pieces/western/red/red_horse_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/red/red_horse_67x67.png'

    def is_legal(self, source, destination):
        """
        Determines if a move from the source to the destination is
        legal for this piece. Converts the source and destination
        from algebraic notation to row, column notation and performs
        logic appropriate to the movement rules for this piece.
        Interacts with a board object to determine whether there are
        pieces blocking the intended path.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: True if the move is legal
                 False if the move is not legal
        """
        # set up variables for use throughout method
        game_board = self.get_board().get_board()  # save game board
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        destination_piece = game_board[to_row][to_col]

        # if a friendly piece is on the destination
        if destination_piece is not None:
            if self.get_owner() is destination_piece.get_owner():
                return False

        # handle relational movement logic
        if (abs(to_row - from_row) == 2) and (abs(to_col - from_col) == 1):
            for square in self.move_path(source, destination):
                if self.get_board().get_occupant(square) is not None:
                    return False
            return True

        elif (abs(to_row - from_row) == 1) and (abs(to_col - from_col) == 2):
            for square in self.move_path(source, destination):
                if self.get_board().get_occupant(square) is not None:
                    return False
            return True

        else:  # move is not physically allowed
            return False


    def move_path(self, source, destination):
        """
        Returns a list of all of the squares traversed while making
        the specified move. The list is generated by implementing a
        move square by square and then appending each square to the
        list. The method is used by Board.is_in_checkmate to determine
        if a defender can intercept an attacker.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: List containing squares on the board (in algebraic
                 notation) that the piece will traverse during move.
                 Returns an empty list if there are no intermediate
                 squares on the move.
        """
        # set up variables for use throughout method
        move_path = []
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)

        # Horses have 8 possible moves, but travel through
        # only 4 different squares to get to those 8 moves.
        # They move either a) two rows and one column,
        # or b) two columns and one row.

        # if a Horse moves up two rows, they travel through
        # the square one up from the start
        if (to_row - from_row) == -2:
            square = self.encode_location(from_row - 1, from_col)
            move_path.append(square)

        # if a Horse moves down two rows, they travel through
        # the square one down from the start
        if (to_row - from_row) == 2:
            square = self.encode_location(from_row + 1, from_col)
            move_path.append(square)

        # if a Horse moves right two columns, they travel through
        # the square one right from the start
        if (to_col - from_col) == 2:
            square = self.encode_location(from_row, from_col + 1)
            move_path.append(square)

        # if a Horse moves left two columns, they travel through
        # the square one left from the start
        if (to_col - from_col) == -2:
            square = self.encode_location(from_row, from_col - 1)
            move_path.append(square)

        return move_path


class Chariot(Piece):
    """
    Represents a Chariot piece in a Janggi game with a name, location,
    owner, and board. Inherits from the Piece class.
    Additional methods are provided for determining valid moves and for
    generating a list of squares traversed in a move.
    """

    def __init__(self, name, location, owner, board):
        """
        Constructs a Chariot object and initializes variables.

        :param name: A string containing a two-letter abbreviation
                     for the piece.
        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :param owner: A player object who is the owner of the piece
        :param board: The board object that created the piece object
        """
        super().__init__(name, location, owner, board)
        if owner.get_color() == 'blue':
            self._image = 'images/pieces/western/blue/blue_chariot_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/blue/blue_chariot_67x67.png'
        else:
            self._image = 'images/pieces/western/red/red_chariot_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/red/red_chariot_67x67.png'

    def is_legal(self, source, destination):
        """
        Determines if a move from the source to the destination is
        legal for this piece. Converts the source and destination
        from algebraic notation to row, column notation and performs
        logic appropriate to the movement rules for this piece.
        Interacts with a board object to determine whether there are
        pieces blocking the intended path.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: True if the move is legal
                 False if the move is not legal
        """
        # set up variables for use throughout method
        game_board = self.get_board().get_board()  # save game board
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        destination_piece = game_board[to_row][to_col]
        palace_corners = ['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10']
        blue_palace_corners = ['d8', 'f8', 'd10', 'f10']
        red_palace_corners = ['d1', 'f1', 'd3', 'f3']
        red_palace_center = 'e2'
        blue_palace_center = 'e9'

        # if a friendly piece is on the destination
        if destination_piece is not None:
            if self.get_owner() is destination_piece.get_owner():
                return False

        # if there is any piece blocking the move path
        for square in self.move_path(source, destination):
            if self.get_board().get_occupant(square) is not None:
                return False

        # diagonal moves within the palace are allowed.
        # otherwise, diagonal moves are not allowed
        if (from_row != to_row) and (from_col != to_col):  # if diagonal

            # handle palace moves
            if source in palace_corners:
                if (source in blue_palace_corners
                        and destination in blue_palace_corners):
                    return True
                elif (source in blue_palace_corners
                        and destination == blue_palace_center):
                    return True
                elif (source in red_palace_corners
                        and destination in red_palace_corners):
                    return True
                elif (source in red_palace_corners
                        and destination == red_palace_center):
                    return True
                else:
                    return False

            elif source == blue_palace_center:
                if destination in blue_palace_corners:
                    return True
                else:
                    return False

            elif source == red_palace_center:
                if destination in red_palace_corners:
                    return True
                else:
                    return False

            # if the move diagonal but not in the palace
            else:
                return False

        # if none of the above conditions return False,
        # then the move is legal
        return True

    def move_path(self, source, destination):
        """
        Returns a list of all of the squares traversed while making
        the specified move. The list is generated by implementing a
        move square by square and then appending each square to the
        list. The method is used by Board.is_in_checkmate to determine
        if a defender can intercept an attacker.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: List containing squares on the board (in algebraic
                 notation) that the piece will traverse during move.
                 Returns an empty list if there are no intermediate
                 squares on the move.
        """
        # set up variables for use throughout method
        move_path = []
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        palace_corners = ['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10']
        blue_palace_corners = ['d8', 'f8', 'd10', 'f10']
        palace_centers = ['e2', 'e9']

        # if move is from palace corner to corner,
        # then the only intermediate square is the palace center
        if (source in palace_corners) and (destination in palace_corners):
            if abs(to_row - from_row) == abs(to_col - from_col):
                if source in blue_palace_corners:
                    move_path.append('e9')
                else:
                    move_path.append('e2')
                return move_path

        # if move is from palace corner to palace center or center to corner,
        # then there is no intermediate square
        if ((source in palace_corners and destination in palace_centers)
              or (destination in palace_corners and source in palace_centers)):

            return move_path

        # if move is orthogonal:

        # horizontal move
        if from_row == to_row:
            # add each intermediate square to the move list
            if to_col > from_col:
                for column in range(from_col + 1, to_col):
                    square = self.encode_location(from_row, column)
                    move_path.append(square)
            else:
                for column in range(from_col - 1, to_col, -1):
                    square = self.encode_location(from_row, column)
                    move_path.append(square)

        # vertical move
        if from_col == to_col:
            # add each intermediate square to the move list
            if to_row > from_row:
                for row in range(from_row + 1, to_row):
                    square = self.encode_location(row, from_col)
                    move_path.append(square)
            else:
                for row in range(from_row - 1, to_row, -1):
                    square = self.encode_location(row, from_col)
                    move_path.append(square)

        return move_path


class Cannon(Piece):
    """
    Represents a Cannon piece in a Janggi game with a name, location,
    owner, and board. Inherits from the Piece class.
    Additional methods are provided for determining valid moves and for
    generating a list of squares traversed in a move.
    """

    def __init__(self, name, location, owner, board):
        """
        Constructs a Cannon object and initializes variables.

        :param name: A string containing a two-letter abbreviation
                     for the piece.
        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :param owner: A player object who is the owner of the piece
        :param board: The board object that created the piece object
        """
        super().__init__(name, location, owner, board)
        if owner.get_color() == 'blue':
            self._image = 'images/pieces/western/blue/blue_cannon_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/blue/blue_cannon_67x67.png'
        else:
            self._image = 'images/pieces/western/red/red_cannon_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/red/red_cannon_67x67.png'

    def is_legal(self, source, destination):
        """
        Determines if a move from the source to the destination is
        legal for this piece. Converts the source and destination
        from algebraic notation to row, column notation and performs
        logic appropriate to the movement rules for this piece.
        Interacts with a board object to determine whether there are
        pieces blocking the intended path.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: True if the move is legal
                 False if the move is not legal
        """
        # set up variables for use throughout method
        game_board = self.get_board().get_board()  # save game board
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        destination_piece = game_board[to_row][to_col]
        palace_corners = ['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10']
        blue_palace_corners = ['d8', 'f8', 'd10', 'f10']
        red_palace_corners = ['d1', 'f1', 'd3', 'f3']
        red_palace_center = 'e2'
        blue_palace_center = 'e9'

        # if a friendly piece is on the destination
        if destination_piece is not None:
            if self.get_owner() is destination_piece.get_owner():
                return False

            # if a cannon is on the destination
            if destination_piece.get_name() == 'CA':
                return False

        # evaluate the intended move path for pieces to jump over
        jumps = 0
        cannon_in_path = False

        for square in self.move_path(source, destination):
            # if there is a piece
            if self.get_board().get_occupant(square) is not None:
                jumps += 1
                # if the piece is a cannon
                if self.get_board().get_occupant(square).get_name() == "CA":
                    cannon_in_path = True

        # if there are 0 or more than 1 pieces to jump
        if jumps == 0 or jumps > 1:
            return False

        # if there is a cannon on the path
        if cannon_in_path:
            return False

        # diagonal moves within the palace are allowed.
        # otherwise, diagonal moves are not allowed
        if (from_row != to_row) and (from_col != to_col):  # if diagonal

            # handle palace moves
            if source in palace_corners:
                if (source in blue_palace_corners
                        and destination in blue_palace_corners):
                    return True
                elif (source in blue_palace_corners
                        and destination == blue_palace_center):
                    return True
                elif (source in red_palace_corners
                        and destination in red_palace_corners):
                    return True
                elif (source in red_palace_corners
                        and destination == red_palace_center):
                    return True
                else:
                    return False

            elif source == blue_palace_center:
                if destination in blue_palace_corners:
                    return True
                else:
                    return False

            elif source == red_palace_center:
                if destination in red_palace_corners:
                    return True
                else:
                    return False

            # if the move diagonal but not in the palace
            else:
                return False

        # if none of the above conditions return False,
        # then the move is legal
        return True

    def move_path(self, source, destination):
        """
        Returns a list of all of the squares traversed while making
        the specified move. The list is generated by implementing a
        move square by square and then appending each square to the
        list. The method is used by Board.is_in_checkmate to determine
        if a defender can intercept an attacker.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: List containing squares on the board (in algebraic
                 notation) that the piece will traverse during move.
                 Returns an empty list if there are no intermediate
                 squares on the move.
        """
        # set up variables for use throughout method
        move_path = []
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        palace_corners = ['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10']
        blue_palace_corners = ['d8', 'f8', 'd10', 'f10']
        palace_centers = ['e2', 'e9']

        # if move is from palace corner to corner,
        # then the only intermediate square is the palace center
        if (source in palace_corners) and (destination in palace_corners):
            if abs(to_row - from_row) == abs(to_col - from_col):
                if source in blue_palace_corners:
                    move_path.append('e9')
                else:
                    move_path.append('e2')
                return move_path

        # if move is from palace corner to palace center or center to corner,
        # then there is no intermediate square
        if ((source in palace_corners and destination in palace_centers)
              or (destination in palace_corners and source in palace_centers)):

            return move_path

        # if move is orthogonal:

        # horizontal move
        if from_row == to_row:
            # add each intermediate square to the move list
            if to_col > from_col:
                for column in range(from_col + 1, to_col):
                    square = self.encode_location(from_row, column)
                    move_path.append(square)
            else:
                for column in range(from_col - 1, to_col, -1):
                    square = self.encode_location(from_row, column)
                    move_path.append(square)

        # vertical move
        if from_col == to_col:
            # add each intermediate square to the move list
            if to_row > from_row:
                for row in range(from_row + 1, to_row):
                    square = self.encode_location(row, from_col)
                    move_path.append(square)
            else:
                for row in range(from_row - 1, to_row, -1):
                    square = self.encode_location(row, from_col)
                    move_path.append(square)

        return move_path


class Soldier(Piece):
    """
    Represents a Soldier piece in a Janggi game with a name, location,
    owner, and board. Inherits from the Piece class.
    Additional methods are provided for determining valid moves and for
    generating a list of squares traversed in a move.
    """

    def __init__(self, name, location, owner, board):
        """
        Constructs a Soldier object and initializes variables.

        :param name: A string containing a two-letter abbreviation
                     for the piece.
        :param location: A string containing the algebraic notation for
                         the square that the piece currently occupies
        :param owner: A player object who is the owner of the piece
        :param board: The board object that created the piece object
        """
        super().__init__(name, location, owner, board)
        if owner.get_color() == 'blue':
            self._image = 'images/pieces/western/blue/blue_pawn_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/blue/blue_pawn_67x67.png'
        else:
            self._image = 'images/pieces/western/red/red_pawn_wooden_67x67.png'
            self._image_highlight = 'images/pieces/western/red/red_pawn_67x67.png'

    def is_legal(self, source, destination):
        """
        Determines if a move from the source to the destination is
        legal for this piece. Converts the source and destination
        from algebraic notation to row, column notation and performs
        logic appropriate to the movement rules for this piece.
        Interacts with a board object to determine whether there are
        pieces blocking the intended path.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: True if the move is legal
                 False if the move is not legal
        """
        # set up variables for use throughout method
        game_board = self.get_board().get_board()  # save game board
        from_row, from_col = self.decode_location(source)
        to_row, to_col = self.decode_location(destination)
        destination_piece = game_board[to_row][to_col]

        # if a friendly piece is blocking the move
        if destination_piece is not None:
            if self.get_owner() is destination_piece.get_owner():
                return False

        # can only move left or right 1 square
        if from_row == to_row:
            if abs(to_col - from_col) != 1:
                return False

        # can only move forward 1 square
        if from_col == to_col:
            if self.get_owner().get_color() == 'blue':
                if (to_row - from_row) != -1:
                    return False
            else:
                if (to_row - from_row) != 1:
                    return False

        # diagonal moves within the palace are allowed.
        # otherwise, diagonal moves are not allowed
        if (from_row != to_row) and (from_col != to_col):
            if source == 'd3' or source == 'f3':
                if destination == 'e2':
                    return True
                else:
                    return False
            elif source == 'e2':
                if destination == 'd1' or destination == 'f1':
                    return True
                else:
                    return False
            elif source == 'd8' or source == 'f8':
                if destination == 'e9':
                    return True
                else:
                    return False
            elif source == 'e9':
                if destination == 'd10' or destination == 'f10':
                    return True
                else:
                    return False
            else:
                return False

        return True

    def move_path(self, source, destination):
        """
        Returns a list of all of the squares traversed while making
        the specified move. The list is generated by implementing a
        move square by square and then appending each square to the
        list. The method is used by Board.is_in_checkmate to determine
        if a defender can intercept an attacker.

        :param source: string - algebraic notation for a location
                                on the board
        :param destination: string - algebraic notation for a location
                                     on the board
        :return: List containing squares on the board (in algebraic
                 notation) that the piece will traverse during move.
                 Returns an empty list if there are no intermediate
                 squares on the move.
        """
        return self.get_move_path()  # Soldier has no intermediate moves


def main():
    game = JanggiGame()
    game.make_move('e7', 'e6')  # blue player moves
    game.make_move('e4', 'e5')  # red player moves

    game.print_board()
    print("Game state:    ", game.get_game_state())
    print("Current player:", game.get_current_player())


if __name__ == '__main__':
    main()