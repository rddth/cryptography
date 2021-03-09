#########################################################################
# A simple program which works with Caesar's and affine ciphers, based on chosen options:
# first option: -c for Caesar's cipher, -a for affine cipher
# second option: -e for encoding, -d for decoding,
# -j for cryptanalysis with some given probe of a text, -k for cryptanalysis with neither the key nor the text probe.
# after choosing one from each category, the program performs the chosen operation and writes its input to a file.
#########################################################################
# Author: A. Ekalt
###########
import string
import sys

#for linear equations in finding affine cipher's key
import numpy as np


def input_reader():
    if len(sys.argv) < 3 or (sys.argv[1] != '-a' and sys.argv[1] != '-c') \
            or (sys.argv[2] != '-e' and sys.argv[2] != '-d' and sys.argv[2] != '-j' and sys.argv[2] != '-k'):
        print('Compile the file writing the following after the name caesars_affine.py: -c for Caesar\'s cipher '
              '\nor -a for affine cipher.' +
              '\nThen write -e for encryption or -d for decryption or -j for cryptanalysis with declared text' +
              '\nor -k for cryptanalysis without neither the text probe nor the key.')
    else:
        if sys.argv[1] == '-c':
            if sys.argv[2] == '-e':
                encoder('c')
            elif sys.argv[2] == '-d':
                decoder('c')
            elif sys.argv[2] == '-j':
                caesars_crypto_text()
            else:
                crypto_no_text('c')
        else:
            if sys.argv[2] == '-e':
                encoder('a')
            elif sys.argv[2] == '-d':
                decoder('a')
            elif sys.argv[2] == '-j':
                affine_crypto_text()
            else:
                crypto_no_text('a')


def encoder(arg):
    try:
        with open('plain.txt', 'r') as plain_file:
            text = plain_file.read()
        with open('key.txt', 'r') as key_file:
            line = key_file.read().split(' ')
            b = int(line[0])
            a = int(line[1])
            if b > 25 | b < 0:
                print('Error: wrong key')
            elif arg == 'a' and a not in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
                print('Error: wrong argument')
        text = text.lower()
        new_text = ''
        for el in text:
            if ord(el) > 96 & ord(el) < 123:
                if arg == 'c':
                    new_text += chr((ord(el) - ord('a') + b) % 26 + ord('a'))
                else:
                    new_text += chr(((ord(el) - ord('a')) * a + b) % 26 + ord('a'))
            else:
                new_text += el
        with open('crypto.txt', 'w') as encoded_file:
            encoded_file.write(new_text)
        print('Encryption ready')
    except FileNotFoundError:
        print('Input file/-s not found')


def decoder(arg):
    try:
        with open('crypto.txt', 'r') as encoded_file:
            text = encoded_file.read()
        with open('key.txt', 'r') as key_file:
            line = key_file.read().split(' ')
            b = int(line[0])
            a = int(line[1])
            if b > 25 | b < 0:
                print('Error: wrong key')
            elif arg == 'a' and a not in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
                print('Error: wrong argument')
        new_text = ''
        for el in text:
            if ord(el) > 96 & ord(el) < 123:
                if arg == 'c':
                    new_text += chr((ord(el) - ord('a') - b) % 26 + ord('a'))
                else:
                    new_text += chr(pow(a, -1, 26) * (ord(el) - ord('a') - b) % 26 + ord('a'))
            else:
                new_text += el
        with open('decrypt.txt', 'w') as plain_file:
            plain_file.write(new_text)
        print('Decryption ready')
    except FileNotFoundError:
        print('Input file/-s not found')


def caesars_crypto_text():
    try:
        with open('crypto.txt', 'r') as encoded_file:
            crypto = encoded_file.read()
        with open('extra.txt', 'r') as extra:
            example = extra.read()
        if ord(example) >= 123 | ord(example) < 97:
            print('Could not calculate the key')
        key = (ord(crypto[0][0]) - ord(example[0][0].lower())) % 26
        new_text = ''
        for el in crypto:
            if ord(el) > 96 & ord(el) < 123:
                new_text += chr((ord(el) - ord('a') - key) % 26 + ord('a'))
            else:
                new_text += el
        with open('decrypt.txt', 'w') as plain_file:
            plain_file.write(new_text)
        with open('key_found.txt', 'w') as key_file:
            key_file.write(str(key))
        print('Decryption ready')
    except FileNotFoundError:
        print('Input file/-s not found')


def crypto_no_text(arg):
    try:
        with open('crypto.txt', 'r') as encoded_file:
            text = encoded_file.read()
        possibilities = []
        a_s = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        if arg == 'c':
            for i in range(0, 26):
                possibility = ''
                for el in text:
                    if ord(el) > 96 & ord(el) < 123:
                        possibility += chr((ord(el) - ord('a') - i) % 26 + ord('a'))
                    else:
                        possibility += el
                possibilities.append(possibility)
        else:
            for a in a_s:
                for b in range(0, 26):
                    possibility = ''
                    for el in text:
                        if ord(el) > 96 & ord(el) < 123:
                            possibility += chr(pow(a, -1, 26) * (ord(el) - ord('a') - b) % 26 + ord('a'))
                        else:
                            possibility += el
                    possibilities.append(possibility)
        with open('decrypt.txt', 'w') as force_f:
            force_f.write('\n'.join(possibilities))
        print('Brute force attack done')
    except FileNotFoundError:
        print('Input file/-s not found')


def affine_crypto_text():
    with open('crypto.txt', 'r') as encoded_file:
        crypto = encoded_file.read()
    with open('extra.txt', 'r') as extra:
        example = extra.read()
    a = calc_key(crypto, example)[1]
    b = calc_key(crypto, example)[0]
    print(calc_key(crypto, example))
    new_text = ''
    for el in crypto:
        if ord(el) > 96 & ord(el) < 123:
            new_text += chr(pow(a, -1, 26) * (ord(el) - ord('a') - b) % 26 + ord('a'))
        else:
            new_text += el
    with open('key_found.txt', 'w') as key_file:
        key_file.write(' '.join([str(b), str(a)]))
    with open('decrypt.txt', 'w') as plain_file:
        plain_file.write(new_text)
    print('Decryption ready')


def get_letter(letter):
    return list(string.ascii_lowercase).index(letter)


def calc_key(crypto, extra):
    d_first = extra[0].lower()
    d_second = extra[1].lower()
    e_first = crypto[0]
    e_second = crypto[1]
    encrypted = (ord(e_first) - ord(e_second) + 26) % 26
    decrypted = (ord(d_first) - ord(d_second) + 26) % 26
    while (encrypted / decrypted) % 1 != 0:
        encrypted += 26
    key_a = int(encrypted / decrypted)
    key_b = int((get_letter(e_first) - ((get_letter(d_first) * key_a) % 26) + 26) % 26)
    return key_b, key_a


input_reader()

