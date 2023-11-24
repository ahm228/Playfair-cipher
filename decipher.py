import re

def split_paragraph_into_sentences(paragraph):
    sentences = re.findall(r'[^.!?]*[.!?]', paragraph)
    return sentences

def toLowerCase(text):
    return text.lower()

def processTextForCipher(text):
    processed_text = ''
    non_alpha_chars = []
    for i, char in enumerate(text):
        if char.isalpha():
            processed_text += char
        else:
            non_alpha_chars.append((i, char))
    return processed_text, non_alpha_chars

def replaceZwithS(text):
    return text.replace('s', 'z')

def Diagraph(text):
    return [text[i:i+2] for i in range(0, len(text), 2)]

def generateKeyTable(word, alphabet):
    key_letters = ''.join(sorted(set(word), key=word.index))
    matrix = [list(key_letters + ''.join([c for c in alphabet if c not in key_letters]))[i:i + 5] for i in range(0, 25, 5)]
    return matrix

def search(mat, element):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == element:
                return i, j
    raise ValueError(f"Character {element} not found in matrix")

def decrypt_RowRule(matr, e1r, e1c, e2r, e2c):
    return matr[e1r][(e1c-1)%5], matr[e2r][(e2c-1)%5]

def decrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
    return matr[(e1r-1)%5][e1c], matr[(e2r-1)%5][e2c]

def decrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    return matr[e1r][e2c], matr[e2r][e1c]

def decryptByPlayfairCipher(Matrix, cipherText, non_alpha_chars):
    PlainText = []
    processed_pairs = Diagraph(cipherText)

    for pair in processed_pairs:
        if len(pair) == 2:
            e1r, e1c = search(Matrix, pair[0])
            e2r, e2c = search(Matrix, pair[1])

            if e1r == e2r:
                p1, p2 = decrypt_RowRule(Matrix, e1r, e1c, e2r, e2c)
            elif e1c == e2c:
                p1, p2 = decrypt_ColumnRule(Matrix, e1r, e1c, e2r, e2c)
            else:
                p1, p2 = decrypt_RectangleRule(Matrix, e1r, e1c, e2r, e2c)

            PlainText.append(p1)
            PlainText.append(p2)
        else:
            PlainText.append(pair)

    PlainText = list("".join(PlainText))

    for pos, char in non_alpha_chars:
        PlainText.insert(pos, char)

    return "".join(PlainText)

# Main execution
cipherText = input("Ciphered Text: ")
sentences = split_paragraph_into_sentences(cipherText)

key = "icarus"
key = toLowerCase(key)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
Matrix = generateKeyTable(key, alphabet)

PlainTextList = []
for sentence in sentences:
    processed_sentence, non_alpha_chars = processTextForCipher(sentence)
    processed_sentence = toLowerCase(processed_sentence)
    processed_sentence = replaceZwithS(processed_sentence)
    decrypted_sentence = decryptByPlayfairCipher(Matrix, processed_sentence, non_alpha_chars)
    PlainTextList.append(decrypted_sentence)

PlainText = "".join(PlainTextList).upper()
print("Key text:", key.upper())
print("CipherText:", [sentence.upper() for sentence in sentences])
print("Plain Text:", PlainText)
