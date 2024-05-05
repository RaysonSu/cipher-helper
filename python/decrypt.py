from typing import Callable
from math import gcd
from constants import *
from utils import *

def break_ceaser(cipher_text: str) -> str:
    cipher_text = sanatize_cipher_text(cipher_text)
    best_guess: tuple[float, str] = (2, "")
    for key in range(len(ENGLISH_ALPHABET)):
        guess: str = decrypt_ceaser(cipher_text, key)
        guess_frequency: dict[str, float] = analyse_frequency(guess)
        distance: float = compute_frequency_distance(guess_frequency, ENGLISH_LETTER_FREQUENCY)
        
        if best_guess > (distance, guess):
            best_guess = (distance, guess)

    return best_guess[1]

def break_affine(cipher_text: str) -> str:
    cipher_text = sanatize_cipher_text(cipher_text)
    best_guess: tuple[float, str] = (2, "")
    for multiplier in range(len(ENGLISH_ALPHABET)):
        if gcd(multiplier, len(ENGLISH_ALPHABET)) != 1:
            continue

        for shift in range(len(ENGLISH_ALPHABET)):
            guess: str = encrypt_affine(cipher_text, (multiplier, shift))
            guess_frequency: dict[str, float] = analyse_frequency(guess)
            distance: float = compute_frequency_distance(guess_frequency, ENGLISH_LETTER_FREQUENCY)
            
            if best_guess > (distance, guess):
                best_guess = (distance, guess)

    return best_guess[1]

def break_vigenere(cipher_text: str) -> str:
    cipher_text = sanatize_cipher_text(cipher_text)
    potential_length: int = find_vigenere_key_length(cipher_text)
    if potential_length == -1:
        raise ValueError("Decryption failed :( (no repeats found)")

    ceaser_blocks: list[str] = [cipher_text[i::potential_length] for i in range(potential_length)]
    ceaser_blocks = list(map(break_ceaser, ceaser_blocks))
    ceaser_blocks = [block.ljust(len(ceaser_blocks[0])) for block in ceaser_blocks]

    return sanatize_cipher_text("".join(["".join(chunk) for chunk in zip(*ceaser_blocks)]))


def break_all(cipher_text: str) -> str:
    solved_ciphers: list[Callable[[str], str]] = [
        break_ceaser,
        break_affine,
        break_vigenere
    ]

    best: tuple[int, str] = (-1, "")
    for solve_cipher in solved_ciphers:
        try:
            plain_text: str = solve_cipher(cipher_text)
            best = max(best, (count_words(plain_text), plain_text))
        except ValueError:
            pass

    if best[0] == -1:
        raise ValueError("Decryption failed :( (no plaintext found)")

    return best[1]