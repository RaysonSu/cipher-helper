from constants import * 
from decrypt import *

def main() -> None:
    with open(CIPHER_TEXT_FILE_LOCATION, "r") as file:
        cipher_text: str = file.read()
    
    print(break_vigenere(cipher_text))

if __name__ == "__main__":
    main()
