# pip install numpy
# pip install matplotlib
import math
import re
import numpy as np
from functools import reduce
from collections import Counter
import matplotlib.pyplot as plt

eng_frequencies = [
    {"letter": "a", "frequency": 0.08167},
    {"letter": "b", "frequency": 0.01492},
    {"letter": "c", "frequency": 0.02782},
    {"letter": "d", "frequency": 0.04253},
    {"letter": "e", "frequency": 0.12702},
    {"letter": "f", "frequency": 0.0228},
    {"letter": "g", "frequency": 0.02015},
    {"letter": "h", "frequency": 0.06094},
    {"letter": "i", "frequency": 0.06966},
    {"letter": "j", "frequency": 0.00153},
    {"letter": "k", "frequency": 0.00772},
    {"letter": "l", "frequency": 0.04025},
    {"letter": "m", "frequency": 0.02406},
    {"letter": "n", "frequency": 0.06749},
    {"letter": "o", "frequency": 0.07507},
    {"letter": "p", "frequency": 0.01929},
    {"letter": "q", "frequency": 0.00095},
    {"letter": "r", "frequency": 0.05987},
    {"letter": "s", "frequency": 0.06327},
    {"letter": "t", "frequency": 0.09056},
    {"letter": "u", "frequency": 0.02758},
    {"letter": "v", "frequency": 0.00978},
    {"letter": "w", "frequency": 0.0236},
    {"letter": "x", "frequency": 0.0015},
    {"letter": "y", "frequency": 0.01974},
    {"letter": "z", "frequency": 0.00074}
]


def find_gcd(array):
    x = reduce(math.gcd, array)
    return x


def read_file(path):
    file = open(path, 'r+', encoding='utf-8')
    characters = [elem for elem in file.read()]
    file.close()
    return characters


def write_file(path, content):
    file = open(path, "w", encoding='utf-8')
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
    for l in range(2, 20):
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
    counter = Counter(gsd_array)
    answer = next(iter(counter))
    # print('key len = ', answer, ' probability = ', counter[answer] / len(gsd_array))
    return answer


def get_text_frequencies(text):
    alphabet = list(map(lambda x: x['letter'], eng_frequencies))
    letters_repeat = dict.fromkeys(alphabet, 0.0)
    for letter in text:
        if letters_repeat.get(letter.lower()) is not None:
            letters_repeat[letter.lower()] += 1
    letters_num = sum(letters_repeat.values())
    for letter in letters_repeat:
        letters_repeat[letter] = letters_repeat[letter] / letters_num
    return letters_repeat


def find_key_shift(text):
    alphabet_frequencies = eng_frequencies
    text_frequencies = get_text_frequencies(text)
    shifts = {}
    for i in range(len(alphabet_frequencies)):
        absolute_val_array = np.abs(np.array(list(text_frequencies.values())) - alphabet_frequencies[i]['frequency'])
        smallest_difference_index = absolute_val_array.argmin()
        shifts[smallest_difference_index - i] = shifts.get(smallest_difference_index - i, 0) + 1
    max_num_shifts = max(shifts, key=lambda x: shifts[x])
    return max_num_shifts if max_num_shifts >= 0 else len(eng_frequencies) + max_num_shifts


def hack_vigenere(text):
    key_len = casisci("".join(text))
    key = []
    for i in range(key_len):
        shift = find_key_shift(text[i::key_len])
        key.append(chr(ord('a') + shift))
    return "".join(key)


def keys_equality(key1, key2):
    arr1 = [char for char in key1]
    arr2 = [char for char in key2]
    counter = 0
    for i in range(min(len(arr1), len(arr2))):
        if arr1[i] == arr2[i]:
            counter += 1
    return counter / max(len(arr1), len(arr2))


x = []
y = []
key = 'hjsiz'

for i in range(1, 11):
    input_characters = read_file('resources/input' + str(i) + '.txt')
    encrypted = vigenere(input_characters, key)
    write_file('resources/output' + str(i) + '.txt', encrypted)
    hacked_key = hack_vigenere(encrypted)
    x.append(len(input_characters))
    y.append(keys_equality(key, hacked_key))
    print(i)
    print('file len', len(input_characters))
    print('hacked key = ', hacked_key)
    print('equality = ', keys_equality(key, hacked_key))


plt.plot(x, y)
plt.xlabel('file len')
plt.ylabel('probability')
plt.title('File Len - Probability diagram')
plt.show()



# vigenere
# input_characters = read_file('resources/input' + str(i) + '.txt')
# encrypted = vigenere(input_characters, 'hjsiz')
# print(encrypted)
# print('key length = ', casisci("".join(encrypted)))
# decrypted = vigenere(encrypted, 'moUsE', False)
# print(decrypted)

# cesar
# encrypted = cesar(input_characters, 3)
# print(encrypted)
# decrypted = cesar(encrypted, 3, False)
# print(decrypted)
# write_file('resources/output1.txt', decrypted)
