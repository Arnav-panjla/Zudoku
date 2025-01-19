from py_ecc.optimized_bn128 import G1, G2, add, multiply, pairing
from py_ecc.optimized_bn128 import field_modulus as q
import hashlib
import random




def verify(commitment, value, random_value):
    """
    Verify the Pedersen commitment corresponds to the value and random value.
    
    :param commitment: The commitment point to verify
    :param value: The value to check the commitment against
    :param random_value: The random value (blinding factor) used in the commitment
    :return: True if the commitment corresponds to the value, False otherwise
    """
    expected_commitment = add(multiply(G1, random_value), multiply(H, value))
    return commitment == expected_commitment
