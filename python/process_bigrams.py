def main() -> None:
    with open("txt/bigrams.txt") as file:
        bigrams: list[str] = file.read().splitlines()

    total: int = 0
    ranked: list[str] = []
    counts: dict[str, float] = {}
    for bigram_data in bigrams:
        bigram: str = bigram_data[:2]
        bigram_count: int = int(bigram_data[3:])

        total += bigram_count
        ranked.append(bigram)
        counts[bigram] = bigram_count
    
    for key in counts.keys():
        counts[key] /= total


    print(counts)
    print()
    print(ranked)

if __name__ == "__main__":
    main()