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


def encrypt(array):
    for i in range(len(array)):
        array[i] = chr((ord(array[i]) + 3) % 256)
    return array


def decrypt(array):
    for i in range(len(array)):
        array[i] = chr((ord(array[i]) - 3) % 256)
    return array


input_characters = read_file('resources/input1.txt')
encrypted = encrypt(input_characters)
decrypted = decrypt(encrypted)

write_file('resources/output1.txt', decrypted)
