import sys
from ciphers import Ciphers

cipherClass = Ciphers()

#Kajetan Wiśniewski grupa 1
#właściwia logika programu znajduje się w pliku klasy.py
#kod jest pisany w większości po angielsku za wyjątkiem komunikatów zwrotnych do użytkownika

if len(sys.argv) >= 2:
    if sys.argv[1] == '-c':
        print("wybrano szyfr cezara")
        if len(sys.argv) >= 3:
            match sys.argv[2]:
                case '-e':
                    cipherClass.encrypt_file_cesar()
                case '-d':
                    cipherClass.decrypt_file_cesar()
                case '-j':
                    cipherClass.text_force_decrypt_cesar()
                case '-k':
                    cipherClass.brute_force_decrypt_cesar()
                case _:
                    print("niewlasciwa flaga")
    if sys.argv[1] == '-a':
        print('wybrano szyfr afiniczny')
        if len(sys.argv) >= 3:
            match sys.argv[2]:
                case '-e':
                    cipherClass.encrypt_file_affine()
                case '-d':
                    cipherClass.decrypt_file_affine()
                case '-j':
                    cipherClass.text_force_decrypt_affine()
                case '-k':
                    cipherClass.brute_force_decrypt_affine()
                case _:
                    print("niewlasciwa flaga")

