from constants import *
from typing import TypeVar
from math import log10, gcd
from functools import reduce
from itertools import combinations
from random import shuffle, randint

T = TypeVar('T')
S = TypeVar('S')

def try_getting_dict_value(dictionary: dict[T, S], key: T, default: S) -> S:
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return default

def analyse_frequency(cipher_text: str) -> dict[str, float]:
    return {
        char: cipher_text.count(char) / len(cipher_text)
        for char in ENGLISH_ALPHABET
    }

def analyse_bigram(cipher_text: str) -> dict[str, float]:
    return {
        char: cipher_text.count(char) / len(cipher_text)
        for char in ENGLISH_BIGRAM_BY_COMMON
    }

def parse_frequencies(frequencies: dict[str, float]) -> str:
    frequencies_tmp: list[tuple[float, str]] = [
        (freq, char)
        for char, freq in frequencies.items()
    ]

    frequencies_tmp.sort(reverse=True)

    parsed: str = ""
    for _, char in frequencies_tmp:
        parsed += char
    
    return parsed

def compute_frequency_distance(frequency_1: dict[str, float], frequency_2: dict[str, float]) -> float:
    ret: float = 0
    for char in set(frequency_1.keys()).union(frequency_2.keys()):
        char_frequency_1: float = try_getting_dict_value(frequency_1, char, 0)
        char_frequency_2: float = try_getting_dict_value(frequency_2, char, 0)
        
        ret += (char_frequency_1 - char_frequency_2) ** 2
    
    return ret

def compute_frequency_score(text: str) -> float:
    return compute_frequency_distance(
        analyse_frequency(text), ENGLISH_LETTER_FREQUENCY
    )

def compute_bigram_score(text: str) -> float:
    return compute_frequency_distance(
        analyse_bigram(text), ENGLISH_BIGRAM_FREQUENCY
    )


def find_repeats(cipher_text: str, min_length: int | None = None) -> list[tuple[str, int, int]]:
    if not min_length:
        min_length = int(log10(len(cipher_text)) / log10(len(ENGLISH_ALPHABET))) + 3
    found: list[tuple[str, int, int]] = []
    for length in range(min_length, 2 * min_length):
        for box in range(len(cipher_text) - length):
            window: str = cipher_text[box: box + length]
            try:
                index: int = cipher_text.index(window, box + 1)
                found.append((window, box, index - box))
            except ValueError:
                pass
    
    return found

def count_words(text: str) -> int:
    words: int = 0
    for word in ENGLISH_WORDS:
        words += text.count(word)
    
    return words

def sanatize_cipher_text(cipher_text: str) -> str:
    cipher_text = cipher_text.lower()
    cipher_text = "".join([char for char in cipher_text if char in ENGLISH_ALPHABET])
    return cipher_text

def decrypt_ceaser(cipher_text: str, key: int) -> str:
    cipher_text = sanatize_cipher_text(cipher_text)
    plain_text: str = ""
    for char in cipher_text:
        char = char.lower()
        if char in ENGLISH_ALPHABET:
            char = ENGLISH_ALPHABET[(ENGLISH_ALPHABET.index(char) - key) % len(ENGLISH_ALPHABET)]
        
        plain_text += char
    
    return plain_text

def encrypt_affine(cipher_text: str, key: tuple[int, int]) -> str:
    cipher_text = sanatize_cipher_text(cipher_text)
    plain_text: str = ""
    for char in cipher_text:
        char = char.lower()
        if char in ENGLISH_ALPHABET:
            char = ENGLISH_ALPHABET[(
                (ENGLISH_ALPHABET.index(char) - key[1]) * pow(key[0], -1, len(ENGLISH_ALPHABET))
                ) % len(ENGLISH_ALPHABET)]
        
        plain_text += char
    
    return plain_text

def find_vigenere_key_length(cipher_text: str) -> int:
    min_length: int = 1
    potential_length: int  = -1
    while min_length < 10:
        repeats: list[int] = [repeat[2] for repeat in find_repeats(cipher_text, min_length)]

        if not repeats:
            continue
        
        potential_length = reduce(gcd, repeats)

        if potential_length == 1:
            min_length += 1
            continue
        else:
            break
    
    return potential_length

def get_initial_substition_key(cipher_text: str) -> str:
    frequencies: dict[str, float] = analyse_frequency(cipher_text)
    frequencies_parsed: str = parse_frequencies(frequencies)

    key: str = ""
    for char in ENGLISH_ALPHABET:
        index: int = ENGLISH_LETTER_BY_COMMON.index(char)
        key += frequencies_parsed[index]

    return key

def decrypt_subsitition(cipher_text: str, key: str) -> str:
    cipher_text = sanatize_cipher_text(cipher_text)

    for char, plain in zip(key, ENGLISH_ALPHABET):
        cipher_text = cipher_text.replace(char, plain.upper())
    
    return cipher_text.lower()

def randomly_modify_key(key: str) -> str:
    lower: int = randint(0, len(ENGLISH_ALPHABET) - 1)
    upper: int = randint(0, len(ENGLISH_ALPHABET) - 1)

    new_key_tmp: list[str] = list(key)
    new_key_tmp[lower], new_key_tmp[upper] = new_key_tmp[upper], new_key_tmp[lower]
    return "".join(new_key_tmp)

def make_better_subsitition_key(cipher_text: str, key: str) -> str:
    current_score: float = compute_bigram_score(decrypt_subsitition(cipher_text, key))
    
    possible_shuffles: list[tuple[int, int]] = list(combinations(range(len(ENGLISH_ALPHABET)), 2))
    shuffle(possible_shuffles)

    for lower, upper in possible_shuffles:
        new_key_tmp: list[str] = list(key)
        new_key_tmp[lower], new_key_tmp[upper] = new_key_tmp[upper], new_key_tmp[lower]
        new_key: str = "".join(new_key_tmp)
        new_score: float = compute_bigram_score(decrypt_subsitition(cipher_text, new_key))
        if new_score < current_score:
            return new_key
    
    return key

def make_canadiate_subsitition_solve(cipher_text: str, current_key_guess: str) -> str:
    cipher_text = sanatize_cipher_text(cipher_text)
    
    key_guess: str = current_key_guess
    prev_key: str = ""
    while prev_key != key_guess:
        prev_key = key_guess
        key_guess = make_better_subsitition_key(cipher_text, key_guess)

    return key_guess