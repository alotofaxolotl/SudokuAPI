"""
Solving A Sudoku:

The simplest, but not fastest, way to solve a Sudoku would be to brute-force it. Simply
fill in each empty cell with a posible number, check to see if it is a valid solution,
and recurse until one is found. But with 9^81 possible configurations, that's not fast enough.

When solving a maze, the one efficent solution is pretty straight-forward. Keep turning left
until you hit a dead end. When you do, go back to the previous turn and go a different way.
If there are no other options, then go back to the step before that. Eventually, you will find
the sequence of turns to solve the maze. 

A Sudoku puzzle can be treated much the same way, but with the digits 1-9 instead of the direction
to turn (which is also numbered). There are also some additional rules about what numbers can
go where, but the solution used here is similar to the maze solution.

Unlike the maze, there is no clear starting point in a Sudoku puzzle. Instead, each cell must be
evaluated to determine it's score. The score is the total number of digits that could go in a cell,
the lower the better. By finding this cell it means that we limit the number of digits we have to
try (or number of turns to take in our maze analogy).

So, to solve...
1. Evaluate all cells and determine cells with lowest score. Pick any (for now).
2. Put the first possible digit in that cell, and store it's index and value in a stack.
3. Evaluate all cells again and pick one with the lowest score.
4. Put the first possible digit in that cell, and store it's index and value in a stack.

If we legally populate all cells, the Sudoku is solved.
If we cannot legally populate a cell, then go back to the previous cell (the one on top of the stack)
and change it's value to the next possible digit. If there are no more possible digits, then pop it
from the stack and go to the previous one again. Repeat until a solution is found.
"""

class Sudoku:

    def __init__(self) -> None:
        self.grid = []

    def assign_grid(self, grid: list):
        self.grid = grid

    def load_sudoku_from_file(self, filepath: str) -> None:

        # Read in the specified file
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    # Lines should appear as '1, 3, 7, 0, 0, 0, ...'
                    # One line per row
                    line = line.rstrip('\n').replace(' ', '')
                    self.grid.append([int(n) for n in line.split(',')])
            return

        except FileNotFoundError:
            print(f'{filepath} does not exist!')

        except ValueError:
            print(f'A value in {filepath} was not a number!')

        self.grid = []

    def get_assignable_coords(self) -> list:

        coords = []

        for row in range(9):
            for column in range(9):
                if self.grid[row][column] == 0:
                    coords.append((row, column))

        return coords

    # use a grid coord to find a square coord
    # for example the cell (4, 7) is in square (1, 2)
    def get_square_coord(self, coord: tuple) -> tuple:
        return (coord[0]//3, coord[1]//3)

    # get the list of numbers in a given row in the sudoku
    def get_numbers_in_row(self, row: int) -> list:
        return self.grid[row]

    # get the list of numbers in a given column in the sudoku
    def get_numbers_in_column(self, column: int) -> bool:
        return [row[column] for row in self.grid]

    # get the list of numbers in a given square in the sudoku
    def get_numbers_in_square(self, square: tuple) -> bool:
        nums = []
        for row in range(3):
            for column in range(3):
                # square coord * 3 gives cell coord
                # the top left cell in square (2, 1) is (6, 3)
                nums.append(self.grid[square[0]*3 + row][square[1]*3 + column])
        return nums

    # looks at all numbers in the row, column and square of a givel cell
    # and determines what numbers haven't been used
    def get_legal_numbers(self, coord: tuple) -> list:

        # The numbers that the current cell cannot be
        nums = []
        r_nums = self.get_numbers_in_row(coord[0])
        c_nums = self.get_numbers_in_column(coord[1])
        s_nums = self.get_numbers_in_square(self.get_square_coord(coord))

        for i in range(9):
            nums.append(r_nums[i])
            nums.append(c_nums[i])
            nums.append(s_nums[i])

        # Only check numbers greater than the current value of the cell
        cell_value = self.grid[coord[0]][coord[1]]

        legal_nums = []

        # Add 1 to exclude current value and include 9
        for n in range(cell_value, 9):
            if n+1 not in nums:
                legal_nums.append(n+1)

        return legal_nums

    # A linear search to find the cell with the least options
    # Returns an array [coord, legal_nums]
    def find_best_cell(self, coords: list):

        best = 9
        result = []

        for coord in coords:
            legal_nums = self.get_legal_numbers(coord)

            if len(legal_nums) < best:
                result = [coord, legal_nums]

            if len(legal_nums) == 1:
                return result

        return result

    def solve(self):

        # Determine initally empty cells
        coords = self.get_assignable_coords()

        stack = []

        # Find the first move
        print(self.find_best_cell(coords))
