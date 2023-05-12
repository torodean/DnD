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
    phon = phonemizer.phonemize(word, language=language)
    return phon.split()


words = ['hello world', 'how are you?']
print(words)
for word in words:
    phonemes = get_phonemes(word)
    print(f'The phonetic representation of "{word}" is: {phonemes}')

for phoneme in phonemes:
    ascii_word = ascii_convert(phoneme)
    print(ascii_word)

words_of_all_sounds = ['pit', 'tab', 'dill', 'bill', 'kill', 'mill', 'fill', 'gill', 'seal', 'real', 'zeal', 'veal',
                       'heal', 'leaf', 'nil', 'witch', 'shill', 'chill', 'thin', 'thy', 'ring', 'jog', 'you', 'beige',
                       'butt', 'foot', 'bat', 'bout', 'bore', 'bite', 'boy', 'never', 'beet', 'boot', 'sofa', 'bait',
                       'pot', 'bit', 'bet', 'boat',
                       'sheep', 'ship', 'good', 'shoot', 'here', 'wait', 'bed', 'teacher', 'bird', 'door', 'tourist',
                       'boy', 'show', 'cat', 'up', 'far', 'on', 'hair', 'my', 'cow', 'pea', 'boat', 'tea', 'dog',
                       'cheese', 'june', 'car', 'go', 'fly', 'video', 'think', 'thy', 'see', 'zoo', 'shall',
                       'television', 'man', 'now', 'sing', 'hat', 'love', 'red', 'wet', 'yes', 'Worcestershire',
                       'Colonel', 'Phenomenon', 'Synecdoche', 'Chiaroscurist', 'Omphaloskepsis', 'Ecclesiastical',
                       'Entrepreneurial', 'Schadenfreude', 'Quixotic', 'Xylophone', 'Discombobulate',
                       'Pneumonoultramicroscopicsilicovolcanoconiosis', 'Squirrel', 'Onomatopoeia',
                       'Supercalifragilisticexpialidocious', 'Antidisestablishmentarianism', 'Colloquialism',
                       'Heterogeneous', 'Hyperbole', 'Hieroglyphics', 'Psychophysicotherapeutics', 'Pterodactyl',
                       'Esoteric', 'Otorhinolaryngology', 'Sphygmomanometer', 'Triskaidekaphobia', 'Obfuscate',
                       'Dichotomy', 'Anemone', 'Inchoate', 'Calliope', 'Archipelago', 'Macabre', 'Enervate',
                       'Pizzicato', 'Cacophony', 'Worcestershire sauce', 'Aphorism', 'Sesquipedalian']

phoneme_char_to_ascii = {}

# Get all possible phonemes for each character in the alphabet
for word in words_of_all_sounds:
    phoneme_word = get_phonemes(word)
    for phoneme in phoneme_word:
        ascii_chars = ascii_convert(phoneme)
        print(f"{word}: {phoneme_word} -> {ascii_chars}")
        combined_char = ''
        for index, char in enumerate(phoneme):
            # check if the index is not out of bounds
            if index < len(phoneme) - 1:
                # check if the next character is a stress marker
                if phoneme[index + 1] == 'ː':
                    # print(f"stress marker detected!")
                    # combine the current character with the stress marker
                    combined_char = char + 'ː'
                    continue
                # Skip the stress marker.
                if char == 'ː':
                    continue
            # add the character to the dictionary with its corresponding ASCII value
            if combined_char and combined_char not in phoneme_char_to_ascii:
                phoneme_char_to_ascii[combined_char] = [ascii_convert(combined_char)[0], ascii_chars[index]]
                print(f"added combined character {combined_char} with ASCII values {phoneme_char_to_ascii[combined_char]} to the dictionary")
                combined_char = ''
            if char not in phoneme_char_to_ascii:
                phoneme_char_to_ascii[char] = ascii_chars[index]
                print(f"added character {char} with ASCII value {ascii_chars[index]} to the dictionary")

print(phoneme_char_to_ascii)
print(len(phoneme_char_to_ascii))
