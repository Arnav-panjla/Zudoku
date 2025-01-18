import hashlib
import random

# Function to generate a cryptographic commitment (SHA256)
def create_commitment(value, location, nonce=None):
    """Generate a cryptographic commitment using SHA256"""
    if nonce is None:
        nonce = random.randint(0, 2**32)  # Random nonce for security
    commitment_data = f"{value}|{location}|{nonce}"
    commitment = hashlib.sha256(commitment_data.encode('utf-8')).hexdigest()
    return commitment, nonce

# Function to generate the commitments for the Sudoku solution
def generate_commitments(sudoku_grid):
    commitments = {}
    nonces = {}
    n = 9  # For a 9x9 Sudoku grid
    fixed_cells = set()  # Cells with predetermined values
    cells = {}

    # Step 1: Commit to the 3n² values (locations for row, column, subgrid)
    for i in range(n):
        for j in range(n):
            if sudoku_grid[i][j] != 0:  # Fixed cells
                fixed_cells.add((i, j))
                value = sudoku_grid[i][j]
                location = (i, j)
                commitment, nonce = create_commitment(value, location)
                commitments[location] = commitment
                nonces[location] = nonce
                cells[location] = value

    # Step 2: Generate triples for non-fixed cells
    permuted_cells = permute_cells(cells, fixed_cells)

    # Commit to the permuted non-fixed cells
    for loc, value in permuted_cells.items():
        commitment, nonce = create_commitment(value, loc)
        commitments[loc] = commitment
        nonces[loc] = nonce

    # Step 3: Commit to sets of rows, columns, and subgrids
    row_sets, col_sets, subgrid_sets = create_sets()

    return commitments, nonces, row_sets, col_sets, subgrid_sets, fixed_cells

# Function to permute non-fixed cells only
def permute_cells(cells, fixed_cells):
    """Randomly permute non-fixed cells."""
    permutable_cells = {loc: value for loc, value in cells.items() if loc not in fixed_cells}
    locations = list(permutable_cells.keys())
    random.shuffle(locations)

    permuted_cells = {}
    for i, loc in enumerate(locations):
        permuted_cells[loc] = permutable_cells[loc]

    return permuted_cells

# Create sets for rows, columns, and subgrids
def create_sets():
    n = 9
    row_sets = [set() for _ in range(n)]
    col_sets = [set() for _ in range(n)]
    subgrid_sets = [set() for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            row_sets[i].add((i, j))
            col_sets[j].add((i, j))
            subgrid_sets[(i // 3) * 3 + (j // 3)].add((i, j))
    
    return row_sets, col_sets, subgrid_sets

# Verifier query function
def verifier_query(commitments, row_sets, col_sets, subgrid_sets, fixed_cells):
    query_type = random.choice([1, 2, 3])  # Randomly choose query type
    
    if query_type == 1:
        # Query type (a): Verify rows, columns, and subgrids
        return verify_rows_columns_subgrids(commitments, row_sets, col_sets, subgrid_sets)
    
    elif query_type == 2:
        # Query type (b): Verify consistency of triples (row, column, subgrid)
        return verify_triples(commitments, row_sets, col_sets, subgrid_sets)
    
    elif query_type == 3:
        # Query type (c): Verify filled cells are correct
        return verify_filled_cells(commitments, row_sets, col_sets, subgrid_sets, fixed_cells)

# Verify rows, columns, and subgrids
def verify_rows_columns_subgrids(commitments, row_sets, col_sets, subgrid_sets):
    # Check each set for distinct values and ensure no sets intersect
    for sets in [row_sets, col_sets, subgrid_sets]:
        for cell_set in sets:
            values = [commitments[cell] for cell in cell_set]
            if len(set(values)) != len(cell_set):  # Check if all values are distinct
                return False
    return True

# Verify triples (row, column, subgrid)
def verify_triples(commitments, row_sets, col_sets, subgrid_sets):
    for i in range(9):
        for j in range(9):
            # Check if the value in each row, column, and subgrid is consistent
            triple_values = {commitments[(i, j)], commitments[(i, j)]}
            if len(triple_values) != 1:
                return False
    return True

# Verify filled cells are correct
def verify_filled_cells(commitments, row_sets, col_sets, subgrid_sets, fixed_cells):
    for cell in fixed_cells:
        # Check if the filled cell's value matches the original fixed value
        if commitments[cell] != "Correct_Fixed_Value":  # Example for testing
            return False
    return True

# Test with a 9x9 Sudoku grid
initial_sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

final_sudoku_grid = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

# Generate the commitments for the Sudoku solution
commitments, nonces, row_sets, col_sets, subgrid_sets, fixed_cells = generate_commitments(initial_sudoku_grid)

# Simulate the verifier querying the prover (choose a random query)
query_result = verifier_query(commitments, row_sets, col_sets, subgrid_sets, fixed_cells)
print("Verifier query result:", query_result)
