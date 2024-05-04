
import sys
import random

def read_input(filename):
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        
    n = int(lines[0])
    exponents = [int(line) for line in lines[1:]] if len(lines) > 1 else []
    
    return n, exponents

def fermat_test(n):
    if n <= 1:
        return "certainly complex"
    if n <= 3:
        return "probably the first"
    if n % 2 == 0:
        return "certainly complex"
    
    if pow(2, n-1, n) == 1:
        return "probably the first"
    else:
        return "certainly complex"

def rabin_miller_witness(test, n):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    x = pow(test, d, n)
    if x == 1 or x == n - 1:
        return False

    for _ in range(s - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return False

    return True

def rabin_miller_test(n, k=5):
    if n <= 1:
        return "certainly complex"
    if n <= 3:
        return "probably the first"
    if n % 2 == 0:
        return str(n // 2)

    for _ in range(k):
        test = random.randrange(2, n - 2)
        if rabin_miller_witness(test, n):
            return "certainly complex"

    return "probably the first"

def write_output(filename, result):
    with open(filename, 'w') as file:
        file.write(result)

def main():
    test_type = 'rabin-miller'
    if len(sys.argv) > 1 and sys.argv[1] == '-f':
        test_type = 'fermat'

    n, exponents = read_input("input.txt")
    
    if test_type == 'fermat':
        result = fermat_test(n)
    else:
        result = rabin_miller_test(n)

    write_output("output.txt", result)

main()  # Uncomment this line to run the program
