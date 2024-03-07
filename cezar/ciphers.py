import string

class Ciphers:
    def __init__(self):
        self.lowercase = list(string.ascii_lowercase)
        self.uppercase = list(string.ascii_uppercase)
        self.m = 26

    def encrypt_cesar(self, key, plaintext):
        ciphertext = ''
        for char in plaintext:
            if char.isalpha(): 
                if char.islower():
                    encrypted_char = self.lowercase[(self.lowercase.index(char) + key) % self.m]
                else:
                    encrypted_char = self.uppercase[(self.uppercase.index(char) + key) % self.m]
            else:
                encrypted_char = char
            ciphertext += encrypted_char
        return ciphertext

    def decrypt_cesar(self, key, ciphertext):
        plaintext = ''
        for char in ciphertext:
            if char.isalpha():
                if char.islower():
                    decrypted_char = self.lowercase[(self.lowercase.index(char) - key) % self.m]
                else:
                    decrypted_char = self.uppercase[(self.uppercase.index(char) - key) % self.m]
            else:
                decrypted_char = char
            plaintext += decrypted_char
        return plaintext
    
    def encrypt_file_cesar(self, input_file="plain.txt", output_file="crypto.txt", key_file="key.txt"):
        with open(key_file, 'r') as file:
            key = int(file.readline().split()[0])
            if not (1 <= key <= 25):
                print("klucz musi byc z zakresu liczb miedzy 1 a 25")
            else:
                with open(input_file, 'r') as file:
                    plaintext = file.readline().strip()

                encrypted_text = self.encrypt_cesar(key, plaintext)
                with open(output_file, 'w') as file:
                    file.write(encrypted_text)
                    print("Tekst zaszyfrowany cezarem i zapisany do pliku ")
    
    def decrypt_file_cesar(self, input_file="crypto.txt", output_file="decrypt.txt", key_file="key.txt"):
        with open(key_file, 'r') as file:
            key = int(file.readline().split()[0])
            if not (1 <= key <= 25):
                print("klucz musi byc z zakresu liczb miedzy 1 a 25")
            else:
                with open(input_file, 'r') as file:
                    plaintext = file.readline().strip()

                decrypted_text = self.decrypt_cesar(key, plaintext)
                with open(output_file, 'w') as file:
                    file.write(decrypted_text)
                    print("Tekst odszyfrowany cezarem i zapisany do pliku ")
    
    def brute_force_decrypt_cesar(self, input_file="crypto.txt", output_file="decrypt.txt"):
        with open(input_file, 'r') as file:
                    ciphertext = file.readline().strip()
        with open(output_file, 'w') as file:
            for key in range(1, 26):  # Try all possible keys
                decrypted_text = self.decrypt_cesar(key, ciphertext)
                file.write(f"klucz: {key}\n{decrypted_text}\n")
        print("kryptoanaliza wyłącznie w oparciu o kryptogram przeprowadzona dla szyfru cezara")
    
    def text_force_decrypt_cesar(self, known_plaintext_file="extra.txt", input_file="crypto.txt", output_file="decrypt.txt", key_output_file="key-found.txt"):
        found_key = None
        with open(known_plaintext_file, 'r') as file:
                    known_plaintext = file.readline().strip()
        with open(input_file, 'r') as file:
                    ciphertext = file.readline().strip()
        with open(output_file, 'w') as file:
            for key in range(1, 26):
                decrypted_text = self.decrypt_cesar(key, ciphertext)
                if known_plaintext in decrypted_text:
                    found_key = key
                    with open(key_output_file, 'w') as file:
                        file.write(f"{key}")
                    with open(output_file, 'w') as file:
                        file.write(f"{decrypted_text}")
                    break
        if found_key is None:
            print("Nie udalo sie obliczyc klucza")
        print("kryptoanaliza kryptoanaliza z tekstem jawnym przeprowadzona dla szyfru cezara")
    
    def NWD(self, a, b):
        if b == 0:
            return a
        return self.NWD(b, a % b)
    
    def multiplicative_inverse(self, a):
        for i in range(1, 26):
            if (a * i) % 26 == 1:
                return i
        return None 
    
    def encrypt_affine(self, a, b, plaintext):
        ciphertext = ''
        for char in plaintext:
            if char.isalpha():
                if char.islower():
                    encrypted_char = self.lowercase[((a * self.lowercase.index(char)) + b) % self.m]
                else:
                    encrypted_char = self.uppercase[((a * self.uppercase.index(char)) + b) % self.m]
            else:
                encrypted_char = char
            ciphertext += encrypted_char
        return ciphertext

    def decrypt_affine(self, a, b, ciphertext):
        plaintext = ''
        a_inverse = self.multiplicative_inverse(a)
        #print(a_inverse)
        if a_inverse is None: # ponieważ nie można zakładać, że program odszyfrowujący otrzymuje tę odwrotność
            print("nie znaleziono odwrotnosci klucza 'a' nie jest on wiec odpowiednim kluczem do deszyfrowania.")
            return
        for char in ciphertext:
            if char.isalpha():
                if char.islower():
                    decrypted_char = self.lowercase[(a_inverse * (self.lowercase.index(char) - b)) % self.m]
                else:
                    decrypted_char = self.uppercase[(a_inverse * (self.uppercase.index(char) - b)) % self.m]
            else:
                decrypted_char = char
            plaintext += decrypted_char
        return plaintext

    def encrypt_file_affine(self, input_file="plain.txt", output_file="crypto.txt", key_file="key.txt"):
        with open(key_file, 'r') as file:
            a, b = map(int, file.readline().split())
            if not (1 <= a <= 25) or not (0 <= b <= 25):
                print("klucz musi byc z zakresu liczb miedzy 1 a 25")
            else:
                with open(input_file, 'r') as file:
                    plaintext = file.readline().strip()
                encrypted_text = self.encrypt_affine(a, b, plaintext)
                with open(output_file, 'w') as file:
                    file.write(encrypted_text)
                    print("Tekst zaszyfrowany afinicznym i zapisany do pliku ")

    def decrypt_file_affine(self, input_file="crypto.txt", output_file="decrypt.txt", key_file="key.txt"):
        with open(key_file, 'r') as file:
            a, b = map(int, file.readline().split())
            if not (1 <= a <= 25) or not (1 <= b <= 25):
                print("klucz musi byc z zakresu liczb miedzy 1 a 25")
            else:
                with open(input_file, 'r') as file:
                    ciphertext = file.readline().strip()
                decrypted_text = self.decrypt_affine(a, b, ciphertext)
                with open(output_file, 'w') as file:
                    if(decrypted_text != None):
                        file.write(decrypted_text)
                        print("Tekst odszyfrowany afinicznym i zapisany do pliku ")
    
    def brute_force_decrypt_affine(self, input_file="crypto.txt", output_file="decrypt.txt"):
        with open(input_file, 'r') as file:
                ciphertext = file.readline().strip()
        with open(output_file, 'w') as file:
            for a in range(1, 26):
                # if self.NWD(a, 26) != 1:
                #     continue  # pomijamy niewlasciwie klucze 'a'
                for b in range(1, 26):
                    decrypted_text = self.decrypt_affine(a, b, ciphertext)
                    file.write(f"klucz: a={a}, b={b}\n{decrypted_text}\n\n")
        print("kryptoanaliza wyłącznie w oparciu o kryptogram przeprowadzona dla szyfru afinicznego")
    
    def text_force_decrypt_affine(self, known_plaintext_file="extra.txt", input_file="crypto.txt", output_file="decrypt.txt", key_output_file="key-found.txt"):
        found_key_pair = None
        with open(known_plaintext_file, 'r') as file:
                    known_plaintext = file.readline().strip()
        with open(input_file, 'r') as file:
                    ciphertext = file.readline().strip()
        with open(output_file, 'w') as file:
            for a in range(1, 26):
                if self.NWD(a, 26) != 1:
                    continue  # pomijamy niewlasciwie klucze 'a'
                for b in range(26):
                    decrypted_text = self.decrypt_affine(a, b, ciphertext)
                    if known_plaintext in decrypted_text:
                        found_key_pair = (a, b)
                        with open(key_output_file, 'w') as file:
                            file.write(f"{str(found_key_pair)}")
                        with open(output_file, 'w') as file:
                            file.write(f"{decrypted_text}")
                        break
                # if found_key_pair is not None:
                #     break
        if found_key_pair is None:
            print("Nie znaleziono odpowiedniej pary kluczy.")
        print("kryptoanaliza z tekstem jawnym przeprowadzona dla szyfru afinicznego")


