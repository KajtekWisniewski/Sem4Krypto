import random

def is_prime(n, k=5):  # Number of iterations, higher means more accuracy
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def read_input(filepath):
    with open(filepath, 'r') as file:
        lines = file.read().split()
        n = int(lines[0])
        exp = None
        if len(lines) > 1:
            exp = int(lines[1])
        if len(lines) > 2:
            exp *= (int(lines[2]) - 1)
        return n, exp

def main(filepath, fermat_only=False):
    n, exp = read_input(filepath)
    if fermat_only:
        if pow(2, n-1, n) == 1:
            return "probably prime"
        else:
            return "certainly composite"
    else:
        if is_prime(n):
            return "probably prime"
        else:
            # Attempt to find a divisor if composite
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return i
            return "certainly composite"

if __name__ == "__main__":
    import sys
    option = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] == "-f" else None
    filepath = 'input.txt'
    result = main(filepath, fermat_only=(option == "-f"))
    with open('output.txt', 'w') as output_file:
        output_file.write(str(result))
