#!/usr/bin/env python3
"""
TicTacToe Game
"""
import json


def __save(board, file):
    """
    Save board
    """
    data = {}
    for y in range(3):
        data[y] = {}
        for x in range(3):
            data[y][x] = board[y][x]
    try:
        json.dump(data, open(file, 'w'), indent=4)
    except IOError as e:
        print('Error saving to file: {0}'.format(e))


def __load(board, file):
    """
    Load board
    """
    try:
        data = json.load(open(file, 'r'))
        for y in range(3):
            for x in range(3):
                board[y][x] = data[str(y)][str(x)]
    except IOError as e:
        print('Error loading from file: {0}'.format(e))


def __check(mark, board):
    """
    Check if winning condition has been met
    """
    
    # Check rows
    for y in range(3):
        # Check row
        if __check_y(y, mark, board):
            return True

    # Check columns
    for x in range(3):
        if __check_x(x, mark, board):
            return True

    # Check diagonals
    if __check_c(mark, board):
        return True
    return False


def __check_y(y, mark, board):
    """
    Check row
    """
    for x in range(3):
        if board[y][x] != mark:
            return False
    return True


def __check_x(x, mark, board):
    """
    Check column
    """
    for y in range(3):
        if board[y][x] != mark:
            return False
    return True


def __check_c(mark, board):
    """
    Check diagonals
    """
    lr = 0
    rl = 0
    for i in range(3):
        if board[i][i] == mark:
            lr += 1
    for i in range(3):
        if board[i][2-i] == mark:
            rl += 1
    if lr == 3 or rl == 3:
        return True
    return False


def __full(board):
    """
    Check if the board is full
    """
    for y in range(3):
        for x in range(3):
            if board[y][x] == '_':
                return False
    return True


def __print_board(board):
    """
    Print board
    """
    print(chr(27) + '[2J' + chr(27) + '[;H')
    print(' _ _ _ ')
    print('|{0}|{1}|{2}|'.format(board[0][0], board[0][1], board[0][2]))
    print('|{0}|{1}|{2}|'.format(board[1][0], board[1][1], board[1][2]))
    print('|{0}|{1}|{2}|'.format(board[2][0], board[2][1], board[2][2]))


def __as_c(direction, mark, array, board):
    """
    Evaluate diagonal possibility
    """
    free = 0
    own = 0

    # Check top left to bottom right diagonal
    if direction == 'lr':
        for i in range(3):
            if board[i][i] == '_':
                array[i][i] += 1
                free += 1
            elif board[i][i] == mark:
                array[i][i] = 0
                own += 1
            else:
                array[i][i] = 0
        # Add possible modifiers to probability
        if free + own == 3:
            if own == 2:
                for i in range(3):
                    if array[i][i] != 0:
                        array[i][i] += 15
            if own == 1:
                for i in range(3):
                    if array[i][i] != 0:
                        array[i][i] += 1

    # Check top right to bottom left
    elif direction == 'rl':
        for i in range(3):
            if board[i][2-i] == '_':
                array[i][2-i] += 1
                free += 1
            elif board[i][2-i] == mark:
                array[i][2-i] = 0
                own += 1
            else:
                array[i][2-i] = 0
        # Add possible modifiers to probability
        if free + own == 3:
            if own == 2:
                for i in range(3):
                    if array[i][2-i] != 0:
                        array[i][2-i] += 15
            if own == 1:
                for i in range(3):
                    if array[i][2-i] != 0:
                        array[i][2-i] += 1


def __as_y(y, mark, array, board):
    """
    Evaluate horizontal weight
    """
    free = 0
    own = 0
    foe = 0
    # Check each row
    for x in range(3):
        if board[y][x] == '_':
            array[y][x] += 1
            free += 1
        elif board[y][x] == mark:
            array[y][x] = 0
            own += 1
        else:
            array[y][x] = 0
            foe += 1
    # Add possible modifiers to weight
    if free + own == 3:
        if own == 2:
            for x in range(3):
                if array[y][x] != 0:
                    array[y][x] += 15
        if own == 1:
            for x in range(3):
                if array[y][x] != 0:
                    array[y][x] += 1
    elif foe == 2:
        for x in range(3):
            if board[y][x] == '_':
                array[y][x] = 5


def __as_x(x, mark, array, board):
    """
    Evaluate vertical weight
    """
    free = 0
    own = 0
    foe = 0
    # Check each column
    for y in range(3):
        if board[y][x] == '_':
            array[y][x] += 1
            free += 1
        elif board[y][x] == mark:
            array[y][x] = 0
            own += 1
        else:
            array[y][x] = 0
            foe += 1
    # Add possible modifiers to weight
    if free + own == 3:
        if own == 2:
            for y in range(3):
                if array[y][x] != 0:
                    array[y][x] += 15
        if own == 1:
            for y in range(3):
                if array[y][x] != 0:
                    array[y][x] += 1
    elif foe == 2:
        for y in range(3):
            if board[y][x] == '_':
                array[y][x] = 5


def __artificial_stupidity(board):
    """
    Determine placement
    """
    weight_array = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0], ]
    
    # Calculate weight
    for i in range(3):
        __as_y(i, 'O', weight_array, board)
        __as_x(i, 'O', weight_array, board)
    __as_c('lr', 'O', weight_array, board)
    __as_c('rl', 'O', weight_array, board)
    
    # Put each probability value into dictionary with coordinates as key
    vals = {}
    for i in range(3):
        max_value = max(weight_array[i])
        max_index = weight_array[i].index(max_value)
        vals.update({'{0},{1}'.format(i, max_index): max_value})
    
    # Return coordinates of largest value
    return max(vals, key=vals.get)


def play():
    """
    Play the game
    """
    board = [['_', '_', '_'],
             ['_', '_', '_'],
             ['_', '_', '_'], ]
    
    # print('''
    # Place your marker by coordinates entering coordinates like: 0,0
    # Commands:
    # q: quit
    # s: save
    # l: load
    # ''')
    # input('Enter to continue..')

    state = None

    while True:
        __print_board(board)

        # Your move
        string = input('Your move (y,x): ')
        # if string == 'q':
        #     break
        # elif string == 's':
        #     __save(board, 'tictactoe.txt')
        #     continue
        # elif string == 'o':
        #     __load(board, 'tictactoe.txt')
        #     continue
        coords = string.strip().split(',')
        try:
            y = int(coords[0])
            x = int(coords[1])
        except ValueError:
            print('Only integer characters separated by comma allowed.')
            input('Enter to continue..')
            continue
        try:
            if board[y][x] in ('O', 'X'):
                print('Occupied location.')
                input('Enter to continue..')
                continue
        except IndexError:
            print('Out of bounds.')
            input('Enter to continue..')
            continue
    
        board[y][x] = 'X'
        if __check('X', board):
            print('You win!')
            state = 0
            break

        # Check if more moves are possible
        if __full(board):
            __print_board(board)
            print("It's a draw!")
            state = 1
            break

        # Opponent move
        coords = __artificial_stupidity(board).split(',')
        y = int(coords[0])
        x = int(coords[1])
        board[y][x] = 'O'

        if __check('O', board):
            __print_board(board)
            print('You lose!')
            state = 2
            break

    return state
