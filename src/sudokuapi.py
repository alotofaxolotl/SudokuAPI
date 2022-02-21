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

    def __init__(self, grid: list) -> None:
        self.grid = grid

    def load_sudoku_from_file(self, filepath: str) -> None:

        # Read in the specified file
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    # Lines should appear as '1, 3, 7, 0, 0, 0, ...'
                    # One line per row
                    self.grid.append([int(n) for n in line.split(',')])
            return

        except FileNotFoundError:
            print(f'{filepath} does not exist!')

        except ValueError:
            print(f'A value in {filepath} was not a number!')

        self.grid = []

    def is_number_in_row(self, number: int, row: int) -> bool:
        return number in self.grid[row]

    def is_number_in_column(self, number: int, column: int) -> bool:
        return number in [row[column] for row in self.grid]