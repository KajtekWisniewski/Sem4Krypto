def xor_encrypt(data, key):
    """ Encrypts/decrypts data using XOR with a repeating key. """
    encrypted = bytearray(data)
    for i in range(len(encrypted)):
        encrypted[i] ^= key[i % len(key)]
    return bytes(encrypted)

def ecb_mode(data, key, block_size=16):
    """ Encrypt data using Electronic Codebook (ECB) mode. """
    encrypted = bytearray()
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        if len(block) < block_size:
            block += bytes([0] * (block_size - len(block)))  # Padding with zeros
        encrypted += xor_encrypt(block, key)
    return bytes(encrypted)

def cbc_mode(data, key, iv, block_size=16):
    """ Encrypt data using Cipher Block Chaining (CBC) mode. """
    encrypted = bytearray()
    previous_block = iv
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        if len(block) < block_size:
            block += bytes([0] * (block_size - len(block)))  # Padding with zeros
        block = bytes([x ^ y for x, y in zip(block, previous_block)])
        encrypted_block = xor_encrypt(block, key)
        encrypted += encrypted_block
        previous_block = encrypted_block
    return bytes(encrypted)

def encrypt_bmp(filename, key, mode='ECB', iv=None):
    """ Encrypt a BMP image file using specified mode (ECB or CBC) and save with an appropriate name. """
    with open(filename, 'rb') as file:
        bmp_header = file.read(54)  # Read the BMP header
        image_data = file.read()    # Read the actual image data

    output_filename = ''
    if mode == 'ECB':
        encrypted_data = ecb_mode(image_data, key)
        output_filename = 'ecb.bmp'
    elif mode == 'CBC':
        if iv is None:
            raise ValueError("IV is required for CBC mode")
        encrypted_data = cbc_mode(image_data, key, iv)
        output_filename = 'cbc.bmp'

    encrypted_bmp = bmp_header + encrypted_data

    with open(output_filename, 'wb') as file:
        file.write(encrypted_bmp)
    print(f"File encrypted using {mode} mode and saved as {output_filename}")

# Example usage:
key = b'simplekey1234567'  # Example key (must match block size for real AES)
iv = b'initialvector1234'  # Initial Vector for CBC mode

# Encrypt a BMP image in ECB mode
encrypt_bmp('plain.bmp', key, mode='ECB')

# Encrypt a BMP image in CBC mode
encrypt_bmp('plain.bmp', key, mode='CBC', iv=iv)
