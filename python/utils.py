from constants import *
from typing import TypeVar
from math import log10, gcd
from functools import reduce

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

def compute_frequency_distance(frequency_1: dict[str, float], frequency_2: dict[str, float]) -> float:
    ret: float = 0
    for char in set(frequency_1.keys()).union(frequency_2.keys()):
        char_frequency_1: float = try_getting_dict_value(frequency_1, char, 0)
        char_frequency_2: float = try_getting_dict_value(frequency_2, char, 0)
        
        ret += (char_frequency_1 - char_frequency_2) ** 2
    
    return ret

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