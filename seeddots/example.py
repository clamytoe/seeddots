from typing import List
from importlib.resources import files


# Load BIP39 wordlist
def load_wordlist(path="bip39_english.txt") -> List[str]:
    wordlist_path = files("data").joinpath(path)
    return wordlist_path.read_text(encoding="utf-8").splitlines()


# Convert index to 12-bit binary string
def index_to_binary(index: int) -> str:
    return format(index, "012b")


# Convert binary string to dotmap (● for 1, ○ for 0)
def binary_to_dotmap(binary: str) -> List[str]:
    return [
        "".join("● " if bit == "1" else "○ " for bit in binary[0:4]),
        "".join("● " if bit == "1" else "○ " for bit in binary[4:8]),
        "".join("● " if bit == "1" else "○ " for bit in binary[8:12]),
    ]


# Encode a mnemonic phrase into dotmap
def encode_phrase(phrase: str, wordlist: List[str]) -> List[dict]:
    words = phrase.strip().split()
    result = []
    for word in words:
        index = wordlist.index(word)
        binary = index_to_binary(index)
        dotmap = binary_to_dotmap(binary)
        result.append(
            {
                "word": word,
                "index": index,
                "column1": dotmap[0],
                "column2": dotmap[1],
                "column3": dotmap[2],
            }
        )
    return result


# Pretty-print dotmap table
def print_dotmap_table(dotmap_data: List[dict]):
    print(f"{'Index':<6} {'Word':<10} {'Column1':<8} {'Column2':<8} {'Column3':<8}")
    print("-" * 44)
    for item in dotmap_data:
        print(
            f"{item['index']:<6} {item['word']:<10} {item['column1']:<8} {item['column2']:<8} {item['column3']:<8}"
        )


# Example usage
if __name__ == "__main__":
    wordlist = load_wordlist()
    phrase = "shiver swear mutual crack loop pattern asset soda middle olympic cloth excuse flock wild purity"
    dotmap_data = encode_phrase(phrase, wordlist)
    print_dotmap_table(dotmap_data)
