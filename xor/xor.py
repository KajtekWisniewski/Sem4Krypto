import argparse

def prepare_text(input_file):
    with open(input_file, 'r') as f:
        text = f.read()
    # Usuwamy znaki końca linii
    text = text.replace('\n', ' ')
    # Zamieniamy duże litery na małe
    text = text.lower()
    # Zapisujemy przygotowany tekst do pliku
    with open('orig.txt', 'w') as f:
        f.write(text)

def encrypt(plain_file, key_file):
    with open(plain_file, 'r') as f:
        plain_text = f.read()
    with open(key_file, 'r') as f:
        key = f.read()

    # Szyfrujemy tekst za pomocą operacji XOR
    encrypted_text = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(plain_text, key))

    # Zapisujemy zaszyfrowany tekst do pliku
    with open('crypto.txt', 'w') as f:
        f.write(encrypted_text)

def decrypt(crypto_file, key_file):
    with open(crypto_file, 'r') as f:
        encrypted_text = f.read()
    with open(key_file, 'r') as f:
        key = f.read()

    # Odszyfrowujemy tekst za pomocą operacji XOR
    decrypted_text = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(encrypted_text, key))

    # Zapisujemy odszyfrowany tekst do pliku
    with open('decrypt.txt', 'w') as f:
        f.write(decrypted_text)

def cryptoanalysis(crypto_file, plain_file):
    with open(crypto_file, 'r') as f:
        encrypted_text = f.readlines()

    with open(plain_file, 'r') as f:
        plain_text = f.read()

    # Inicjalizujemy listę do przechowywania odszyfrowanych tekstów
    decrypted_texts = []

    # Iterujemy przez wszystkie linijki zaszyfrowanego tekstu
    for line in encrypted_text:
        decrypted_text = ''
        # Iterujemy przez znaki zaszyfrowanego tekstu
        for i, char in enumerate(line):
            # Jeśli znak jest spacją, to zachowujemy spację
            if char == ' ':
                decrypted_text += ' '
            else:
                # W przeciwnym razie xorujemy znaną spację z zaszyfrowanym znakiem,
                # a następnie xorujemy wynik z literą tekstu jawnego na tej samej pozycji
                decrypted_char = chr(ord(' ') ^ ord(char) ^ ord(plain_text[i]))
                decrypted_text += decrypted_char
        # Dodajemy odszyfrowany tekst do listy
        decrypted_texts.append(decrypted_text)

    # Zapisujemy odszyfrowane teksty do pliku
    with open('decrypt.txt', 'w') as f:
        for text in decrypted_texts:
            f.write(text + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Program do szyfrowania i kryptoanalizy tekstu za pomocą operacji XOR.')
    parser.add_argument('-p', action='store_true', help='Przygotowanie tekstu do przykładu działania')
    parser.add_argument('-e', action='store_true', help='Szyfrowanie tekstu')
    parser.add_argument('-k', action='store_true', help='Kryptoanaliza wyłącznie w oparciu o kryptogram')
    args = parser.parse_args()

    if args.p:
        prepare_text('orig.txt')
    elif args.e:
        encrypt('plain.txt', 'key.txt')
    elif args.k:
        cryptoanalysis('crypto.txt', 'plain.txt')
    else:
        print("Nie wybrano żadnej opcji.")
