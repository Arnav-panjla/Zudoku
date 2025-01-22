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
    commitments1, random_data1, commitments_value1, triplets = prover.generate_commitment1(solution)
    
    print("Commitment1 for the Sudoku Solution:")
    print(commitments1)
    print_grid(triplets)
    print(commitments_value1)
    print(random_data1)

    print("Verifying the commitments...")
    commitments2, random_data2, commitments_value2 = prover.generate_commitment2(triplets)
    print("Commitment2 for the Sudoku Solution:")
    print(commitments2)
    print_grid(triplets)
    print(commitments_value2)
    print(random_data2)

    commitments3, random_data3, commitments_value3 = prover.generate_commitment3(triplets)
    print("Commitment3 for the Sudoku Solution:")
    print(commitments3)
    print(commitments_value3)
    print(random_data3)

    commitments4, random_data4, commitments_value4 = prover.generate_commitment4(solution, triplets)
    print("Commitment4 for the Sudoku Solution:")
    print(commitments4)
    print(commitments_value4)
    print(random_data4)

    print("Verifying all the commitments...")

    if verify_commitment1(commitments1, random_data1, commitments_value1):
        print("Commitment1 verified")
    else:
        print("Commitment1 verification failed")

    if verify_commitment2(commitments2, random_data2, commitments_value2):
        print("Commitment2 verified")
    else:
        print("Commitment2 verification failed")

    if verify_commitment3(commitments3, random_data3, commitments_value3):
        print("Commitment3 verified")
    else:
        print("Commitment3 verification failed")
    
    if verify_commitment4(commitments4, random_data4, commitments_value4):
        print("Commitment4 verified")
    else:
        print("Commitment4 verification failed")


