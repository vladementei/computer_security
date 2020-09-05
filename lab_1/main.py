import math
import re
from functools import reduce
from collections import Counter


def find_gcd(array):
    x = reduce(math.gcd, array)
    return x


def read_file(path):
    file = open(path, 'r+')
    characters = [elem for elem in file.read()]
    file.close()
    return characters


def write_file(path, content):
    file = open(path, "w")
    for elem in content:
        file.write(elem)
    file.close()


def is_letter(char):
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z'


def is_capital(letter):
    return 'A' <= letter <= 'Z'


def get_basis(is_caps):
    return 'A' if is_caps else 'a'


def normalize_size(letter, is_caps):
    basis = get_basis(is_caps)
    return chr(((ord(letter) - ord(basis)) % 26) + ord(basis))


def vigenere_shift(letter, is_caps):
    return ord(letter) - ord(get_basis(is_caps))


def cesar(array, shift, enc=True):
    answer = []
    for i in range(len(array)):
        if is_letter(array[i]):
            is_caps = is_capital(array[i])
            answer.append(normalize_size(chr(ord(array[i]) + (shift if enc else -shift)), is_caps))
        else:
            answer.append(array[i])
    return answer


def vigenere(array, key, enc=True):
    key_length = len(key)
    key_list = list(map(lambda x: {'chr': x, 'is_caps': is_capital(x)}, key))
    answer = []
    for i in range(len(array)):
        if is_letter(array[i]):
            is_caps = is_capital(array[i])
            shift = vigenere_shift(key_list[i % key_length]['chr'], key_list[i % key_length]['is_caps'])
            answer.append(normalize_size(chr(ord(array[i]) + (shift if enc else -shift)), is_caps))
        else:
            answer.append(array[i])
    return answer


def casisci(text):
    text_length = len(text)
    text = text.lower()
    gsd_array = []
    for l in range(2, 10):
        for i in range(text_length - l + 1):
            search = text[i: i + l]
            positions = [token.start() for token in re.finditer(search, text)]
            if len(positions) > 1:
                distances = []
                for j in range(1, len(positions)):
                    distances.append(positions[j] - positions[j - 1])
                gcd = find_gcd(distances)
                if gcd > 1:
                    gsd_array.append(gcd)
                    # print(l, ' ', search, ' ', positions, ' ', distances, ' ', gcd)
    # print(sorted(gsd_array, key=gsd_array.count, reverse=True))
    # print(Counter(gsd_array))
    counter = Counter(gsd_array)
    answer = next(iter(counter))
    print('probability = ', counter[answer] / len(gsd_array))
    return answer


input_characters = read_file('resources/input1.txt')

# vigenere
encrypted = vigenere(input_characters, 'mouse')
# print(encrypted)
print('key length = ', casisci("".join(encrypted)))
# decrypted = vigenere(encrypted, 'moUsE', False)
# print(decrypted)

# cesar
encrypted = cesar(input_characters, 3)
# print(encrypted)
# decrypted = cesar(encrypted, 3, False)
# print(decrypted)
# write_file('resources/output1.txt', decrypted)
