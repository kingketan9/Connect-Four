import random
from tkinter import scrolledtext
import numpy as np
import sys
import pygame  # For the GUI
import math

row_count = 6  # total no of rows
col_count = 7  # total number of columns


def board():
    board = np.zeros((row_count, col_count))  # Make a matrix of 6*7 with all zeros
    return board


def put_piece(board, row, col, piece):  # Puts a piece in given cell
    board[row][col] = piece
    return


def can_put(board, col):  # if the column is completely filled or not
    if board[row_count - 1][col] == 0:
        return 1
    else:
        print("Can't put any more pieces in this column")
        return 0


def next_top_row(board, col):  # get empty row in given column
    for i in range(row_count):
        if board[i][col] == 0:
            return i


def print_board(board):  # To print the game board
    print(np.flip(board, 0))  # flip the board along 0


def win(board, piece):  # check if the player is winning
    # checking horizontolly
    for cols in range(col_count - 3):  # last three can't make horizontal pattern
        for rows in range(row_count):
            if (
                (board[rows][cols] == piece)
                and (board[rows][cols + 1] == piece)
                and (board[rows][cols + 2] == piece)
                and (board[rows][cols + 3] == piece)
            ):
                return True

    # Checking Vertically
    for cols in range(col_count):
        for rows in range(row_count - 3):  # Top ones can't make the pattern
            if (
                (board[rows][cols] == piece)
                and (board[rows + 1][cols] == piece)
                and (board[rows + 2][cols] == piece)
                and (board[rows + 3][cols] == piece)
            ):
                return True

    # For Diagnols
    # For going upwards
    for cols in range(col_count - 3):  # right ones can't make the pattern
        for rows in range(row_count - 3):  # Top ones can't make the pattern
            if (
                (board[rows][cols] == piece)
                and (board[rows + 1][cols + 1] == piece)
                and (board[rows + 2][cols + 2] == piece)
                and (board[rows + 3][cols + 3] == piece)
            ):
                return True
    # For diagnolly downwards
    for cols in range(col_count - 3):  # right ones can't make the pattern
        for rows in range(3, row_count):  # bottom ones can't make the pattern
            if (
                (board[rows][cols] == piece)
                and (board[rows - 1][cols + 1] == piece)
                and (board[rows - 2][cols + 2] == piece)
                and (board[rows - 3][cols + 3] == piece)
            ):
                return True


def draw_board(board):  # GUI for the board
    for c in range(col_count):
        for r in range(row_count):
            pygame.draw.rect(
                screen,
                (0, 0, 255),
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )  # draw blue squares
            # surface,color,position,dimension
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )  # Draw the circle
            # surface,color,position,radius
            # BLACK FOR EMPTY

    for c in range(col_count):
        for r in range(row_count):
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen,
                    (255, 255, 0),
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )  # Draw the circle
                # surface,color,position,radius
                # value is subtracted from height as 0,0 is left top but we need to fill from bottom
                # Player 1 Yellow

            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen,
                    (255, 0, 0),
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )  # Draw the circle
                # surface,color,position,radius
                # value is subtracted from height as 0,0 is left top but we need to fill from bottom
                # Player 2 red

    pygame.display.update()  # To update the screen


def evaluate(window, piece):
    score = 0
    opponent = 1
    if piece == 1:
        opponent = 2

    if window.count(piece) == 4:
        score += 100  # If we find 4 pieces in a row
    elif (window.count(piece) == 3) and window.count(0) == 1:
        score += 5  # if we find 3 pieces in a row and 1 empty
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    if (
        window.count(opponent) == 3 and window.count(0) == 1
    ):  # if the opponent has three in a row and a blank space
        score -= 4  # negative if the opponent is winning
    return score


def get_score(board, piece):  # For heuristic
    # Horizontally
    score = 0
    # Giving preference for piece in center
    center_array = [int(i) for i in list(board[:, col_count // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3  # three score for each piece

    for r in range(row_count):
        # extract each row from the board
        row_arr = [int(i) for i in list(board[r, :])]
        for c in range(col_count - 3):  # last 3 can't be horizontal's starting point
            window = row_arr[c : c + 4]  # take four columns at a time
            score += evaluate(window, piece)

    # For vetical
    for c in range(col_count):
        # extract each column from the board
        col_arr = [int(i) for i in list(board[:, c])]
        for c in range(row_count - 3):  # last 3 can't be vertical's starting point
            window = col_arr[c : c + 4]  # take four columns at a time
            score += evaluate(window, piece)

    # For slopes
    # slope going diagnolly up
    for r in range(row_count - 3):
        for c in range(col_count - 3):
            window = [
                board[r + i][c + i] for i in range(4)
            ]  # taking the board's diagnol elements
            score += evaluate(window, piece)

    for r in range(row_count - 3):
        for c in range(col_count - 3):
            window = [
                board[r + 3 - i][c + i] for i in range(4)
            ]  # for storing diagnolly downwards
            # +3 as we can't start from last three
            # row decrease but column increases
            score += evaluate(window, piece)

    return score


def is_terminal(board):  # check if the end is achieved
    return win(board, 1) or win(board, 2) or len(get_valid_location(board == 0))


# A node is a terminal lnode if it's either one of player wins or there is no possible moves remaining


def minmax(board, depth, alpha, beta, maximizing):  # Min-Max algorithm
    valid = get_valid_location(board)
    terminal = is_terminal(board)
    if depth == 0 or terminal:
        if terminal:  # if the game gets over
            if win(board, 2):
                return (None, 1000000000000)  # if the AI wins return a very big number
            elif win(board, 1):
                return (
                    None,
                    1000000000000,
                )  # if human wins return a vey lage negative number
            else:
                return (None, 0)  # if out of moves return 0
        else:  # If the depth is zero
            return None, get_score(
                board, 2
            )  # if we reached the final depth return the score
    if maximizing:  # For maximizing half
        value = -math.inf  # taking initial value as negative infinity
        column = random.choice(valid)  # choosing one of valid locagions randomly
        for col in valid:
            row = next_top_row(board, col)
            b_copy = board.copy()
            put_piece(b_copy, row, col, 2)
            new_score = minmax(b_copy, depth - 1, alpha, beta, False)[
                1
            ]  # calculating the score recurively
            if new_score > value:
                value = new_score  # updating hte value
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:  # Prune the branch
                break

        return column, value  # returning the max's column,the score at it

    else:  # Minimizing half
        value = math.inf  # Taking positive infinity
        for col in valid:
            row = next_top_row(board, col)
            b_copy = board.copy()
            put_piece(b_copy, row, col, 1)
            new_score = minmax(b_copy, depth - 1, alpha, beta, True)[
                1
            ]  # finding value recursively
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # Prune
        return column, value  # returning column and value


def get_valid_location(board):  # to return the valid locations
    valid_locations = []
    for col in range(col_count):
        if can_put(board, col):
            valid_locations.append(col)
    return valid_locations  # Return the columns in which move can be made


def pick_best(board, piece):  # To choose the best column
    best_score = -10000
    valid_location = get_valid_location(board)
    best_col = random.choice(
        valid_location
    )  # choose any valid lcation randomly initially
    for col in valid_location:
        row = next_top_row(
            board, col
        )  # get the row that can be filled for valid columns
        temp_board = board.copy()  # making a copy of board
        put_piece(temp_board, row, col, piece)
        score = get_score(temp_board, piece)  # get the score of current arrangement
        if score > best_score:  # if new best score is found update it
            best_score = score
            best_col = col
    return best_col


if __name__ == "__main__":

    board = board()  # A 6*7 matrix with all zeros
    game_over = False
    pygame.init()  # initializing the pygame
    SQUARESIZE = 100  # 1 square sixe is 100 pixel
    RADIUS = int(SQUARESIZE / 2 - 5)  # Radius of the inner circle
    width = col_count * SQUARESIZE
    height = (row_count + 1) * SQUARESIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)  # The dimensions of the game area
    draw_board(board)
    pygame.display.update()  # To update the screen
    my_font = pygame.font.SysFont("monospace", 45)  # Font of the final message
    turn = random.randint(0, 1)  # The turn is selected randomly
    while not game_over:
        for event in pygame.event.get():
            # Whenever a event like key press/mouse movement occurs
            if event.type == pygame.QUIT:  # If the player clicks upper red X bar
                sys.exit()

            if event.type == pygame.MOUSEMOTION:  # Whenever the mouse moves
                # For the upper space
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, SQUARESIZE))
                # masks previous colour
                posx = event.pos[0]
                if turn == 0:  # for player 1
                    pygame.draw.circle(
                        screen, (255, 255, 0), (posx, int(SQUARESIZE / 2)), RADIUS
                    )
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if   mouse is clicked
                pygame.draw.rect(
                    screen, (0, 0, 0), (0, 0, width, SQUARESIZE)
                )  # Masks previous coloured circle

                # player 1's turn
                if turn == 0:
                    # col_move = int(input(" Player 1's turn "))  # User enters column values
                    posx = event.pos[0]  # position of x-axis of mouse click
                    col_move = int(math.floor(posx / SQUARESIZE))

                    if can_put(board, col_move):
                        row = next_top_row(board, col_move)
                        put_piece(board, row, col_move, 1)  # player 1's piece is 1

                        if win(board, 1):
                            label = my_font.render(
                                "!!! Player 1 Wins !!!", 1, (255, 255, 0)
                            )
                            screen.blit(label, (40, 10))
                            # The winning message
                            game_over = True  # The game is over

                    turn += 1
                    turn = turn % 2  # Turn will be either  0 or 1
                    print_board(board)
                    draw_board(board)

        if turn == 1 and not game_over:  # AI's turn
            # col_move = int(input(" AI's turn "))
            # col_move = pick_best(board, 2)
            col_move, minmax_score = minmax(
                board, 3, -math.inf, math.inf, True
            )  # The depth of 3 for maximizing player
            # alpha==>Negative infinity
            # beta==>positive infinity
            if can_put(board, col_move):
                pygame.time.wait(400)  # time before AI makes a move
                row = next_top_row(board, col_move)
                put_piece(board, row, col_move, 2)  # AI's piece is 2

            if win(board, 2):
                label = my_font.render("!!! AI Wins !!!", 1, (255, 0, 0))
                screen.blit(label, (40, 10))
                # The winning message
                game_over = True  # The game is over

            turn += 1
            turn = turn % 2  # Turn will be either  0 or 1
            draw_board(board)
            print_board(board)
    if game_over:
        pygame.time.wait(5000)  # Wait before closing the window after game is over