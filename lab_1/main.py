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


def encrypt_cesar(array, shift):
    for i in range(len(array)):
        array[i] = chr((ord(array[i]) + shift) % 256)
    return array


input_characters = read_file('resources/input1.txt')
encrypted = encrypt_cesar(input_characters, 3)
print(encrypted)
decrypted = encrypt_cesar(encrypted, -3)

write_file('resources/output1.txt', decrypted)
