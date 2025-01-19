import prover as prover
from verifier import *

def print_grid(grid):
    """Print the Sudoku grid in a readable format."""
    for row in grid:
        print(" ".join(str(num) if num != 0 else '_' for num in row))

def initial_sudoku():
    """Generate a Sudoku puzzle."""
    sudoku = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]
    return sudoku

def generate_sudoku_solution():
    """Generate a solution for the Sudoku puzzle."""
    solution = [
        [4, 3, 5, 2, 6, 9, 7, 8, 1],
        [6, 8, 2, 5, 7, 1, 4, 9, 3],
        [1, 9, 7, 8, 3, 4, 5, 6, 2],
        [8, 2, 6, 1, 9, 5, 3, 4, 7],
        [3, 7, 4, 6, 8, 2, 9, 1, 5],
        [9, 5, 1, 7, 4, 3, 6, 2, 8],
        [5, 1, 9, 3, 2, 6, 8, 7, 4],
        [2, 4, 8, 9, 5, 7, 1, 3, 6],
        [7, 6, 3, 4, 1, 8, 2, 5, 9]
    ]
    return solution



if __name__ == "__main__":
    print("Welcome to Zudoku!")
    print("Generating a Sudoku puzzle...")
    sudoku = initial_sudoku()
    print_grid(sudoku)
    print("Generating a solution...")
    solution = generate_sudoku_solution()
    print("Solution:")
    print_grid(solution)
    print("Committing to the Sudoku puzzle...")
    commitments, triplets, random_data, commitments_value = prover.generate_commitments_for_sudoku(solution)
    cell_name_commitments = prover.commit_grid_cell_names(triplets)
    # Print the commitments for inspection
    print("Commitments for the Sudoku Solution:")
    print_grid(triplets)
    print(commitments_value)
    print(random_data)
    print(cell_name_commitments)