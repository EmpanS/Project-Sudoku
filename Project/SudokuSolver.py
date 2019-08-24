import copy
import sys
sys.setrecursionlimit(10000)


class SudokuSolver:
    """
    A class used to represent a Sudoku solver

    When using the solve method, the Sudoku board should be represented as a list of list of integers where an empty box
    is represented as -1.
    sudoku_board =   [[-1, -1, -1,  6, -1,  4,  7, -1, -1],
                      [ 7, -1,  6, -1, -1, -1, -1, -1,  9],
                      [-1, -1, -1, -1, -1,  5, -1,  8, -1],
                      [-1,  7, -1, -1,  2, -1, -1,  9,  3],
                      [ 8, -1, -1, -1, -1, -1, -1, -1,  5],
                      [ 4,  3, -1, -1,  1, -1, -1,  7, -1],
                      [-1,  5, -1,  2, -1, -1, -1, -1, -1],
                      [ 3, -1, -1, -1, -1, -1,  2, -1,  8],
                      [-1, -1,  2,  3, -1,  1, -1, -1, -1]]

    Attributes
    ----------
    number_of_insertions : int
        represents the number of made insertions

    Methods
    -------
    solve(sudoku_board, insert_idx=(0, 0), value=-1)
        Solves the given Sudoku board by recursion.
    is_valid_board(self, sudoku_board)
        Validates the given Sudoku board by validating all inserted numbers using the three characteristic conditions.
    print_board(self, sudoku_board):
        Prints the Sudoku board, using an output-format that visualizes the grid.
    __is_insertion_valid(self, sudoku_board, value, position):
        Validates if a given insertion is valid.
    __is_valid_3x3_box(self, sudoku_board, value, position):
        Validates if a given insertion is valid based on the numbers in the affected 3x3-box.
    __is_valid_row(self, sudoku_board, value, position):
        Validates if a given insertion is valid based on the numbers in the affected row.
    __is_valid_column(self, sudoku_board, value, position):
        Validates if a given insertion is valid based on the numbers in the affected col.
    __is_new_row(self, sudoku_board, insert_idx):
        Checks, given the Sudoku board and an insert_idx, if there is an empty box in the row described by the
        insert_idx.
    """

    def __init__(self):
        self.number_of_insertions = 0

    def solve(self, sudoku_board, insert_idx=(0, 0), value=-1):
        """Solves the given Sudoku board using a BRUTE-FORCE strategy. The solution is found by recursion.

        When calling the function the first time, insert_idx nor value should be specified.

        Parameters
        ----------
        sudoku_board : two-dimensional list (9x9)
            The Sudoku board with empty boxes represented as -1.
        insert_idx : tuple, (default is (0, 0))
            The index of where the next number should be inserted represented as (row, col).
        value : int, (default is -1, indicating no recursion has been made)
            The number that should be inserted next.

        Returns
        -------
        tuple
            a tuple with with the Sudoku board as the first object and a boolean as the second. The boolean is True if
            a solution was found, otherwise False. If a solution is found, the Sudoku board (as the first object) will
            represent the solution.
        """

        insert_row = insert_idx[0]
        insert_col = insert_idx[1]
        if value != -1:
            sudoku_board[insert_row][insert_col] = value
            # If the insertions was made at the the bottom right corner, a solution has been found.
            if insert_idx == (8, 8):
                print("Found a solution after {} number of insertions.\n".format(self.number_of_insertions), end='')
                return sudoku_board, True

        # Checks if there are remaining empty boxes at the insert_row, if not, switch to next row.
        if self.__is_new_row(sudoku_board, insert_idx=insert_idx):
            insert_col = 0
            insert_row += 1

        # Loops through all remaining boxes at the current row represented by insert_row
        if insert_row < 9:
            for candidate_col in range(insert_col, 9):
                if sudoku_board[insert_row][candidate_col] == -1:
                    # Try to insert a number
                    return self.__insert_new_number(sudoku_board, insert_row, candidate_col)
            # If there are no remaining empty boxes, a solution has been found.
        else:
            print("Found a solution after {} number of insertions.\n".format(self.number_of_insertions), end='')
            return sudoku_board, True

    def is_valid_board(self, sudoku_board):
        """Validates the given Sudoku board by validating all inserted numbers using the three characteristic
        conditions.

        Each inserted number is removed one at the time, then it validates if the insertion of the same number at the
        same position is valid.

        Parameters
        ----------
        sudoku_board : two-dimensional list (9x9)
            The Sudoku board with empty boxes represented as -1.


        Returns
        -------
        boolean
            a boolean representing if the Sudoku board is valid or not. True if valid, False otherwise.
        """

        for row in range(9):
            for col in range(9):
                if sudoku_board[row][col] != -1:
                    number = sudoku_board[row][col]
                    sudoku_board[row][col] = -1
                    # If the insertion is not valid, return False
                    if not self.__is_insertion_valid(sudoku_board, value=number, position=(row, col)):
                        sudoku_board[row][col] = number
                        return False
                    # Else, insert the number again and continue
                    else:
                        sudoku_board[row][col] = number
        return True

    def print_board(self, sudoku_board):
        """Prints the Sudoku board, using an output-format that visualizes the grid.

        Parameters
        ----------
        sudoku_board : two-dimensional list (9x9)
            The Sudoku board with empty boxes represented as -1.
        """

        print("Printing the Sudoku board...")
        for row_index, row in enumerate(sudoku_board):
            if row_index % 3 == 0:
                print(" -------------------------")
            for col_index, number in enumerate(row):
                if col_index % 3 == 0:
                    print(" |", end='')
                if number != -1:
                    print(" " + str(number), end='')
                else:
                    print("  ", end='')
            print(" |")
        print(" -------------------------")

    def __is_insertion_valid(self, sudoku_board, value, position):
        """Validates if a given insertion is valid.

        Given a candidate to be inserted, represented by its position and value, this function validates all three
        different conditions peculiar to Sudoku.

        Parameters
        ----------
        sudoku_board : two-dimensional list (9x9)
            The Sudoku board with empty boxes represented as -1.
        value : int
            The number of the candidate.
        position : tuple
            The position of the candidate represented as (row, col).

        Returns
        -------
        boolean
            a boolean representing if the insertion is valid or not. True if valid, False otherwise.
        """

        return self.__is_valid_3x3_box(sudoku_board, value, position) and \
               self.__is_valid_row(sudoku_board, value, position)     and \
               self.__is_valid_column(sudoku_board, value, position)

    def __is_valid_3x3_box(self, sudoku_board, value, position):
        """Validates if a given insertion is valid based on the already placed numbers in the affected 3x3 - box.

        Parameters
        ----------
        sudoku_board : two-dimensional list (9x9)
            The Sudoku board with empty boxes represented as -1.
        value : int
            The number of the candidate.
        position : tuple
            The position of the candidate represented as (row, col).

        Returns
        -------
        boolean
            a boolean representing if the insertion is valid or not. True if valid, False otherwise.
        """

        # x_box and y_box represents the coordinates of the upper left corner in the affected 3x3-box.
        x_box = int(position[0] / 3) * 3
        y_box = int(position[1] / 3) * 3
        for row in range(x_box, x_box + 3):
            for col in range(y_box, y_box + 3):
                if value == sudoku_board[row][col]:
                    return False
        return True

    def __is_valid_row(self, sudoku_board, value, position):
        """Validates if a given insertion is valid based on the already placed numbers in the affected row.

        Parameters
        ----------
        sudoku_board : two-dimensional list (9x9)
            The Sudoku board with empty boxes represented as -1.
        value : int
            The number of the candidate.
        position : tuple
            The position of the candidate represented as (row, col).

        Returns
        -------
        boolean
            a boolean representing if the insertion is valid or not. True if valid, False otherwise.
        """

        for col in range(9):
            if value == sudoku_board[position[0]][col]:
                return False
        return True

    def __is_valid_column(self, sudoku_board, value, position):
        """Validates if a given insertion is valid based on the already placed numbers in the affected col.

        Parameters
        ----------
        sudoku_board : two-dimensional list (9x9)
            The Sudoku board with empty boxes represented as -1.
        value : int
            The number of the candidate.
        position : tuple
            The position of the candidate represented as (row, col).

        Returns
        -------
        boolean
            a boolean representing if the insertion is valid or not. True if valid, False otherwise.
        """

        for row in range(9):
            if value == sudoku_board[row][position[1]]:
                return False
        return True

    def __is_new_row(self, sudoku_board, insert_idx):
        """Checks, given the Sudoku board and an insert_idx, if there is an empty box in the row described by the
        insert_idx. If there is no empty box remaining, the insertion should be made at the next row.

        Parameters
        ----------
        sudoku_board : two-dimensional list (9x9)
            The Sudoku board with empty boxes represented as -1.
        insert_idx : tuple
            The position of the candidate represented as (row, col).

        Returns
        -------
        boolean
            a boolean representing if the there is an empty box at the given row. False if there is at least one empty
            box, True otherwise.
        """

        for remaining_col in range(insert_idx[1], 9):
            if sudoku_board[insert_idx[0]][remaining_col] == -1:
                return False
        return True

    def __insert_new_number(self, sudoku_board, insert_row, candidate_col):
        self.number_of_insertions += 1
        for candidate in range(1, 10):
            if self.__is_insertion_valid(sudoku_board, value=candidate,
                                         position=(insert_row, candidate_col)):
                # If the insertion is valid, insert the value and try to solve the remaining part of
                # the Sudoku.
                result = self.solve(copy.deepcopy(sudoku_board), insert_idx=(insert_row, candidate_col),
                                    value=candidate)
                if result[1]:
                    return result[0], True
        # If no insertion was possible, a solution has not been found.
        return sudoku_board, False
