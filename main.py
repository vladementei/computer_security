file = open('lab_1/resources/big.txt', 'r+', encoding='utf-8')
chars = [elem for elem in file.read()]
file.close()
chars = result = [a for a in chars if a not in {'(', ')', '?', '!', '*', '"', '“', '-', '—', '/', '\\', '[', ']'}]
for i in range(5):
    file = open('lab_1/resources/big' + str(i + 6) + '.txt', "w", encoding='utf-8')
    for elem in chars[int(i * len(chars) / 5): int((i + 1) * len(chars) / 5)]:
        file.write(elem)
    file.close()