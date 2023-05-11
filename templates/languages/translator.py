#!/bin/python3
import os
import phonemizer

english_letters = [chr(code) for code in range(65, 91)] + [chr(code) for code in range(97, 123)]

letters_to_ascii = {}

for letter in english_letters:
    letters_to_ascii[letter] = ord(letter)
    
print(letters_to_ascii)

def ascii_convert(word):
    ascii_word = []
    for char in word:
        ascii_word.append(ord(char))
    return ascii_word
    
def get_phonemes(word, language='en-us'):
    phonemes = phonemizer.phonemize(word, language=language)
    return phonemes.split()

words = ['hello world', 'how are you?']
print(words)
for word in words:
    phonemes = get_phonemes(word)
    print(f'The phonetic representation of "{word}" is: {phonemes}')

for phoneme in phonemes:
    ascii_word = ascii_convert(phoneme)
    print(ascii_word)
    
words_of_all_sounds = ['sheep', 'ship', 'good', 'shoot', 'here', 'wait', 'bed', 'teacher', 'bird', 'door', 'tourist', 'boy', 'show', 'cat', 'up', 'far', 'on', 'hair', 'my', 'cow', 'pea', 'boat', 'tea', 'dog', 'cheese', 'june', 'car', 'go', 'fly', 'video', 'think', 'thy', 'see', 'zoo', 'shall', 'television', 'man', 'now', 'sing', 'hat', 'love', 'red', 'wet', 'yes']

# Get all possible phonemes for each character in the alphabet
for word in words_of_all_sounds:
    phoneme_word = get_phonemes(word)
    for phoneme in phoneme_word:
        ascii_chars = ascii_convert(phoneme)        
        print(f"{word}: {phoneme_word} -> {ascii_chars}")
