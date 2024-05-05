from constants import *
from math import log10

def analyse_frequency(cipher_text: str) -> dict[str, float]:
    return {
        char: cipher_text.count(char) / len(cipher_text)
        for char in ENGLISH_ALPHABET
    }

def compute_frequency_distance(frequency_1: dict[str, float], frequency_2: dict[str, float]) -> float:
    ret: float = 0
    for char in set(frequency_1.keys()).union(frequency_2.keys()):
        char_frequency_1: float
        char_frequency_2: float
        if char in frequency_1.keys():
            char_frequency_1 = frequency_1[char]
        else:
            char_frequency_1 = 0

        if char in frequency_2.keys():
            char_frequency_2 = frequency_2[char]
        else:
            char_frequency_2 = 0
        
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