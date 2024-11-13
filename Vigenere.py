import math
import sys

letter_mappings = { 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
                    'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16,
                    'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24,
                    'y': 25, 'z': 26 }

# split input_text to groups (list of lists) based on key. For example if key = 3 will have 3 groups and in the first group will be char 1, 4, 7, etc
def split(key, input_text):
    n = len(input_text)     
    groups = [[] for _ in range(key)]
    for i in range(0, n):
        groups[i % key].append(input_text[i])
    return groups

# returns the index_of_coincidence of a text, given as a list of characters (text_list)
def index_of_coincidence(text_list, n):
    letter_freqs = {}
    
    for letter in text_list:
        if letter in letter_freqs:
            letter_freqs[letter] += 1
        else:
            letter_freqs[letter] = 1

    ic = 0
    for letter in letter_freqs:
        ic += (letter_freqs[letter] / n) * ((letter_freqs[letter] - 1) / (n - 1))
    
    return ic  

# takes a list of decrypted characters (each group that was split) and decrypts it because each group has been encrypted with Caesar
# Returns the shift which corresponds to a letter of the key.
def caesar_decrypt(group):
    letter_freqs = {}
    english_freqs =    {'a': 8.5, 'b': 2.07, 'c': 4.54, 'd': 3.38, 'e': 11.16, 'f': 1.81, 'g': 2.47, 'h': 3,
                        'i': 7.54, 'j': 0.2, 'k': 1.1, 'l': 5.49, 'm': 3.01, 'n': 6.65, 'o': 7.16, 'p': 3.17,
                        'q': 0.2, 'r': 7.58, 's': 5.74, 't': 6.95, 'u': 3.63, 'v': 1.01, 'w': 1.29, 'x': 0.29,
                        'y': 1.78, 'z': 0.27}

    # Convert all letters to lowercase for processing
    group = [char.lower() for char in group]

    for letter in group:
        if letter in letter_freqs:
            letter_freqs[letter] += 1
        else:
            letter_freqs[letter] = 1
    
    def shift(letter_freqs, n):
        shifted_freqs = {}
        for letter, frequency in letter_freqs.items():
            shifted_letter = chr(((ord(letter) - ord('a') + n) % 26) + ord('a'))
            shifted_freqs[shifted_letter] = frequency
        
        return shifted_freqs
    
    min_entropy = 2**10
    n = 0
    for i in range(1, 26):
        shifted_by_n_freqs = shift(letter_freqs, i)
        current_entropy = 0
        for letter in shifted_by_n_freqs:
            current_entropy += (shifted_by_n_freqs[letter] / len(group)) * math.log10(english_freqs[letter])
        current_entropy *= -1
        if current_entropy < min_entropy:
            min_entropy = current_entropy
            n = i

    c = group[0]
    p = chr(((ord(group[0]) - ord('a') + n) % 26) + ord('a'))

    key_char_map = (letter_mappings[c] - letter_mappings[p]) % 26
    key_char = chr(ord('a') + key_char_map)
        
    return key_char

# receives an input_file and does the decryption. It outputs 5 possible plaintexts with keys and ics
def vigenere_decrypt(input_file):
    # whole input text. with commas etc
    input_text = []

    # input text but only letters
    input_text_letters = []

    try:
        file = open(input_file, 'r')
        input_text = list(file.read())
        # list of letters of input text
        input_text_letters = [char.lower() for char in input_text if char.isalpha()]
    finally:
        file.close()

    key = 2
    n = len(input_text_letters)
    groups = []
    ic_counter = 0
    while ic_counter < 5:
        decrypted_text = []
        mean_ic = 0

        groups = split(key, input_text_letters)
        for group in groups:
            if len(group) > 1:
                mean_ic += index_of_coincidence(group, len(group))
        
        mean_ic /= key

        if mean_ic >= 0.06 and mean_ic <= 0.07:     
            vigenere_key = ""
            for group in groups:
                vigenere_key += caesar_decrypt(group)

            key_counter = 0
            for i in range (0, len(input_text)):
                if key_counter == len(vigenere_key):
                    key_counter = 0
                if input_text[i].isalpha():
                    decrypted_text.append(chr((letter_mappings[input_text[i].lower()] - letter_mappings[vigenere_key[key_counter]]) % 26 + ord('a')))
                    key_counter += 1
                else:
                    decrypted_text.append(input_text[i])

            print()
            decrypted_text_str = ''.join(decrypted_text)
            print(vigenere_key + '\n\n' + decrypted_text_str + '\n')
            print(mean_ic)
            print("-----------------------------------------------------------------------------------------")
            ic_counter += 1

        key += 1
        if (key == n):
            break

input_file = sys.argv[1]
vigenere_decrypt(input_file)

