from random import randint
import string


class MineSweeper:
    def __init__(self, size, mines):
        self.size = size
        self.mines = mines
        self.board = self.CreateBoard()

    def CreateBoard(self):
        list = [[' ' for _ in range(self.size)]]
        for row in range(self.size):
            list.append([' ' for _ in range(self.size)])
        return list

    def display_board(self):
        print('  |', end='')
        for y in range(0, self.size):
            print(' ' + str(y) + ' ', end='|')
        print('\n', end='')
        print('-' * int(self.size * 5))
        for x in range(0, self.size):
            print(x, end=' ')
            print('| ', end='')
            print(' | '.join(self.board[x]), end=' |\n')
        print('\n')

    def SetMines(self):
        for x in range(self.mines):
            row = randint(0, self.size - 1)
            column = randint(0, self.size - 1)
            while self.board[row][column] == 'x':
                row = randint(0, self.size - 1)
                column = randint(0, self.size - 1)
            self.board[row][column] = 'x'

    def SetValue(self):
        self.SetMines()
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] == 'x':
                    continue
                self.board[row][column] = self.NearMines(row, column)

    def NearMines(self, row, column):
        count = 0
        for r_check in range(max(0, row - 1), min(self.size - 1, row + 1) + 1):
            for c_check in range(max(0, column - 1), min(self.size - 1, column + 1) + 1):
                if self.board[r_check][c_check] == 'x':
                    count += 1
        return str(count)

    def reveal(self, row, column, res):
        self.board[row][column] = res[row][column]
        if res[row][column] == 'x':
            self.display_board()
            print("You lost :(\nFinal board is:\n")
            return -1
        if res[row][column] == '0':
            self.ShowZero(row, column, res)
        self.display_board()
        return 0

    def EndGame(self, hidden):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == ' ' and hidden[x][y] != 'x':
                    return 1
        return 0

    def ShowZero(self, row, column, hidden):
        # my first method to discover 0 in a square 3x3
        # if hidden[row][column] == '0':
        #     for x in range(max(0, row - 1), min(self.size - 1, row + 1) + 1):
        #         for y in range(max(0, column - 1), min(self.size - 1, column + 1) + 1):
        #             if hidden[x][y] != 'x':
        #                 self.board[x][y] = hidden[x][y]

        #i know its not optimal but it works
        self.board[row][column] = hidden[row][column]
        for z in range(self.size ** 2):
            for x in range(self.size):
                for y in range(self.size):
                    if self.board[x][y] == '0':
                        if hidden[x][y] != '0':
                            if hidden[x][y] != 'x':
                                self.board[x][y] = hidden[x][y]
                            break
                        self.LeftRight(x, y, hidden)
                        self.HighLow(x, y, hidden)
                        self.board[x][y] = hidden[x][y]
        return

    def LeftRight(self, row, column, hidden):
        y = column - 1
        while y >= 0:
            if hidden[row][y] != '0':
                self.board[row][y] = hidden[row][y]
                break
            self.board[row][y] = hidden[row][y]
            y -= 1

        y = column + 1
        while y < self.size:
            if hidden[row][y] != '0':
                self.board[row][y] = hidden[row][y]
                break
            self.board[row][y] = hidden[row][y]
            y += 1

        return

    def HighLow(self, row, column, hidden):
        # reveal hidden 0 higher
        x = row - 1
        while x >= 0:
            if hidden[x][column] != '0':
                self.board[x][column] = hidden[x][column]
                break
            self.board[x][column] = hidden[x][column]
            x -= 1

        # reveal hidden 0 lower
        x = row + 1
        while x < self.size:
            if hidden[x][column] != '0':
                self.board[x][column] = hidden[x][column]
                break
            self.board[x][column] = hidden[x][column]
            x += 1
        return


def play(size=10, mines=5):
    if size ** 2 < mines:
        print('input data error')
        exit()
    hidden = MineSweeper(size, mines)
    hidden.SetValue()
    player = MineSweeper(size, mines)
    player.display_board()
    # -1 = lose | 0 = still in game
    result = 0
    row = 0
    column = 0
    start = 1
    while result == 0:
        row = -1
        column = -1
        row, column = input("Where to dig(row,column): ").split()
        if row.isdigit() is False or column is False:
            print("Incorrect input")
            continue
        row = int(row)
        column = int(column)
        if row >= size or column >= size or column < 0 or row < 0:
            print("Incorrect input")
            continue
        while start == 1:
            if hidden.board[row][column] == '0':
                start = 0
                break
            hidden = MineSweeper(size, mines)
            hidden.SetValue()

        result = player.reveal(row, column, hidden.board)
        if player.EndGame(hidden.board) == 0:
            hidden.display_board()
            print('You won!!! :)')
            quit()
    if result == -1:
        hidden.display_board()


if __name__ == '__main__':
    print('''       
        WELCOME TO MY MINESWEEPER
The rules are the same as real minesweeper:
You start with one empty grid where the mines are hidden.
For this moment there are no flaging option.
To dig you will be asked to write the coordinates (rows, columns).
If you dig every field without activating the mines you will win
Your first move will never active a bomb and will land on a 0 area

Enjoy and good luck :)

''')
    play()

# by Theo_TDS
