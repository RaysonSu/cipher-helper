from constants import * 
from decrypt import *
from utils import *

def main() -> None:
    with open(CIPHER_TEXT_FILE_LOCATION, "r") as file:
        cipher_text: str = file.read()
    
    print(break_all(cipher_text))

if __name__ == "__main__":
    main()
