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


input_characters = read_file('resources/input1.txt')

# vigenere
encrypted = vigenere(input_characters, 'moUsE')
print(encrypted)
decrypted = vigenere(encrypted, 'moUsE', False)
print(decrypted)

# cesar
encrypted = cesar(input_characters, 3)
print(encrypted)
decrypted = cesar(encrypted, 3, False)
print(decrypted)
# write_file('resources/output1.txt', decrypted)
