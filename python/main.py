from py_ecc import bls

# Generate a private key and its corresponding public key
private_key = bls.PrivateKey.random()
public_key = private_key.get_public_key()

# Sign a message (hash the message first)
message = b"Hello, BLS12-381!"
message_hash = bls.hash_message(message)
signature = private_key.sign(message_hash)

# Verify the signature
is_valid = public_key.verify(message_hash, signature)
print("Signature is valid:", is_valid)
