#Kajetan Wiśniewski

pair = {
    "personaltxt": 'personal.txt',
    "personal_txt": 'personal_.txt'
}

hashes = ['md5sum', 'sha1sum', 'sha224sum', 'sha256sum', 'sha384sum', 'sha512sum', 'b2sum']

def hex_to_bin(hex_str):
    scale = 16 
    num_of_bits = len(hex_str) * 4
    bin_str = bin(int(hex_str, scale))[2:].zfill(num_of_bits)
    return bin_str

def compare_bits(bin_str1, bin_str2):
    length = min(len(bin_str1), len(bin_str2))
    equal_bits = sum(1 for a, b in zip(bin_str1[:length], bin_str2[:length]) if a == b)
    total_bits = length
    percentage = ((total_bits-equal_bits) / total_bits) * 100
    return equal_bits, total_bits, percentage

def read_hashes(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

def write_results(filename, results):
    with open(filename, 'w') as f:
        i = 0
        for result in results:
            f.write(f"cat hash-.pdf {pair['personaltxt']} | {hashes[i]}\n")
            f.write(f"cat hash-.pdf {pair['personal_txt']} | {hashes[i]}\n")
            f.write(f"{result['pair'][0]}\n")
            f.write(f"{result['pair'][1]}\n")
            i+=1
            f.write(f"Liczba rozniacych sie bitow: {result['total_bits']-result['equal_bits']} z {result['total_bits']}, procentowo ({result['percentage']:.2f}%)\n\n")

def main():
    hashes = read_hashes('hash.txt')
    results = []

    for i in range(0, len(hashes) - 1, 2):
        hash1 = hashes[i]
        hash2 = hashes[i + 1]
        bin_str1 = hex_to_bin(hash1)
        bin_str2 = hex_to_bin(hash2)

        equal_bits, total_bits, percentage = compare_bits(bin_str1, bin_str2)

        results.append({
            'pair': (hash1, hash2),
            'equal_bits': equal_bits,
            'total_bits': total_bits,
            'percentage': percentage
        })
    
    write_results('diff.txt', results)

if __name__ == "__main__":
    main()