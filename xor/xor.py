# Kajetan Wiśniewski

import math
import argparse
import re

def log_table(table):
  index_width = len(str(len(table[0])))

  for i, row in enumerate(table):
    row_padding = " " * (index_width - len(str(i + 1)))
    print(f"{row_padding}{i + 1}: ", end=" ")
    for element in row:
      print(f"{element}", end=" ")
    print()


def parse_ascii_char_to_binary(char):
  return bin(int(char))[2:].zfill(8)


def prepare(input_filename, output_filename):
  with open(input_filename, "r") as input_file:
    text = re.sub(r'[^a-zA-Z\s]', '', input_file.read().lower().replace("\n", ""))
    formatted_text = []
    for i in range (0, (math.ceil(len(text))), 64):
      formatted_text.append(text[i:i+64])
    
    formatted_text = '\n'.join(formatted_text)

    with open(output_filename, "w") as output_file:
      output_file.write(formatted_text)


def encrypt(plain_text_filename, key_filename, output_filename):
  with open(plain_text_filename, "r") as plain_text_file:
    plain_text = (
      plain_text_file.read().lower()
    ) 
  with open(key_filename, "r") as key_file:
    key = key_file.read().lower()

  encrypted_text = ""

  for line in plain_text.split('\n'):
    for a, b in zip(
      line,
      key[:len(line)],
    ):
      encrypted_text += (str(ord(a) ^ ord(b))) + "|"
    encrypted_text += "\n"

  with open(output_filename, "w") as output_file:
    output_file.write(encrypted_text.strip())


def cryptoanalysis(crypto_filename, output_filename):
  with open(crypto_filename, "r") as crypto_file:
    crypto_text = (
      crypto_file.read().lower()
    )

  crypto_lines = crypto_text.split('\n')

  for i in range (len(crypto_lines)):
    crypto_lines[i] = crypto_lines[i].strip('|').split('|')

  decrypted_lines = [['__' for i in range (64)] for j in range (len(crypto_lines))]
  
  key_width = 64
  number_of_lines = len(crypto_lines)
  cutoff_column_index = len(crypto_lines[number_of_lines - 1]) - 1
  
  for column_index in range (key_width):
    column_length = number_of_lines - 1 if column_index > cutoff_column_index else number_of_lines
    first_char = int(crypto_lines[0][column_index])
    second_char = int(crypto_lines[1][column_index])
    xor_result = parse_ascii_char_to_binary(first_char ^ second_char)

    if no_info(xor_result):
      space_index = find_space_scenario_1(column_index, column_length, crypto_lines)
      
    elif is_space(xor_result):
      space_index = find_space_scenario_2(column_index, column_length, crypto_lines)

    elif same_chars(xor_result):
      space_index = find_space_scenario_3(column_index, column_length, crypto_lines)

    if space_index != None:
      for i in range(column_length):
        decrypted_lines[i][column_index] = decrypt_letter(crypto_lines[i][column_index], crypto_lines[space_index][column_index])

      decrypted_lines[space_index][column_index] = " "

  decrypted_lines[len(decrypted_lines) - 1] = decrypted_lines[len(decrypted_lines) - 1][:cutoff_column_index + 1]
  log_table(decrypted_lines)

def find_space_scenario_1(column_index, column_length, crypto_lines):
  first_char = int(crypto_lines[0][column_index])
  for char_index in range (2, column_length):
    current_char = int(crypto_lines[char_index][column_index])
    xor_result = parse_ascii_char_to_binary(first_char ^ current_char)

    if is_space(xor_result):
      return char_index

  return None

def find_space_scenario_2(column_index, column_length, crypto_lines):
  first_char = int(crypto_lines[0][column_index])
  second_char = int(crypto_lines[1][column_index])
  
  for char_index in range (1, column_length):
    curr_char = int(crypto_lines[char_index][column_index])

    first_and_nth_element_xor_result = parse_ascii_char_to_binary(first_char ^ curr_char)
    second_and_nth_element_xor_result = parse_ascii_char_to_binary(second_char ^ curr_char)

    if no_info(first_and_nth_element_xor_result):
      return 1
    elif no_info(second_and_nth_element_xor_result):
      return 0
  
  return None

def find_space_scenario_3(column_index, column_length, crypto_lines):
  first_char = int(crypto_lines[0][column_index])
  space_char = None
  space_char_index = None

  for char_index in range (1, column_length):
    curr_char = int(crypto_lines[char_index][column_index])

    first_and_nth_element_xor_result = parse_ascii_char_to_binary(first_char ^ curr_char)

    if space_char == None and is_space(first_and_nth_element_xor_result):
      space_char_index = char_index
      space_char = int(crypto_lines[space_char_index][column_index])

    if space_char != None:
      space_and_nth_element_xor_result = parse_ascii_char_to_binary(space_char ^ curr_char)

      if no_info(first_and_nth_element_xor_result):
        return space_char_index

      elif no_info(space_and_nth_element_xor_result):
        return 0

  return None


def same_chars(xor_result):
  return xor_result == "00000000"


def is_space(xor_result):
  return xor_result[0:3] == "010"


def no_info(xor_result):
  return xor_result[0:3] != "010" and xor_result != "00000000"


def decrypt_letter(encrypted_letter, encrypted_space):
  decrypted_letter = chr((int(encrypted_letter) ^ int(encrypted_space)) ^ ord(" "))

  return decrypted_letter


def main():
  parser = argparse.ArgumentParser(
    description="XOR Encryption and Cryptanalysis Program"
  )
  parser.add_argument(
    "-p", "--prepare", action="store_true", help="Prepare text for analysis"
  )
  parser.add_argument(
    "-e", "--encrypt", action="store_true", help="Encrypt plain text"
  )
  parser.add_argument(
    "-k", "--analyze", action="store_true", help="Analyze crypto text"
  )
  args = parser.parse_args()

  if args.prepare:
    prepare("orig.txt", "plain.txt")
  elif args.encrypt:
    encrypt("plain.txt", "key.txt", "crypto.txt")
  elif args.analyze:
    cryptoanalysis("crypto.txt", "decrypt.txt")
    pass


if __name__ == "__main__":
  main()
