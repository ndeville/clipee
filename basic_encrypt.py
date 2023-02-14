### 220922 WORKS - MOVED TO my_utils

from datetime import datetime
from operator import le
import os
print("----------")
ts_file = f"{datetime.now().strftime('%y%m%d-%H%M')}"
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"{ts_time} starting {os.path.basename(__file__)}")
import time
start_time = time.time()

import sys
sys.path.append("/Users/nic/Python/indeXee")
sys.path.append("/Users/nic/Python/Scrapee")

import pprint
pp = pprint.PrettyPrinter(indent=4)
print()
count = 0
count_row = 0

print(f"{os.path.basename(__file__)} boilerplate loaded -----------")
print()
####################
# Basic String Encryption

test = False

input_raw = 'string to encrypt'

offset = 2 # needs to be <26. 26 returns input_raw

index = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26,
}

def find_key(input_dict, value):
    for k, v in input_dict.items():
        if v == value:
            return k

def encrypt_with_offset(input,offset=2):
    input = input.lower().strip()
    if test:
        print(f"\nencrypt_with_offset {input=}\n")
    output = ''
    for letter in input:
        if letter == ' ':
            output = output + ' '
            continue
        if letter == ',':
            output = output + ','
            continue
        letter_index = index[letter]
        if test:
            print(f"{letter_index=}")
        if (letter_index + offset) > len(index):
            letter_index = letter_index - 26
        encrypted_letter = find_key(index, letter_index + offset)
        if test:
            print(letter, encrypted_letter)
        output = output + encrypted_letter
    if test:
        print(f"\n{output=}\n")
    return output

def decrypt_with_offset(input,offset=2):
    input = input.lower().strip()
    if test: 
        print(f"\ndecrypt_with_offset {input=}\n")
    output = ''
    for letter in input:
        if letter == ' ':
            output = output + ' '
            continue
        if letter == ',':
            output = output + ','
            continue
        letter_index = index[letter]
        if test:
            print(f"{letter_index=}")
        if (letter_index - offset) < 0:
            letter_index = letter_index + 26
        encrypted_letter = find_key(index, letter_index - offset)
        if test:
            print(letter, encrypted_letter)
        output = output + encrypted_letter
    if test:
        print(f"\n{output=}\n")
    return output

if test:

    encrypt_output = encrypt_with_offset(input_raw, offset)

    print(f"Encrypt: {repr(input_raw)}\toutput with offset {offset}: {repr(encrypt_output)}")
    print()
    print(f"Decrypt with offset {offset}: {repr(encrypt_output)}\toutput: {repr(decrypt_with_offset(encrypt_output, offset))}")



########################################################################################################

if __name__ == '__main__':
    print()
    print()
    print('-------------------------------')
    print(f"{os.path.basename(__file__)}")
    print()
    print(f"{count=}")
    print()
    print('-------------------------------')
    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    else:
        print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    print()