def hashIt(plaintext):
    counter = ''
    for char in range(len(plaintext)):
        # print(f'ordinalValue: {ord(plaintext[char])}')
        # print(plaintext.index(plaintext[char]))
        ordinalValue = ord(plaintext[char]) ** (char + 1)
        binaryValue = bin(ordinalValue)[2:]
        counter += str(binaryValue)[2:]
        # print(f'character: {plaintext[char]}\nordinalValue: {ordinalValue}\nbinaryValue: {binaryValue}')

    # print(f'counter: {counter}')
    hashed = ''
    for i in range(0, len(counter), 7):
        # print(counter[i:i + 7])
        temp = int(counter[i:i + 7])
        # print(f'temp: {temp}')

        decimal, i = 0, 0
        while temp != 0:
            dec = temp % 10
            # print(f'dec: {dec}')
            decimal = decimal + dec * pow(2, i)
            # print(f'decimal: {decimal}\n    dec * pow(2, i): {dec *pow(2, i)}')
            temp = temp // 10
            # print(f'new temp: {temp}')
            i += 1
        decimalData = decimal
        # print(f'decimal data: {decimalData}')
        hashed = hashed + chr(decimalData)
    return hashed


# hashedWords = []
# word = input('Enter a word: ')
# while word != '':
#     encrypted = hashIt(word)
#     print(word)
#     print(encrypted)
#     if encrypted in hashedWords:
#         print('word found')
#     else:
#         hashedWords.append(encrypted)
#     print(hashedWords)
#     word = input('Enter a word: ')
