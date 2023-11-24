import re

def split_paragraph_into_sentences(paragraph):
    # Use regex to keep the punctuation with each sentence
    sentences = re.findall(r'[^.!?]*[.!?]', paragraph)
    return sentences

def toLowerCase(text):
    return text.lower()

def processTextForCipher(text):
    # Process alphabetic characters for cipher, keep others (including spaces) as is
    processed_text = ''
    non_alpha_chars = []
    for i, char in enumerate(text):
        if char.isalpha():
            processed_text += char
        else:
            non_alpha_chars.append((i, char))
    return processed_text, non_alpha_chars

def replaceZwithS(text):
    return text.replace('z', 's')

def Diagraph(text):
    # Do not add extra characters for odd length strings
    return [text[i:i+2] for i in range(0, len(text), 2)]

def generateKeyTable(word, alphabet):
    key_letters = ''.join(sorted(set(word), key=word.index))  # Removing duplicates
    matrix = [list(key_letters + ''.join([c for c in alphabet if c not in key_letters]))[i:i + 5] for i in range(0, 25, 5)]
    return matrix

def search(mat, element):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == element:
                return i, j
    raise ValueError(f"Character {element} not found in matrix")

def encrypt_RowRule(matr, e1r, e1c, e2r, e2c):
    return matr[e1r][(e1c+1)%5], matr[e2r][(e2c+1)%5]

def encrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
    return matr[(e1r+1)%5][e1c], matr[(e2r+1)%5][e2c]

def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    return matr[e1r][e2c], matr[e2r][e1c]

def encryptByPlayfairCipher(Matrix, plainText, non_alpha_chars):
    CipherText = []
    processed_pairs = Diagraph(plainText)

    # Process each pair and append to CipherText
    for pair in processed_pairs:
        if len(pair) == 2:
            e1r, e1c = search(Matrix, pair[0])
            e2r, e2c = search(Matrix, pair[1])

            if e1r == e2r:
                c1, c2 = encrypt_RowRule(Matrix, e1r, e1c, e2r, e2c)
            elif e1c == e2c:
                c1, c2 = encrypt_ColumnRule(Matrix, e1r, e1c, e2r, e2c)
            else:
                c1, c2 = encrypt_RectangleRule(Matrix, e1r, e1c, e2r, e2c)

            CipherText.append(c1)
            CipherText.append(c2)
        else:
            CipherText.append(pair)

    # Convert CipherText into a list of characters to easily insert non-alphabetic characters
    CipherText = list("".join(CipherText))

    # Insert non-alphabetic characters back into their original positions
    for pos, char in non_alpha_chars:
        CipherText.insert(pos, char)

    return "".join(CipherText)

# Main execution
paragraph = input("Plaintext: " )
sentences = split_paragraph_into_sentences(paragraph)

key = "icarus"
key = toLowerCase(key)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
Matrix = generateKeyTable(key, alphabet)

CipherTextList = []
for sentence in sentences:
    processed_sentence, non_alpha_chars = processTextForCipher(sentence)
    processed_sentence = toLowerCase(processed_sentence)
    processed_sentence = replaceZwithS(processed_sentence)
    encrypted_sentence = encryptByPlayfairCipher(Matrix, processed_sentence, non_alpha_chars)
    CipherTextList.append(encrypted_sentence)

CipherText = "".join(CipherTextList).upper()  # Convert the final cipher text to uppercase
print("Key text:", key.upper())  # Also convert key to uppercase for consistency
print("Plain Text:", [sentence.upper() for sentence in sentences])  # Convert each sentence to uppercase
print("CipherText:", CipherText)
