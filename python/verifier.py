from py_ecc.optimized_bn128 import G1, G2, add, multiply, pairing
from py_ecc.optimized_bn128 import field_modulus as q
import hashlib
import random

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


def verify(commitment, random_value, value):
    """
    Verify the Pedersen commitment corresponds to the value and random value.
    
    :param commitment: The commitment point to verify
    :param value: The value to check the commitment against
    :param random_value: The random value (blinding factor) used in the commitment
    :return: True if the commitment corresponds to the value, False otherwise
    """
    # expected_commitment = add(multiply(G1, random_value), multiply(H, value))
    expected_commitment = value*random_value
    return commitment == expected_commitment

def verify_commitment1(commitments, random_data, commitments_value):
    """

    """

    for i in range(len(commitments)):
        if not verify(commitments[i], random_data[i], commitments_value[i]):
            return False

    return True

def verify_commitment1c(commitments, random_data1c, commitments_value1c):
    """

    """

    for i in range(len(commitments)):
        if commitments_value1c[i] is None:
            continue
        if not verify(commitments[i], random_data1c[i], commitments_value1c[i]):
            return False

    return True

def verify_commitment2(commitments, random_data, commitments_value):
    """

    """
    for i in range(len(commitments)):
        for j in range(3):
            if not verify(commitments[i][j], random_data[i], commitments_value[i][j]):
                return False
    return True

def verify_commitment3(commitments, random_data, commitments_value):
    """

    """
    for i in range(len(commitments)):
        for j in range(len(commitments[0])):
            for k in range(3):
                if not verify(commitments[i][j][k], random_data[i][j], commitments_value[i][j][k]):
                    # print("commitment: ", commitments[i][j], "random_data: ", random_data[i][j], "commitments_value: ", commitments_value[i][j])
                    return False
    return True

def verify_commitment4(commitments, random_data, commitments_value):
    """

    """
    for i in range(len(commitments)):
        for j in range(len(commitments[0])):
            if not verify(commitments[i][j], random_data[i][j], commitments_value[i][j]):
                return False
    return True

def verify_query_a(commitment1_value, commitment4_value):
    """
    
    
    """
    n  = len(commitment4_value)//3
    possible_values = [i for i in range(1, n+1)]
    for i in range(len(commitment4_value)):
        values_set = set()
        for j in range(len(commitment4_value[0])):
            index = commitment4_value[i][j]
            values_set.add(commitment1_value[index])
            if commitment1_value[index] not in possible_values:
                return False
        if len(values_set) != n:
            return False
    return True
def verify_query_b(commitment1_value, commitment2_value):
    """
    
    
    """
    n = len(commitment1_value)
    index_list = []
    for tup in commitment2_value:
        index0 = tup[0]
        index1 = tup[1]
        index2 = tup[2]
        index_list.append(index0)
        index_list.append(index1)
        index_list.append(index2)
        if commitment1_value[tup[0]] != commitment1_value[tup[1]]:
            return False
        if commitment1_value[tup[1]] != commitment1_value[tup[2]]:
            return False
        if commitment1_value[tup[0]] != commitment1_value[tup[2]]:
            return False
    if set(index_list) != set(range(len(commitment1_value))):
        return False

    return True


def verify_query_c(commitments1c_value, commitments2_value, commitments3_value, commitments4_value):
    """
    
    """
    # checking the consistency of predetermined values
    n = len(commitments4_value)//3
    empty_sudoku = initial_sudoku()
    for i in range(n):
        for j in range(n):
            cell = empty_sudoku[i][j]
            if cell != 0:
                indexes = commitments3_value[i][j]
                for idx in indexes:
                    if commitments1c_value[idx] != cell:
                        return False            
    return True

