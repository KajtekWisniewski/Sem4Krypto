import random

# Kajetan Wiśniewski grupa 1

def generate_s_box():
    """ Generate a random S-box for all byte values (0-255). """
    s_box = list(range(256))
    random.shuffle(s_box)
    return s_box

# Generate a static S-box for the sake of consistency in example runs
# For real applications, this should be kept secure and probably not generated in this manner
s_box = generate_s_box()

def simple_substitution(data):
    """ Substitute data using a simple hardcoded substitution box (S-box). """
    return bytearray(s_box[b] for b in data)

def simple_permutation(data):
    """ Permute data using a simple pattern (for the sake of example). """
    # This is a trivial permutation for educational purposes.
    permuted = bytearray(len(data))
    for i in range(len(data)):
        # This "permutation" doesn't actually change positions, replace this with real permutation logic in practice.
        permuted[i] = data[i]
    return permuted

def block_encrypt(data, key, block_size=16):
    """ A very simple block cipher that uses substitution and permutation. """
    if len(data) % block_size != 0:
        raise ValueError("Block size must evenly divide the data. Consider padding the data.")
    
    encrypted = bytearray()
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        # Substitute
        substituted = simple_substitution(block)
        # Permute
        permuted = simple_permutation(substituted)
        # XOR with the key as a simple form of mixing
        encrypted_block = bytearray(permuted[j] ^ key[j % len(key)] for j in range(block_size))
        encrypted.extend(encrypted_block)
    return bytes(encrypted)

# Rest of the code for ECB, CBC, and BMP handling remains the same

def encrypt_bmp(input_filename, output_filename, key, mode='ECB', iv=None):
    """ Encrypt a BMP file and save it. """
    with open(input_filename, 'rb') as file:
        bmp_header = file.read(54)  # BMP header is always the first 54 bytes
        image_data = file.read()

    if mode == 'ECB':
        encrypted_data = ecb_mode(image_data, key)
    elif mode == 'CBC':
        if iv is None:
            raise ValueError("IV is required for CBC mode")
        encrypted_data = cbc_mode(image_data, key, iv)

    with open(output_filename, 'wb') as file:
        file.write(bmp_header + encrypted_data)  # Write header unchanged, encrypted data follows

def ecb_mode(data, key, block_size=16):
    """ Encrypt data using Electronic Codebook (ECB) mode with the new block cipher. """
    data = data + bytes((block_size - len(data) % block_size) % block_size)  # Padding data
    encrypted = bytearray()
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        encrypted_block = block_encrypt(block, key, block_size)
        encrypted.extend(encrypted_block)
    return bytes(encrypted)

def cbc_mode(data, key, iv, block_size=16):
    """ Encrypt data using Cipher Block Chaining (CBC) mode with the new block cipher. """
    data = data + bytes((block_size - len(data) % block_size) % block_size)  # Padding data
    encrypted = bytearray()
    previous_block = iv
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        block = bytes(b ^ p for b, p in zip(block, previous_block))
        encrypted_block = block_encrypt(block, key, block_size)
        encrypted.extend(encrypted_block)
        previous_block = encrypted_block
    return bytes(encrypted)

# Example usage:
key = b'secretsecretsecr'  # AES key must be exactly 16, 24, or 32 bytes long
iv = b'initialvector567'  # IV must be exactly 16 bytes long for AES
encrypt_bmp('plain.bmp', 'ecb_encrypted2.bmp', key, mode='ECB')
encrypt_bmp('plain.bmp', 'cbc_encrypted2.bmp', key, mode='CBC', iv=iv)