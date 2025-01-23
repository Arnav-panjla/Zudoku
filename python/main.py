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
    user_decision = input("Do you want to see the commitments for all steps(y/n) ? :")
    if user_decision == "y" or user_decision == "Y":
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
        case "a":
            print("ask the prover to open the commitmnet 1 & 4")
            print("Opening commitment1...")
            commitments1_value = Prover.get_commitments_value1()
            commitments1_random_data = Prover.get_random_data1()
            if user_decision == "y" or user_decision == "Y":
                print("commitment1_value: \n", commitments1_value)
                print("commitment1_random_data: \n", commitments1_random_data)
                print()
            print("Verifying commitment1...")
            if verify_commitment1(commitments1, commitments1_random_data, commitments1_value):
                print("Commitment1 verified successfully!")
            else:
                print("Commitment1 verification failed!")

            print("Opening commitment4...")
            commitments4_value = Prover.get_commitments_value4()
            commitments4_random_data = Prover.get_random_data4()
            if user_decision == "y" or user_decision == "Y":
                print("commitment4_value: \n", commitments4_value)
                print("commitment4_random_data: \n", commitments4_random_data)
                print()
            print("Verifying commitment4...")
            if verify_commitment4(commitments4, commitments4_random_data, commitments4_value):
                print("Commitment4 verified successfully!")
            else:
                print("Commitment4 verification failed!")

            print("--- checking for query A ---")
            print("Each set contains n different numbers and no two sets intersect")
            if verify_query_a(commitments1_value, commitments4_value):
                print("Query A verified successfully!")
            else:
                print("Query A verification failed!")

        case "b":
            print("ask the prover to open the commitmnet 1 & 2")
            print("Opening commitment1...")
            commitments1_value = Prover.get_commitments_value1()
            commitments1_random_data = Prover.get_random_data1()
            if user_decision == "y" or user_decision == "Y":
                print("commitment1_value: \n", commitments1_value)
                print("commitment1_random_data: \n", commitments1_random_data)
                print()
            print("Verifying commitment1...")
            if verify_commitment1(commitments1, commitments1_random_data, commitments1_value):
                print("Commitment1 verified successfully!")
            else:
                print("Commitment1 verification failed!")

            print("Opening commitment2...")
            commitments2_value = Prover.get_commitments_value2()
            commitments2_random_data = Prover.get_random_data2()
            if user_decision == "y" or user_decision == "Y":
                print("commitment2_value: \n", commitments2_value)
                print("commitment2_random_data: \n", commitments2_random_data)
                print()
            print("Verifying commitment2...")
            if verify_commitment2(commitments2, commitments2_random_data, commitments2_value):
                print("Commitment2 verified successfully!")
            else:
                print("Commitment2 verification failed!")

            print("--- checking for query B ---")
            print("each tuple corresponds to same value and every number appears in tupple")
            if verify_query_b(commitments1_value, commitments2_value):
                print("Query B verified successfully!")
            else:
                print("Query B verification failed!")


        case "c":pass
        case _:
            print("Invalid query!")
            print("Please enter a valid query (a/b/c)")
            exit(1)
    print("-------------Verification completed successfully!-------------")
    print("we have 2/3 soundness error with zeroknowledge property")
    print("Thank you for using Zudoku!")