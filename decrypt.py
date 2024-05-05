from functools import reduce
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

def break_vigenere(cipher_text: str) -> str:
    cipher_text = sanatize_cipher_text(cipher_text)
    repeats: list[int] = [repeat[2] for repeat in find_repeats(cipher_text)]
    if not repeats:
        raise ValueError("Decryption failed :( (no repeats found)")
    potential_length: int = reduce(gcd, repeats)

    ceaser_blocks: list[str] = [cipher_text[i::potential_length] for i in range(potential_length)]
    ceaser_blocks = list(map(break_ceaser, ceaser_blocks))
    ceaser_blocks = [block.ljust(len(ceaser_blocks[0])) for block in ceaser_blocks]

    return sanatize_cipher_text("".join(["".join(chunk) for chunk in zip(*ceaser_blocks)]))
