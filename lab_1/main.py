# pip install numpy
# pip install matplotlib
import math
import random
import re
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

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


def write_probabilities(path, content):
    file = open(path, "w", encoding='utf-8')
    for elem in content:
        file.write(str(elem))
        file.write('\n')
    file.close()


def read_probabilities(path):
    file = open(path, 'r+', encoding='utf-8')
    characters = [float(elem) for elem in file.readlines()]
    file.close()
    return characters


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


def gram_gcd(positions):
    distances = []
    for j in range(1, len(positions)):
        distances.append(positions[j] - positions[j - 1])
    # filtering random grams
    frequency = Counter(distances)
    leave_num = math.ceil(0.9 * len(frequency))  # change threshold
    frequency = frequency.most_common(leave_num)
    distances = [f[0] for f in frequency]
    # end
    gcd = find_gcd(distances)
    return gcd


def add_gsd(gcd_array, gcd):
    if gcd > 1:
        gcd_array.append(gcd)


def casisci(text):
    text_length = len(text)
    text = text.lower()
    gcd_array = []
    grams = {}
    for i in range(text_length - 1):
        search = text[i: i + 2]
        if grams.get(search) is None:
            positions = [token.start() for token in re.finditer(search, text)]
            if len(positions) > 2:  # or 1
                grams[search] = positions
                add_gsd(gcd_array, gram_gcd(positions))

    i = 0
    while i < len(grams.keys()):
        gram = list(grams.keys())[i]
        for pos in grams[gram]:
            search = text[pos: pos + len(gram) + 1]
            if grams.get(search) is None:
                positions = [token.start() for token in re.finditer(search, text)]
                if len(positions) > 2:  # or 1
                    grams[search] = positions
                    add_gsd(gcd_array, gram_gcd(positions))
        i += 1
    answer = max(set(gcd_array), key=gcd_array.count)
    return answer


def get_text_frequencies(text):
    alphabet = list(map(lambda x: x['letter'], eng_frequencies))
    letters_repeat = dict.fromkeys(alphabet, 0.0)
    for letter in text:
        if letters_repeat.get(letter.lower()) is not None:
            letters_repeat[letter.lower()] += 1
    letters_num = sum(letters_repeat.values())
    letters_num = letters_num if letters_num > 0 else 1
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


def perform_tests(num_tests):
    demo_keys = ['zx', 'ryh', 'gqpl', 'hjsiz', 'zqwerm', 'mpqzjga', 'qrtogdan', 'zxcvbnmlk', 'omqfvijktp',
                 'pkdajpiltwm']
    casisci_statistics = [[0 for i in range(num_tests)] for i in range(num_tests)]
    dz = [0 for i in range(num_tests * num_tests)]
    for text_iter in range(num_tests):
        input_characters = read_file('resources/big' + str(text_iter + 1) + '.txt')
        for cur_inter in range(num_tests):
            cur_key = demo_keys[cur_inter]
            for text_len in range(num_tests):
                rand_num = random.randint(0, len(input_characters) - (text_len + 1) * 1000)
                test_text = input_characters[rand_num: rand_num + (text_len + 1) * 1000]
                encrypted = vigenere(test_text, cur_key)
                hacked_key = hack_vigenere(encrypted)
                print('text ', text_iter + 1, ', len key ', len(cur_key), ', len text ', len(test_text))
                print('hacked key = ', hacked_key)
                print('equality = ', keys_equality(cur_key, hacked_key))
                dz[text_len * num_tests + len(cur_key) - len(demo_keys[0])] += ((hacked_key == cur_key) / num_tests)
                casisci_statistics[len(cur_key) - len(demo_keys[0])][text_len] += len(hacked_key) == len(cur_key)
    print('casisci tests statistics')
    for row in casisci_statistics:
        print(row)
    return dz


num_tests = 10
dz = perform_tests(num_tests)
write_probabilities('resources/probabilities.txt', dz)
# dz = read_probabilities('resources/probabilities.txt') построение на основе ранее полученных данных без перевычислений

xpos = []
ypos = []
zpos = []
dx = []
dy = np.ones(num_tests * num_tests)
for i in range(num_tests):
    for j in range(num_tests):
        xpos.append((i + 1) * 1000)
        ypos.append(j + 2)
        zpos.append(0)
        dx.append(1000)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('text len')
ax.set_ylabel('key len')
ax.set_zlabel('probability')
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
plt.margins(0)
plt.show()


# x = []
# y = []
# key = 'hjsiz'
#
# for i in range(1, 11):
#     input_characters = read_file('resources/input' + str(i) + '.txt')
#     encrypted = vigenere(input_characters, key)
#     write_file('resources/output' + str(i) + '.txt', encrypted)
#     hacked_key = hack_vigenere(encrypted)
#     x.append(len(input_characters))
#     y.append(keys_equality(key, hacked_key))
#     print(i)
#     print('file len = ', len(input_characters))
#     print('hacked key = ', hacked_key)
#     print('equality = ', keys_equality(key, hacked_key))
#
#
# plt.plot(x, y)
# plt.xlabel('file len')
# plt.ylabel('probability')
# plt.title('File Len - Probability diagram')
# plt.show()
#
# ##################################
#
# x = []
# y = []
# demo_keys = ['zx', 'ryh', 'gqpl', 'hjsiz', 'zqwerm', 'mpqzjga', 'qrtogdan', 'zxcvbnmlk', 'omqfvijktp', 'pkdajpiltwm']
#
# for i in range(0, 10):
#     input_characters = read_file('resources/input6.txt')
#     encrypted = vigenere(input_characters, demo_keys[i])
#     hacked_key = hack_vigenere(encrypted)
#     x.append(len(demo_keys[i]))
#     y.append(keys_equality(demo_keys[i], hacked_key))
#     print(i + 1)
#     print('key len = ', len(demo_keys[i]))
#     print('hacked key = ', hacked_key)
#     print('equality = ', keys_equality(demo_keys[i], hacked_key))
#
#
# plt.plot(x, y)
# plt.xlabel('key len')
# plt.ylabel('probability')
# plt.title('Key Len - Probability diagram')
# plt.show()


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
