from py_ecc.optimized_bn128 import G1, G2, add, multiply, pairing
from py_ecc.optimized_bn128 import field_modulus as q
import hashlib
import random

class CommitmentStorage:
    def __init__(self, solution):
        self.solution = solution  # Store the Sudoku solution
        self.n = len(solution)  # Size of the Sudoku grid (n x n)
        
        # Generate all commitments upon initialization
        self.commitments1, self.random_data1, self.commitments_value1, self.triplets = self.generate_commitment1()
        self.commitments2, self.random_data2, self.commitments_value2 = self.generate_commitment2()
        self.commitments3, self.random_data3, self.commitments_value3 = self.generate_commitment3()
        self.commitments4, self.random_data4, self.commitments_value4 = self.generate_commitment4()

    def generate_random_value(self):
        """Generate a random value for the Pedersen commitment."""
        return random.randint(1, 100 - 1)  # You can replace this with any other random generation logic
    
    def commit(self, value, random_value):
        """
        Commit to a Sudoku value using a Pedersen commitment.
        
        :param value: The value (0-9) to commit to
        :param random_value: A random blinding factor used to hide the value
        :return: The commitment (point on elliptic curve)
        """
        # Commitment formula: C(x, r) = r * G + x * H
        # Here you would normally compute elliptic curve operations. For this example, we just return a product.
        return value * random_value  # This is a simplified commitment for illustrative purposes.

    def generate_commitment1(self):
        """
        Generate the commitments for all cells in the Sudoku grid.
        
        :return: Tuple containing:
            - commitments: List of commitments for each cell
            - triplets: List of triplets, each containing indices of the three commitments for a cell
            - random_data: List of random blinding factors used for each commitment
            - commitments_value: List of original values corresponding to each commitment
        """
        # Initialize lists to store the commitments, their corresponding values, and random blinding factors
        commitments = [None for _ in range(3 * self.n * self.n)]  # 3n² commitments for all cells
        commitments_value = [None for _ in range(3 * self.n * self.n)]  # The original values for each commitment
        triplets = [[None for __ in range(self.n)] for _ in range(self.n)]  # Store the indices of the triplets for each cell
        random_data = [None for _ in range(3 * self.n * self.n)]  # Random blinding factors used for each commitment

        # Generate a list of all possible indices (3n² total) and shuffle them
        available_indices = list(range(3 * self.n * self.n))
        random.shuffle(available_indices)  # Shuffle to ensure randomness in index assignment

        # Iterate over each cell in the Sudoku grid
        for i in range(self.n):
            for j in range(self.n):
                value = self.solution[i][j]  # Get the value of the current cell
                
                # Select three unique indices from the shuffled list for the current cell
                i1 = available_indices.pop()  # Index for the row-related commitment
                i2 = available_indices.pop()  # Index for the column-related commitment
                i3 = available_indices.pop()  # Index for the subgrid-related commitment

                # Store the indices in the triplets list for later verification
                triplets[i][j] = (i1, i2, i3)
                
                # Generate commitments for each of the three indices
                for idx in [i1, i2, i3]:
                    random_val = self.generate_random_value()  # Generate a random blinding factor
                    commitments[idx] = self.commit(value, random_val)  # Create the Pedersen commitment
                    commitments_value[idx] = value  # Store the original value
                    random_data[idx] = random_val  # Store the blinding factor used

        # Return the commitments, triplets, random blinding factors, and original values
        return commitments, random_data, commitments_value, triplets

    def generate_commitment2(self):
        """
        Generate commitments for the names (positions) of the grid cells.
        
        :return: Tuple containing:
            - commitments: List of commitments for each cell name
            - random_data: List of random blinding factors used for each commitment
            - commitments_value: List of the original cell names (positions)
        """
        commitments = [None for _ in range(self.n * self.n)]
        random_data = [None for _ in range(self.n * self.n)]
        commitments_value = [None for _ in range(self.n * self.n)]
        
        # Generate a random list of indices and shuffle it
        random_list = [i for i in range(self.n * self.n)]
        random.shuffle(random_list)

        for i in range(self.n):
            for j in range(self.n):
                # Get the triplets for each cell
                i1, i2, i3 = self.triplets[i][j]
                k = random_list.pop()  # Pop an index from the shuffled list
                random_val = self.generate_random_value()  # Generate a random value
                commitments[k] = (i1 * random_val, i2 * random_val, i3 * random_val)  # Store the commitment
                random_data[k] = random_val  # Store the blinding factor
                commitments_value[k] = (i1, i2, i3)  # Store the triplet positions

        return commitments, random_data, commitments_value

    def generate_commitment3(self):
        """
        Generate commitments for each cell with the appropriate triplets for row, column, and subgrid.
        
        :return: commitments, random_data, commitments_value
        """
        commitments = [[None for __ in range(self.n)] for _ in range(self.n)]
        random_data = [[None for __ in range(self.n)] for _ in range(self.n)]
        commitments_value = [[None for __ in range(self.n)] for _ in range(self.n)]

        for i in range(self.n):
            for j in range(self.n):
                i1, i2, i3 = self.triplets[i][j]
                random_val = self.generate_random_value()
                commitments[i][j] = (i1 * random_val, i2 * random_val, i3 * random_val)
                random_data[i][j] = random_val
                commitments_value[i][j] = (i1, i2, i3)

        return commitments, random_data, commitments_value

    def generate_commitment4(self):
        """
        Generate commitments based on row, column, and subgrid indices.
        
        :return: commitments, random_data, commitments_value
        """
        commitments = [[None for __ in range(self.n)] for _ in range(3 * self.n)]
        random_data = [[None for __ in range(self.n)] for _ in range(3 * self.n)]
        commitments_value = [[None for __ in range(self.n)] for _ in range(3 * self.n)]

        # Row-based commitments
        for r in range(self.n):
            for c in range(self.n):
                i1, i2, i3 = self.triplets[r][c]
                commitment1_val = i1  # For row commitment 
                random_val = self.generate_random_value()
                commitments_value[r][c] = commitment1_val
                random_data[r][c] = random_val
                commitments[r][c] = random_val * commitment1_val

        # Column-based commitments
        for c in range(self.n):
            for r in range(self.n):
                i1, i2, i3 = self.triplets[r][c]
                commitment1_val = i2  # For column commitment 
                random_val = self.generate_random_value()
                commitments_value[self.n + r][c] = commitment1_val
                random_data[self.n + r][c] = random_val
                commitments[self.n + r][c] = random_val * commitment1_val

        # Subgrid-based commitments
        subgrid_size = self.n // 3
        for subgrid in range(self.n):
            # Calculate the starting row and column for the current subgrid
            start_row = (subgrid // subgrid_size) * subgrid_size
            start_col = (subgrid % subgrid_size) * subgrid_size
            
            # Now, loop over each cell in the current subgrid
            for i in range(subgrid_size):
                for j in range(subgrid_size):
                    row = start_row + i
                    col = start_col + j
                    i1, i2, i3 = self.triplets[row][col]
                    commitments_value[2 * self.n + subgrid][3 * i + j] = i3  # For subgrid commitment
                    random_val = self.generate_random_value()
                    random_data[2 * self.n + subgrid][3 * i + j] = random_val
                    commitments[2 * self.n + subgrid][3 * i + j] = i3 * random_val

        return commitments, random_data, commitments_value

    def get_commitments(self):
        return  self.commitments1, self.commitments2, self.commitments3, self.commitments4
    

    # Getter methods to access the variables
    def get_commitments1(self):
        return self.commitments1

    def get_random_data1(self):
        return self.random_data1

    def get_commitments_value1(self):
        return self.commitments_value1

    def get_triplets(self):
        return self.triplets

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


    