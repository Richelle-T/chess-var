# Author: Richelle Thompson
# GitHub username: Richelle-T
# Date: 12/10/2023
# Description: A variation of chess, where the goal is to capture all pieces of one type. Like standard chess,
#              pieces are either white or black; white always moves first. Each player has 1 king, 1 queen, 2 rooks,
#              2 bishops, 2 knights, and 8 pawns. These pieces must move and capture the same as in standard chess,
#              there is no castling, en passant, or pawn promotion. The king isn't a special piece in this game,
#              there is no check or checkmate. The winner is the first player to capture all of an opponent's pieces
#              of one type, for example capturing all 8 pawns, or capturing 2 knights, or capturing 1 king.

class ChessVar:
    """
    Represents an instance of the modified chess game, where a player must capture all of an opponent's pieces
        of one type. Has methods for creating an instance of the class, setting the turn, getting and setting the game
        state, making a move from one square to another, and converting algebraic notation to indices of a 2D list.
    Communicates with the ChessBoard class. ChessVar uses an object of the ChessBoard class in the constructor
        to create the game board.
    """
    
    def __init__(self):
        """
        Creates a ChessVar object with a board, turn, and game state.
            game_board is an object of the ChessBoard class.
            player_turn is a string initialized to 'WHITE', since white always moves first.
            game_state is a string initialized to 'UNFINISHED' since there can't be a winner before the game starts.
        :param: none
        :return: none
        """
        self._game_board = ChessBoard()
        self._player_turn = 'WHITE'
        self._game_state = 'UNFINISHED'
    
    def set_player_turn(self):
        """
        Switches the turn between 'BLACK' and 'WHITE'.
        :param: none
        :return: none
        """
        if self._player_turn == 'WHITE':
            self._player_turn = 'BLACK'
        else:
            self._player_turn = 'WHITE'
    
    def get_game_state(self):
        """
        Returns the state of the game. The state will be 'UNFINISHED' if there hasn't been a winner, otherwise
            the state will be 'WHITE_WON' or 'BLACK_WON' depending on the winner.
        :param: none
        :return:
            'UNFINISHED': if there hasn't been a winner
            'WHITE_WON': if white color player captured all black pieces of one type
            'BLACK_WON': if black color player captured all white pieces of one type
        """
        return self._game_state
    
    def set_game_state(self):
        """
        Checks the pieces_on_board dictionary in the ChessBoard object for any values that are 0.
            If any value is 0, the other color's player has captured all pieces of a type; set game state to
            a string declaring the winner.
        :param: none
        :return: none
        """
        # Check if white's dictionary has any 0 values:
        white_pieces = self._game_board.get_current_pieces_on_board()['WHITE'].values()
        if 0 in white_pieces:
            self._game_state = 'BLACK_WON'
        
        # Check if black's dictionary has any 0 values:
        black_pieces = self._game_board.get_current_pieces_on_board()['BLACK'].values()
        if 0 in black_pieces:
            self._game_state = 'WHITE_WON'
    
    def is_valid_input(self, from_square, to_square):
        """
        Checks if the algebraic notation inputs for from_square and to_square are valid. Only the letters
            A through H and numbers 1 through 8 are valid.
        :param from_square: string that represents square being moved from, in algebraic notation
        :param to_square: string that represents square being moved to, in algebraic notation
        :return: True if input is valid, otherwise False
        """
        valid_letters = ("A", "B", "C", "D", "E", "F", "G", "H")
        valid_numbers = ("1", "2", "3", "4", "5", "6", "7", "8")
        
        if from_square == to_square:
            print("\nThis is the same square your piece is on! Try again.")
            return False
        
        # check if the from_square is valid
        if (len(from_square) != 2
                or from_square[0].upper() not in valid_letters
                or from_square[1] not in valid_numbers):
            print("\nInvalid input for the square moved from. Try again.")
            return False
        
        # check if the to_square is valid
        if (len(to_square) != 2
                or to_square[0].upper() not in valid_letters
                or to_square[1] not in valid_numbers):
            print("\nInvalid input for the square moved to. Try again.")
            return False
        
        return True
    
    def algebraic_to_indices(self, square):
        """
        Description: Converts algebraic notation to a tuple containing indices for the row and column of the board.
            The board is oriented the same way as the diagram in the README.md file. A8 corresponds to (0,0)
            and H1 corresponds to (7,7). Returns the tuple of indices.
        :param square: string that represents a square (location on the board) in algebraic notation
        :return:
            row_index, col_index: a tuple containing the indices of the row and column corresponding to the
            parameter's location on the board
        """
        letter_to_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        number_to_index = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        
        col_index = letter_to_index[square[0].upper()]
        row_index = number_to_index[square[1]]
        return row_index, col_index
    
    def display_board_and_game_status(self):
        """
        Description: Displays the board and the player's turn. If there's a winner,
            displays the winner instead of the turn.
        :param: none
        :return: none
        """
        self._game_board.display_board()
        if self._game_state == 'UNFINISHED':
            if self._player_turn == 'WHITE':
                print("WHITE'S TURN")
            else:
                print("BLACK'S TURN")
        else:
            if self._game_state == 'WHITE_WON':
                print("WHITE WON!")
            else:
                print("BLACK WON!")
    
    def make_move(self, from_square, to_square):
        """
        Description: Checks if a move from the from_square to the to_square is valid.
            For a move to be valid, the following conditions must be true:
            1. The game must not already have a winner
            2. Inputs for both squares must be in valid algebraic notation
            3. The move must be legal for the particular piece being moved
            If any of these conditions are not true, returns False. Otherwise, makes the indicated move from
            from_square to to_square, removes any captured piece, updates the game state, updates the player turn,
            displays the board and game status, and returns True.
        :param from_square: string that represents the square being moved from, in algebraic notation
        :param to_square: string that represents the square being moved to, in algebraic notation
        :return:
            True: if move is valid
            False: if move is not valid
        """
        # check if game has already been won
        if self._game_state != 'UNFINISHED':
            print("\nYou can't make any more moves, there's already a winner.")
            return False
        
        # check if inputs for both squares are valid
        if not self.is_valid_input(from_square, to_square):
            return False
        
        # convert algebraic notation to indices
        from_row, from_col = self.algebraic_to_indices(from_square)
        to_row, to_col = self.algebraic_to_indices(to_square)
        
        # check if the move is legal
        piece_to_move = self._game_board.get_piece_at(from_row, from_col)
        if piece_to_move is None:
            print("\nThere's no piece to move here! Try again.")
            return False
        elif not piece_to_move.is_valid_move(self._game_board, self._player_turn, from_row, from_col, to_row, to_col):
            return False
        else:  # move piece and update game data
            self._game_board.move_piece(from_row, from_col, to_row, to_col)
            self.set_game_state()
            self.set_player_turn()
            self.display_board_and_game_status()
            return True


class ChessBoard:
    """
    Represents a chess board. Has methods for creating an instance of the class, getting the board, getting the
        dictionary of pieces on the board, removing a piece from the board, and displaying the board.
    Communicates with the Piece class and all its child classes (King, Queen, Rook, Bishop, Knight, Pawn). ChessBoard
        uses objects of each child class in the constructor to create the game board.
    """
    
    def __init__(self):
        """
        Description: Creates a ChessBoard object with a board (2D list), and a dictionary called pieces_on_board.
            The board is set up the way a standard chess board would be, with black pieces at the top of the board, and
            white pieces at the bottom. The dictionary has two keys, 'WHITE' and 'BLACK', and the corresponding values
            are another dictionary that contains the number of pieces on the board for each type.
        :param: none
        :return: none
        """
        self._board = [
            [Rook("BLACK"), Knight("BLACK"), Bishop("BLACK"), Queen("BLACK"),
                King("BLACK"), Bishop("BLACK"), Knight("BLACK"), Rook("BLACK")],
            [Pawn("BLACK"), Pawn("BLACK"), Pawn("BLACK"), Pawn("BLACK"),
                Pawn("BLACK"), Pawn("BLACK"), Pawn("BLACK"), Pawn("BLACK")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn("WHITE"), Pawn("WHITE"), Pawn("WHITE"), Pawn("WHITE"),
                Pawn("WHITE"), Pawn("WHITE"), Pawn("WHITE"), Pawn("WHITE")],
            [Rook("WHITE"), Knight("WHITE"), Bishop("WHITE"), Queen("WHITE"),
                King("WHITE"), Bishop("WHITE"), Knight("WHITE"), Rook("WHITE")]
        ]
        self._current_pieces_on_board = {
            "WHITE": {
                "King": 1,
                "Queen": 1,
                "Rook": 2,
                "Bishop": 2,
                "Knight": 2,
                "Pawn": 8
            },
            "BLACK": {
                "King": 1,
                "Queen": 1,
                "Rook": 2,
                "Bishop": 2,
                "Knight": 2,
                "Pawn": 8
            }
        }
    
    def get_board(self):
        """
        Description: Returns a 2D list representing the board with pieces.
        :param: none
        :return:
            self._board: a nested list
        """
        return self._board
    
    def get_current_pieces_on_board(self):
        """
        Description: Returns a dictionary that holds the current pieces on the board for each color.
        :param: none
        :return:
            self._current_pieces_on_board: a nested dictionary
        """
        return self._current_pieces_on_board
    
    def get_piece_at(self, row, col):
        """
        Description: Returns the object at the row and column in the 2D list.
        :param row: row index of the list
        :param col: col index of the list
        :return:
            object at the location of row, col
            None if there is no object
        """
        return self._board[row][col]
    
    def display_board(self):
        """
        Description: Displays the chess board, with letters labeling the columns and numbers labeling the rows on
            each edge of the board. Each piece is represented by a unicode character corresponding to color and piece
            type.
        :param: none
        :return: none
        """
        print()
        row_number = 8
        letters = " abcdefgh"
        print(*letters, sep="\t")
        for row in range(8):
            print(row_number, end="\t")
            for col in range(8):
                if self._board[row][col] is None:
                    print(" ", end="\t")
                else:
                    print(self._board[row][col], end="\t")
            print(row_number, end="\t")
            row_number -= 1
            print()  # create a new line
        print(*letters, sep="\t")
    
    def remove_piece_from_board(self, color, piece_name):
        """
        Description: Decrements the value held at the keys matching the color and piece_name in the dictionary of pieces.
        :param: none
        :return: none
        """
        self._current_pieces_on_board[color][piece_name] -= 1
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """
        Description: Moves a piece from the from_square to the to_square. If there's a piece on the to_square,
            capture. Update the location of the moved piece.
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return: none
        """
        # if to_square has other color's piece, capture it
        piece_at_to_square = self._board[to_row][to_col]
        if piece_at_to_square is not None:
            self.remove_piece_from_board(piece_at_to_square.get_color(), piece_at_to_square.__class__.__name__)
        
        # move piece from from_square to to_square
        self._board[to_row][to_col] = self._board[from_row][from_col]
        self._board[from_row][from_col] = None


class Piece:
    """
    Represents a chess piece. Has methods for creating an instance of the class, and getting the color of the piece.
    Communicates with all its child classes (King, Queen, Rook, Bishop, Knight, Pawn) since these child
        classes inherit the constructor and get_color methods.
    """
    
    def __init__(self, color):
        """
        Description: Creates a Piece object. The color will be set to either white or black.
        :param color: a string that is either 'WHITE' or 'BLACK'
        :return: none
        """
        self._color = color
    
    def get_color(self):
        """
        Description: Returns the color of the piece
        :param: none
        :return:
            'WHITE': if the piece is white
            'BLACK': if the piece is black
        """
        return self._color
    
    def is_valid_move(self, board_object, turn, from_row, from_col, to_row, to_col):
        """
        Description: Checks if from_square and to_square have the right piece colors for a move to be valid.
            The from_square must contain a piece belonging to the current turn's player. The to_square must either
            be empty, or contain a piece belonging to the opponent.
        :param board_object: ChessBoard object
        :param turn: current player's piece color
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return:
            True: if the move is valid
            False: if the move is not valid
        """
        # check if from_square contains a piece belonging to current turn's player
        if self.get_color() != turn:
            print("\nYou can't move the other player's piece! Try again.")
            return False
        
        # check if to_square contains a piece belonging to current turn's player
        piece_at_to_square = board_object.get_piece_at(to_row, to_col)
        if piece_at_to_square is not None and piece_at_to_square.get_color() == turn:
            print("\nYou can't capture your own piece! Try again.")
            return False
        
        return True
    
    def check_horizontal_path(self, board_object, from_row, from_col, to_col):
        """
        Description: If from_square and to_square are in the same row, checks if there's any pieces
            between them.
        :param board_object: ChessBoard object
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_col: column index of the to_square
        :return:
            True: if there's no pieces between the two squares
            False: if there's a piece between the two squares
        Return value:
        """
        # from_square is to the left of to_square
        if from_col < to_col:
            while (from_col + 1) != to_col:
                if board_object.get_piece_at(from_row, (from_col + 1)) is None:
                    from_col += 1
                else:
                    print("\nYou can't jump over any pieces. Try again.")
                    return False
        
        # from_square is to the right of to_square
        elif from_col > to_col:
            while (from_col - 1) != to_col:
                if board_object.get_piece_at(from_row, (from_col - 1)) is None:
                    from_col -= 1
                else:
                    print("\nYou can't jump over any pieces. Try again.")
                    return False
        
        return True
    
    def check_vertical_path(self, board_object, from_row, from_col, to_row):
        """
        Description: If from_square and to_square are in the same row, checks if there's any pieces
            between them.
        :param board_object: ChessBoard object
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :return:
            True: if there's no pieces between the two squares
            False: if there's a piece between the two squares
        """
        # from_square is above to_square
        if from_row < to_row:
            while (from_row + 1) != to_row:
                if board_object.get_piece_at((from_row + 1), from_col) is None:
                    from_row += 1
                else:
                    print("\nYou can't jump over any pieces. Try again.")
                    return False
                
        # from_square is below to_square
        elif from_row > to_row:
            while (from_row - 1) != to_row:
                if board_object.get_piece_at((from_row - 1), from_col) is None:
                    from_row -= 1
                else:
                    print("\nYou can't jump over any pieces. Try again.")
                    return False
        
        return True
    
    def check_diagonal_path(self, board_object, from_row, from_col, to_row, to_col):
        """
        Description: If from_square and to_square are in the same diagonal, checks if there's any pieces
            between them.
        :param board_object: ChessBoard object
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return:
            True: if there's no pieces between the two squares
            False: if there's a piece between the two squares
        """
        # from_square is diagonally below and left of to_square
        if from_row > to_row and from_col < to_col:
            while (from_col + 1) != to_col:
                if board_object.get_piece_at((from_row - 1), from_col + 1) is None:
                    from_row -= 1
                    from_col += 1
                else:
                    print("\nYou can't jump over any pieces. Try again.")
                    return False
         
        # from_square is diagonally above and left of to_square
        elif from_row < to_row and from_col < to_col:
            while (from_col + 1) != to_col:
                if board_object.get_piece_at((from_row + 1), (from_col + 1)) is None:
                    from_row += 1
                    from_col += 1
                else:
                    print("\nYou can't jump over any pieces. Try again.")
                    return False
        
        # from_square is diagonally above and right of to_square
        elif from_row < to_row and from_col > to_col:
            while (from_col - 1) != to_col:
                if board_object.get_piece_at((from_row + 1), (from_col - 1)) is None:
                    from_row += 1
                    from_col -= 1
                else:
                    print("\nYou can't jump over any pieces. Try again.")
                    return False
        
        # from_square is diagonally below and right of to_square
        elif from_row > to_row and from_col > to_col:
            while (from_col - 1) != to_col:
                if board_object.get_piece_at((from_row - 1), (from_col - 1)) is None:
                    from_row -= 1
                    from_col -= 1
                else:
                    print("\nYou can't jump over any pieces. Try again.")
                    return False
        
        return True


class King(Piece):
    """
    Represents a King piece. Has methods for creating an instance of the class and validating a move.
        Communicates with Piece (the parent class) since it inherits from Piece
    """
    
    def __repr__(self):
        """
        Description: Returns a printable representational string of the King object.
        :param: none
        :return:
            '♔': if the color of the King is 'WHITE'
            '♚': if the color of the King is 'BLACK'
        """
        if self._color == "WHITE":
            return "\u2654"
        else:
            return "\u265A"
    
    def is_valid_move(self, board_object, turn, from_row, from_col, to_row, to_col):
        """
        Description: Returns True if the move is valid, otherwise returns False. Kings can only move one square
            horizontally, vertically, or diagonally.
        :param board_object: ChessBoard object
        :param turn: current player's piece color
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return:
            True: if the move is valid
            False: if the move is not valid
        """
        # make sure from_square has a piece belonging to the player, and to_square does not
        if not super().is_valid_move(board_object, turn, from_row, from_col, to_row, to_col):
            return False
        
        # check if from_square and to_square are one square apart
        if abs(to_col - from_col) > 1 or abs(to_row - from_row) > 1:
            print("\nIllegal move, try again.")
            return False
        else:
            return True


class Rook(Piece):
    """
    Represents a Rook piece. Has methods for creating an instance of the class and validating a move.
        Communicates with Piece (the parent class) since it inherits from Piece
    """
    
    def __repr__(self):
        """
        Description: Returns a printable representational string of the Rook object.
        :param: none
        :return:
            '♖': if the color of the Rook is 'WHITE'
            '♜': if the color of the Rook is 'BLACK'
        """
        if self._color == "WHITE":
            return "\u2656"
        else:
            return "\u265C"
    
    def is_valid_move(self, board_object, turn, from_row, from_col, to_row, to_col):
        """
        Description: Returns True if the move is valid, otherwise returns False. Rooks can move any number of squares
            horizontally or vertically, as long as it doesn't jump over any piece.
        :param board_object: ChessBoard object
        :param turn: current player's piece color
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return:
            True: if the move is valid
            False: if the move is not valid
        """
        # make sure from_square has a piece belonging to the player, and to_square does not
        if not super().is_valid_move(board_object, turn, from_row, from_col, to_row, to_col):
            return False
        
        # check if there is a valid path between from_square and to_square:
        if to_row == from_row:  # horizontal move
            if not super().check_horizontal_path(board_object, from_row, from_col, to_col):
                return False
        elif to_col == from_col:  # vertical move
            if not super().check_vertical_path(board_object, from_row, from_col, to_row):
                return False
        else:
            print("\nIllegal move, try again.")
            return False
        
        return True


class Bishop(Piece):
    """
    Represents a Bishop piece. Has methods for creating an instance of the class and validating a move.
        Communicates with Piece (the parent class) since it inherits from Piece
    """
    
    def __repr__(self):
        """
        Description: Returns a printable representational string of the Bishop object.
        :param: none
        :return:
            '♗': if the color of the Bishop is 'WHITE'
            '♝': if the color of the Bishop is 'BLACK'
        """
        if self._color == "WHITE":
            return "\u2657"
        else:
            return "\u265D"
    
    def is_valid_move(self, board_object, turn, from_row, from_col, to_row, to_col):
        """
        Description: Returns True if the move is valid, otherwise returns False. Bishops can move any number of squares
            diagonally, as long as it doesn't jump over any piece.
        :param board_object: ChessBoard object
        :param turn: current player's piece color
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return:
            True: if the move is valid
            False: if the move is not valid
        """
        # make sure from_square has a piece belonging to the player, and to_square does not
        if not super().is_valid_move(board_object, turn, from_row, from_col, to_row, to_col):
            return False
        
        # check if there is a valid path between from_square and to_square:
        if abs(to_col - from_col) == abs(to_row - from_row):  # diagonal move
            if not super().check_diagonal_path(board_object, from_row, from_col, to_row, to_col):
                return False
        else:
            print("\nIllegal move, try again.")
            return False
        
        return True


class Queen(Piece):
    """
    Represents a Queen piece. Has methods for creating an instance of the class and validating a move.
        Communicates with Piece (the parent class) since it inherits from Piece
    """
    
    def __repr__(self):
        """
        Description: Returns a printable representational string of the Queen object.
        :param: none
        :return:
            '♕': if the color of the Queen is 'WHITE'
            '♛': if the color of the Queen is 'BLACK'
        """
        if self._color == "WHITE":
            return "\u2655"
        else:
            return "\u265B"
    
    def is_valid_move(self, board_object, turn, from_row, from_col, to_row, to_col):
        """
        Description: Returns True if the move is valid, otherwise returns False. Queens can move any number of squares
            diagonally, horizontally, or vertically, as long as it doesn't jump over any piece.
        :param board_object: ChessBoard object
        :param turn: current player's piece color
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return:
            True: if the move is valid
            False: if the move is not valid
        """
        # make sure from_square has a piece belonging to the player, and to_square does not
        if not super().is_valid_move(board_object, turn, from_row, from_col, to_row, to_col):
            return False
        
        # check if there is a valid path between from_square and to_square:
        if to_row == from_row:  # horizontal move
            if not super().check_horizontal_path(board_object, from_row, from_col, to_col):
                return False
        elif to_col == from_col:  # vertical move
            if not super().check_vertical_path(board_object, from_row, from_col, to_row):
                return False
        elif abs(to_col - from_col) == abs(to_row - from_row):  # diagonal move
            if not super().check_diagonal_path(board_object, from_row, from_col, to_row, to_col):
                return False
        else:
            print("\nIllegal move, try again.")
            return False
        
        return True


class Knight(Piece):
    """
    Represents a Knight piece. Has methods for creating an instance of the class and validating a move.
        Communicates with Piece (the parent class) since it inherits from Piece
    """
    
    def __repr__(self):
        """
        Description: Returns a printable representational string of the Knight object.
        :param: none
        :return:
            '♘': if the color of the Knight is 'WHITE'
            '♞': if the color of the Knight is 'BLACK'
        """
        if self._color == "WHITE":
            return "\u2658"
        else:
            return "\u265E"
    
    def is_valid_move(self, board_object, turn, from_row, from_col, to_row, to_col):
        """
        Description: Returns True if the move is valid, otherwise returns False. Knights can only move
            [2 squares horizontally AND 1 square vertically] OR [1 square horizontally AND 2 square vertically].
            Knights can also jump over other pieces.
        :param board_object: ChessBoard object
        :param turn: current player's piece color
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return:
            True: if the move is valid
            False: if the move is not valid
        """
        # make sure from_square has a piece belonging to the player, and to_square does not
        if not super().is_valid_move(board_object, turn, from_row, from_col, to_row, to_col):
            return False
        
        # check if there is a valid path between from_square and to_square:
        # move 1 square horizontally and 2 squares vertically
        if abs(to_row - from_row) == 1 and abs(to_col - from_col) == 2:
            return True
        # move 2 squares horizontally and 1 square vertically
        elif abs(to_row - from_row) == 2 and abs(to_col - from_col) == 1:
            return True
        else:
            print("\nIllegal move, try again.")
            return False


class Pawn(Piece):
    """
    Represents a Pawn piece. Has methods for creating an instance of the class and validating a move.
        Communicates with Piece (the parent class) since it inherits from Piece
    """
    
    def __repr__(self):
        """
        Description: Returns a printable representational string of the Pawn object.
        :param: none
        :return:
            '♙': if the color of the Pawn is 'WHITE'
            '♟︎': if the color of the Pawn is 'BLACK'
        """
        if self._color == "WHITE":
            return "\u2659"
        else:
            return "\u265F"
    
    def is_valid_move(self, board_object, turn, from_row, from_col, to_row, to_col):
        """
        Description: Returns True if the move is valid, otherwise returns False. Pawns can move one square forward
            if there's nothing in its path. If it's the pawn's first move, it can move forward two squares, as long
            as there are no pieces in its path. Pawns can move forward diagonally one square only if there's a piece
            to capture. It can't capture vertically, and it can't move diagonally without a capture.
        :param board_object: ChessBoard object
        :param turn: current player's piece color
        :param from_row: row index of the from_square
        :param from_col: column index of the from_square
        :param to_row: row index of the to_square
        :param to_col: column index of the to_square
        :return:
            True: if the move is valid
            False: if the move is not valid
        """
        # make sure from_square has a piece belonging to the player, and to_square does not
        if not super().is_valid_move(board_object, turn, from_row, from_col, to_row, to_col):
            return False
        
        if turn == 'BLACK':  # when black pieces move forward, they move down the board
            # move down one space
            if from_row + 1 == to_row and from_col == to_col:
                if board_object.get_piece_at(to_row, to_col) is not None:
                    print("\nIllegal move: can't capture a piece vertically. Try again.")
                    return False
            # move down 2 spaces if it's the first move
            elif from_row == 1 and to_row == 3 and from_col == to_col:
                if board_object.get_piece_at((from_row + 1), to_col) is not None:
                    print("\nIllegal move: can't capture a piece vertically. Try again.")
                    return False
                if board_object.get_piece_at(to_row, to_col) is not None:
                    print("\nIllegal move: can't capture a piece vertically. Try again.")
                    return False
            # move down diagonally 1 space
            elif (from_row + 1 == to_row and from_col + 1 == to_col
                    or from_row + 1 == to_row and from_col - 1 == to_col):
                if board_object.get_piece_at(to_row, to_col) is None:
                    print("\nIllegal move: can't move pawns diagonally if there's no piece to capture. Try again.")
                    return False
            else:
                print("\nIllegal move, try again.")
                return False
        
        else:  # turn == 'WHITE', when white pieces move forward, they move up the board
            # move up one space
            if from_row - 1 == to_row and from_col == to_col:
                if board_object.get_piece_at(to_row, to_col) is not None:
                    print("\nIllegal move: can't capture a piece vertically. Try again.")
                    return False
            # move up 2 spaces if it's the first move
            elif from_row == 6 and to_row == 4 and from_col == to_col:
                if board_object.get_piece_at((from_row - 1), to_col) is not None:
                    print("\nIllegal move: can't capture a piece vertically. Try again.")
                    return False
                if board_object.get_piece_at(to_row, to_col) is not None:
                    print("\nIllegal move: can't capture a piece vertically. Try again.")
                    return False
            # move up diagonally 1 space
            elif (from_row - 1 == to_row and from_col + 1 == to_col
                    or from_row - 1 == to_row and from_col - 1 == to_col):
                if board_object.get_piece_at(to_row, to_col) is None:
                    print("\nIllegal move: can't move pawns diagonally if there's no piece to capture. Try again.")
                    return False
            else:
                print("\nIllegal move, try again.")
                return False
    
        return True

