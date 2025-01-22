from py_ecc.optimized_bn128 import G1, G2, add, multiply, pairing
from py_ecc.optimized_bn128 import field_modulus as q
import hashlib
import random




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