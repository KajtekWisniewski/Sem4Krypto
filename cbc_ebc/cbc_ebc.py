from PIL import Image
import numpy as np

def divide_into_blocks(img, block_size=(8, 8)):
    width, height = img.size
    padded_width = ((width - 1) // block_size[0] + 1) * block_size[0]
    padded_height = ((height - 1) // block_size[1] + 1) * block_size[1]
    padded_image = Image.new('L', (padded_width, padded_height))
    padded_image.paste(img, (0, 0))

    blocks = []
    for y in range(0, padded_height, block_size[1]):
        for x in range(0, padded_width, block_size[0]):
            block = padded_image.crop((x, y, x + block_size[0], y + block_size[1]))
            blocks.append(np.array(block))
    return blocks, (padded_width, padded_height)

def transform_block(block):
    # A simple deterministic transformation (e.g., rotating bits or using a simple hash)
    return np.rot90(block, k=np.sum(block) % 4)  # Rotate block based on sum of its pixels

def simulate_ecb_encryption(blocks):
    encrypted_blocks = [transform_block(block) for block in blocks]
    return encrypted_blocks

def simulate_cbc_encryption(blocks, iv):
    encrypted_blocks = []
    previous_block = iv
    for block in blocks:
        mixed_block = np.bitwise_xor(block, previous_block)
        # A stronger mix using rotation and bitwise operations
        mixed_block = np.rot90(mixed_block, k=np.sum(mixed_block) % 4)
        mixed_block = np.bitwise_xor(mixed_block, np.roll(mixed_block, shift=1, axis=1))
        encrypted_blocks.append(mixed_block)
        previous_block = mixed_block
    return encrypted_blocks

def blocks_to_image(blocks, image_size):
    image = Image.new('L', image_size)
    index = 0
    for y in range(0, image_size[1], 8):
        for x in range(0, image_size[0], 8):
            block = Image.fromarray(blocks[index])
            image.paste(block, (x, y))
            index += 1
    return image

plain_image_path = 'plain.bmp'
plain_image = Image.open(plain_image_path)
blocks, padded_size = divide_into_blocks(plain_image)
iv = np.zeros((8, 8), dtype=np.uint8)  # Simple initial vector

ecb_encrypted_blocks = simulate_ecb_encryption(blocks)
cbc_encrypted_blocks = simulate_cbc_encryption(blocks, iv)

ecb_image = blocks_to_image(ecb_encrypted_blocks, padded_size)
cbc_image = blocks_to_image(cbc_encrypted_blocks, padded_size)

ecb_image.save('ecb_crypto_simulated.bmp')
cbc_image.save('cbc_crypto_simulated.bmp')
