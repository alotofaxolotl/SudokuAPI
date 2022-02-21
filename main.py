from src.sudokuapi import Sudoku

sudoku = Sudoku()
sudoku.load_sudoku_from_file('sudoku')

sudoku.solve()