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
                crypto_text('c')
            else:
                crypto_no_text('c')
        else:
            if sys.argv[2] == '-e':
                encoder('a')
            elif sys.argv[2] == '-d':
                decoder('a')
            elif sys.argv[2] == '-j':
                crypto_text('a')
            else:
                crypto_no_text('a')


def encoder(arg):
    origin = read_file('plain.txt')
    line = read_file('key.txt').split()
    a = get_affine_keys(line)[0]
    b = get_affine_keys(line)[1]
    text = origin.lower()
    new_text = ''
    for el in text:
        if ord(el) > 96 & ord(el) < 123:
            if arg == 'c':
                new_text += chr((ord(el) - ord('a') + b) % 26 + ord('a'))
            else:
                new_text += chr(((ord(el) - ord('a')) * a + b) % 26 + ord('a'))
        else:
            new_text += el
    write_file('crypto.txt', change_letters(new_text, origin))
    print('Encryption ready')


def decoder(arg):
    origin = read_file('crypto.txt')
    line = read_file('key.txt').split()
    a = get_affine_keys(line)[0]
    b = get_affine_keys(line)[1]
    text = origin.lower()
    new_text = ''
    for el in text:
        if ord(el) > 96 & ord(el) < 123:
            if arg == 'c':
                new_text += chr((ord(el) - ord('a') - b) % 26 + ord('a'))
            else:
                new_text += chr(pow(a, -1, 26) * (ord(el) - ord('a') - b) % 26 + ord('a'))
        else:
            new_text += el
    write_file('decrypt.txt', change_letters(new_text, origin))
    print('Decryption ready')


def crypto_text(arg):
    origin = read_file('crypto.txt')
    crypto = origin.lower()
    example = read_file('extra.txt')
    if not example[0].isalpha():
        print('Could not calculate the key')
    key = (ord(crypto[0]) - ord(example[0].lower())) % 26
    a = calc_key(crypto, example)[1]
    b = calc_key(crypto, example)[0]
    new_text = ''
    for el in crypto:
        if ord(el) > 96 & ord(el) < 123:
            if arg == 'c':
                new_text += chr((ord(el) - ord('a') - key) % 26 + ord('a'))
            else:
                new_text += chr(pow(a, -1, 26) * (ord(el) - ord('a') - b) % 26 + ord('a'))
        else:
            new_text += el
    write_file('decrypt.txt', change_letters(new_text, origin))
    if arg == 'c':
        write_file('key_found.txt', str(key))
    else:
        write_file('key_found.txt', ' '.join([str(b), str(a)]))
    print('Decryption ready')



def crypto_no_text(arg):
    origin = read_file('crypto.txt')
    text = origin.lower()
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
            possibilities.append(change_letters(possibility, origin))
    else:
        for a in a_s:
            for b in range(0, 26):
                possibility = ''
                for el in text:
                    if ord(el) > 96 & ord(el) < 123:
                        possibility += chr(pow(a, -1, 26) * (ord(el) - ord('a') - b) % 26 + ord('a'))
                    else:
                        possibility += el
                possibilities.append(change_letters(possibility, origin))
    write_file('decrypt.txt', '\n'.join(possibilities))
    print('Brute force attack done')


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


def write_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)


def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print('Input file not found')


def get_affine_keys(line):
    b = int(line[0])
    a = int(line[1])
    if b > 25 | b < 0:
        print('Error: wrong key')
    elif a not in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
        print('Error: wrong argument')
    return a, b


def change_letters(text, source):
    new_text = ''
    for i in range(0, len(text)):
        if source[i].isalpha() and source[i].isupper():
            new_text += text[i].upper()
        else:
            new_text += text[i]
    return new_text


input_reader()
