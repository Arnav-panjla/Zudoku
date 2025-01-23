from py_ecc.optimized_bn128 import G1, G2, add, multiply, pairing
from py_ecc.optimized_bn128 import field_modulus as q
import hashlib
import random


class CommitmentStorage:
    def __init__(self, solution):
        # Call the generate_all_commitments method to initialize the attributes
        commitments1, random_data1, commitments_value1, commitments2, random_data2, commitments_value2, commitments3, random_data3, commitments_value3, commitments4, random_data4, commitments_value4 = generate_all_commitments(solution)
        
        # Store the generated values as instance variables
        self.commitments1 = commitments1
        self.random_data1 = random_data1
        self.commitments_value1 = commitments_value1
        self.commitments2 = commitments2
        self.random_data2 = random_data2
        self.commitments_value2 = commitments_value2
        self.commitments3 = commitments3
        self.random_data3 = random_data3
        self.commitments_value3 = commitments_value3
        self.commitments4 = commitments4
        self.random_data4 = random_data4
        self.commitments_value4 = commitments_value4

    # You can add methods to retrieve these values as needed
    def get_commitments1(self):
        return self.commitments1

    def get_random_data1(self):
        return self.random_data1
    
    def get_commitments_value1(self):
        return self.commitments_value1
    
    def get_commitments2(self):
        return self.commitments2

    def get_random_data2(self):
        return self.random_data2
    
    def get_commitments_value2(self):
        return self.commitments_value2
    
    def get_commitments3(self):
        return self.commitments3
    
    def get_random_data3(self):
        return self.random_data3
    
    def get_commitments_value3(self):
        return self.commitments_value3
    
    def get_commitments4(self):
        return self.commitments4
    
    def get_random_data4(self):
        return self.random_data4
    
    def get_commitments_value4(self):
        return self.commitments_value4
    
    def get_commitments(self):
        return self.commitments1, self.commitments2, self.commitments3, self.commitments4
    
    


def generate_random_value():
    """Generate a random value for the Pedersen commitment."""
    return random.randint(1, 100 - 1)
    # return 1

# Define a distinct generator H for the second term in the commitment
H = multiply(G1, 8935763487)  # Using G2 as an example; you might want to define your H differently.

def commit(value, random_value):
    """
    Commit to a Sudoku value using a Pedersen commitment.
    
    :param value: The value (0-9) to commit to
    :param random_value: A random blinding factor used to hide the value
    :return: The commitment (point on elliptic curve)
    """
    # Commitment: C(x, r) = r * G + x * H
    # return add(multiply(G1, random_value), multiply(H, value))
    return value*random_value



def generate_commitment1(solution):
    """
    Generate the commitments for all cells in the Sudoku grid.
    Each cell has 3 associated values: one for row, one for column, and one for subgrid.
    
    :param solution: The completed Sudoku solution grid (2D list)
    :return: Tuple containing:
        - commitments: List of commitments for each cell
        - triplets: List of triplets, each containing indices of the three commitments for a cell
        - random_data: List of random blinding factors used for each commitment
        - commitments_value: List of original values corresponding to each commitment
    """
    n = len(solution)  # Size of the Sudoku grid (n x n)
    
    # Initialize lists to store the commitments, their corresponding values, and random blinding factors
    commitments = [None for _ in range(3 * n * n)]  # 3n² commitments for all cells
    commitments_value = [None for _ in range(3 * n * n)]  # The original values for each commitment
    triplets = [[None for __ in range(n)] for _ in range(n)]  # Store the indices of the triplets for each cell
    random_data = [None for _ in range(3 * n * n)]  # Random blinding factors used for each commitment

    # Generate a list of all possible indices (3n² total) and shuffle them
    available_indices = list(range(3 * n * n))
    random.shuffle(available_indices)  # Shuffle to ensure randomness in index assignment

    # Iterate over each cell in the Sudoku grid
    for i in range(n):
        for j in range(n):
            value = solution[i][j]  # Get the value of the current cell
            
            # Select three unique indices from the shuffled list for the current cell
            i1 = available_indices.pop()  # Index for the row-related commitment
            i2 = available_indices.pop()  # Index for the column-related commitment
            i3 = available_indices.pop()  # Index for the subgrid-related commitment

            # Store the indices in the triplets list for later verification
            triplets[i][j] = (i1, i2, i3)
            
            # Generate commitments for each of the three indices
            for idx in [i1, i2, i3]:
                random_val = generate_random_value()  # Generate a random blinding factor
                commitments[idx] = commit(value, random_val)  # Create the Pedersen commitment
                commitments_value[idx] = value  # Store the original value
                random_data[idx] = random_val  # Store the blinding factor used

    # Return the commitments, triplets, random blinding factors, and original values
    return commitments, random_data, commitments_value, triplets


def generate_commitment2(triplets):
    """
    Generate commitments for the names (positions) of the grid cells.
    
    :param triplets: A list of triples, where each triple contains the indices (i1, i2, i3) for a grid cell
    :return: List of commitments for the grid cell names
    """
    n = len(triplets)
    commitments = [ None for _ in range(n*n)]
    random_data = [ None for _ in range(n*n)]
    commitments_value = [ None for _ in range(n*n)]
    random_list = [ i for i in range(n*n)]
    print(random_list)
    random.shuffle(random_list)

    for i in range(n):
        for j in range(n):
            i1, i2, i3 = triplets[i][j]
            k = random_list.pop()
            random_val = generate_random_value()
            commitments[k] = (i1*random_val, i2*random_val,  i3*random_val)
            random_data[k] = random_val
            commitments_value[k] = (i1, i2, i3)
    
    return commitments, random_data, commitments_value



def generate_commitment3(triplets):
    """
    


    """

    n = len(triplets)
    commitments = [[None for __ in range(n)] for _ in range(n)]  
    commitments_value = [[None for __ in range(n)] for _ in range(n)]  
    random_data = [[None for __ in range(n)] for _ in range(n)]  

    for i in range(n):
        for j in range(n):
            i1, i2, i3 = triplets[i][j]
            random_val = generate_random_value()
            commitments[i][j] = (i1*random_val, i2*random_val, i3*random_val)
            random_data[i][j] = random_val
            commitments_value[i][j] = (i1, i2, i3)
    
    return commitments, random_data, commitments_value


def generate_commitment4(solution, triplets):
    """




    """
    n = len(solution)
    commitments = [[None for __ in range(n)] for _ in range(3*n)]
    random_data = [[None for __ in range(n)] for _ in range(3*n)]
    commitments_value = [[None for __ in range(n)] for _ in range(3*n)]

    for r in range(n):
        for c in range(n):
            i1, i2, i3 = triplets[r][c]
            commitment1_val = i1 # for row commitment 
            random_val = generate_random_value()
            commitments_value[r][c] = commitment1_val
            random_data[r][c] = random_val
            commitments[r][c] = random_val*commitment1_val

    for c in range(n):
        for r in range(n):
            i1, i2, i3 = triplets[r][c]
            commitment1_val = i2 # for column commitment 
            random_val = generate_random_value()
            commitments_value[n+r][c] = commitment1_val
            random_data[n+r][c] = random_val
            commitments[n+r][c] = random_val*commitment1_val
    
    subgrid_size = n//3
    for subgrid in range(n):
        # Calculate the starting row and column for the current subgrid
        start_row = (subgrid // subgrid_size) * subgrid_size
        start_col = (subgrid % subgrid_size) * subgrid_size
        
        # Now, loop over each cell in the current subgrid
        for i in range(subgrid_size):
            for j in range(subgrid_size):
                row = start_row + i
                col = start_col + j
                i1, i2, i3 = triplets[row][col]
                commitments_value[2*n + subgrid][3*i+j] = i3 # for subgrid commitment
                random_val = generate_random_value()
                random_data[2*n + subgrid][3*i+j] = random_val
                commitments[2*n + subgrid][3*i+j] = i3 * random_val       


    return commitments, random_data, commitments_value



def generate_all_commitments(solution):
    commitments1, random_data1, commitments_value1, triplets = generate_commitment1(solution)
    commitments2, random_data2, commitments_value2 = generate_commitment2(triplets)
    commitments3, random_data3, commitments_value3 = generate_commitment3(triplets)
    commitments4, random_data4, commitments_value4 = generate_commitment4(solution, triplets)
    return commitments1, random_data1, commitments_value1, commitments2, random_data2, commitments_value2, commitments3, random_data3, commitments_value3, commitments4, random_data4, commitments_value4
