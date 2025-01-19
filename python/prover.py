from py_ecc.optimized_bn128 import G1, G2, add, multiply, pairing
from py_ecc.optimized_bn128 import field_modulus as q
import hashlib
import random

def generate_random_value():
    """Generate a random value for the Pedersen commitment."""
    return random.randint(1, q - 1)

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
    return add(multiply(G1, random_value), multiply(H, value))


def commit_grid_cell_names(triplets):
    """
    Commit to the names (grid positions) of the cells for each triple of indices.
    
    :param triplets: A list of triples, where each triple contains the indices (i1, i2, i3) for a grid cell
    :return: A list of commitments for the grid cell names
    """
    n = len(triplets)
    cell_name_commitments = []
    
    for i in range(n):
        for j in range(n):
            i1, i2, i3 = triplets[i][j]
            grid_position = (i, j)  # Grid position for the cell
            
            # Convert grid position to a string for commitment
            grid_position_str = f"{grid_position}"
            
            # Use a hash-based commitment for simplicity (this can be replaced with a more secure scheme)
            position_commitment = hashlib.sha256(grid_position_str.encode()).hexdigest()
            
            # Store the commitment along with the indices
            cell_name_commitments.append((i1, i2, i3, position_commitment))
    
    return cell_name_commitments



def generate_commitments_for_sudoku(solution):
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
    return commitments, triplets, random_data, commitments_value
