def main() -> None:
    with open("txt/words.txt") as file:
        words: list[str] = file.read().splitlines()

    words = [word for word in words if len(word) >= 3]
    new_words: str = "\n".join(words)

    with open("txt/processed_words.txt", "w") as file:
        file.write(new_words)

if __name__ == "__main__":
    main()