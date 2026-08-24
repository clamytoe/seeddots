import random
from pathlib import Path


def load_wordlist(file="bip39_english.txt"):
    filepath = Path(__file__).parent / "data" / file
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def generate_seed_phrase(wordlist, count=24):
    return random.sample(wordlist, count)


def save_seed_phrase(seed_phrase, filepath: Path | str = "seed.txt"):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(" ".join(seed_phrase) + "\n")


def main():
    file = "sample_seed.txt"
    filepath = Path(Path(__file__).parent.parent, "examples", file)
    wordlist = load_wordlist()
    seed_phrase = generate_seed_phrase(wordlist)
    save_seed_phrase(seed_phrase, filepath=filepath)
    print(f"✅ Seed phrase saved to {filepath}")


if __name__ == "__main__":
    main()
