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
    print("Note -- all the terminologies used in the code are related to sited paper (Zudoku)")
    print("Generating a Sudoku puzzle...")
    sudoku = initial_sudoku()
    print_grid(sudoku)
    print("Generating a solution...")
    solution = generate_sudoku_solution()
    print("-------------Solution generated successfully!-------------")

    print("Committing to the Sudoku puzzle...")
    Prover = prover.CommitmentStorage(solution)
    commitments1, commitments2, commitments3, commitments4 = Prover.get_commitments()

    print("-------------Commitments recieved successfully!-------------")
    user_input = input("Do you want to see the commitments(y/n) ? :")
    if user_input == "y" or user_input == "Y":
        print("Commitment1 for the Sudoku Solution:")
        print(commitments1)

        print("Commitment2 for the Sudoku Solution:")
        print(commitments2)

        print("Commitment3 for the Sudoku Solution:")
        print(commitments3)

        print("Commitment4 for the Sudoku Solution:")
        print(commitments4)
    else:
        print("As you wish :)\nCommitments are not displayed")


    verifier_query = input("which query you want to verify (a/b/c) : ")
    match verifier_query:
        case "a":pass
        case "b":pass
        case "c":pass
        case _:
            print("Invalid query!")
            print("Please enter a valid query (a/b/c)")
            exit(1)
