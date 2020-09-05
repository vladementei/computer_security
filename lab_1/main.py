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


def normalize_size(letter, is_caps):
    basis = 'A' if is_caps else 'a'
    return chr(((ord(letter) - ord(basis)) % 26) + ord(basis))


def vigenere_shift(letter, is_caps):
    return ord(letter) - ord('A' if is_caps else 'a')


def cesar(array, shift, enc=True):
    for i in range(len(array)):
        if is_letter(array[i]):
            is_caps = is_capital(array[i])
            array[i] = normalize_size(chr(ord(array[i]) + (shift if enc else -shift)), is_caps)
    return array


def vigenere(array, key, enc=True):
    key_length = len(key)
    key_list = list(map(lambda x: {'chr': x, 'is_capital': is_capital(x)}, key))
    for i in range(len(array)):
        if is_letter(array[i]):
            is_caps = is_capital(array[i])
            shift = vigenere_shift(key_list[i % key_length]['chr'], key_list[i % key_length]['is_capital'])
            array[i] = normalize_size(chr(ord(array[i]) + (shift if enc else -shift)), is_caps)
    return array


input_characters = read_file('resources/input1.txt')

# vigenere
# encrypted = vigenere(input_characters, 'moUsE')
# print(encrypted)
# decrypted = vigenere(encrypted, 'moUsE', False)
# print(decrypted)

# cesar
encrypted = cesar(input_characters, 3)
print(encrypted)
decrypted = cesar(encrypted, 3, False)
print(decrypted)
# write_file('resources/output1.txt', decrypted)
