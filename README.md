# Turn your seed words into secure dots. (*seeddots*)

> *Deterministic dot‑pattern encoding for BIP39 seed phrases.*

![Python version][python-version]
![Latest version][latest-version]
[![GitHub issues][issues-image]][issues-url]
[![GitHub forks][fork-image]][fork-url]
[![GitHub Stars][stars-image]][stars-url]
[![License][license-image]][license-url]

NOTE: This project was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@clamytoe's](https://github.com/clamytoe) [toepack](https://github.com/clamytoe/toepack) project template.

![SeedDots Logo Light][seeddots-logo-light]
![SeedDots Logo Dark][seeddots-logo-dark]

SeedDots provides a deterministic, reversible way to encode BIP39 seed phrases into compact dot‑patterns suitable for metal stamping, engraving, or visual backup.

Unlike QR codes or random patterns, SeedDots produces human‑verifiable, symbol‑agnostic, space‑efficient encodings that can be reconstructed even from partial damage.

SeedDots converts each word of a BIP39 mnemonic into a compact, 3‑column dotmap.
It’s a human‑portable obfuscation layer designed for secure backups, metal plates, and offline storage systems like OneKey stamping plates.

The dotmap is fully reversible, deterministic, and symbol‑set agnostic.

## ✨ Features

- 🔐 **Encode BIP39 seed phrases** into deterministic dotmaps  
- 🔄 **Decode dotmaps** back into seed phrases  
- 🧩 **Verification** of encoded/decoded output  
- 🖨️ **Printable stamping cards** (Markdown, PNG, or SVG)  
- 🧱 **Multiple symbol sets**: dot, ascii, block, rune  
- 📋 **Clipboard support** for fast workflows  
- 🧪 **Clean, modular architecture** (`encoder.py`, `utils.py`, `dotmap.py`)
- 🔒 **Zero external dependencies** for encoding/decoding

## 📦 Installation

Clone the repository:

```zsh
cd Projects
git clone https://github.com/clamytoe/seeddots.git
cd seeddots
```

### Conda environment

If you are an Anaconda user, this command will get you up to speed with the base installation.

```zsh
conda env create -f environment.yml
conda activate seeddots
```

### Python venv

If you are just using normal Python, this will get you ready, but I highly recommend that you do this in a virtual environment.
There are many ways to do this, the simplest using *venv*.

```zsh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### PIP install

```zsh
pip install -e .
```

## 🚀 Usage

### Run the CLI

```zsh
seeddots --help
Usage: seeddots [OPTIONS] COMMAND [ARGS]...

  SeedDots — Encode and decode BIP39 seed phrases into dotmaps.

Options:
  --help  Show this message and exit.

Commands:
  decode      Decode a dotmap back into a mnemonic phrase.
  encode      Encode a mnemonic phrase into a dotmap.
  logo        Print or save the SeedDots logo.
  preview     Preview the dotmap for a single word.
  printcard   Generate a printable stamping card for OneKey plates.
  symbol-key  Show symbol set mappings.
```

### Encode a seed phrase

```zsh
seeddots encode "abandon ability able about above absent"
```

### Encode from clipboard

```zsh
seeddots encode --from-clipboard --copy-output
```

### Decode a dotmap file

```zsh
seeddots decode --file dotmap.txt
```

### Preview with custom symbol set

Available sets can be viewed with the following command:

```zsh
seeddots symbol-key
   dot: ●  = 1  ○  = 0
 ascii: 1  = 1  0  = 0
 block: █  = 1  ░  = 0
  rune: ⊙  = 1  ∘  = 0
```

Then, preview with the following command:

```zsh
seeddots encode --file examples/sample_seed.txt --preview-symbols "block"
              🔐 BIP39 Dotmap Encoding
┏━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ Index ┃ Word     ┃ Column 1 ┃ Column 2 ┃ Column 3 ┃
┡━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│  1586 │ shiver   │ ░ █ █ ░  │ ░ ░ █ █  │ ░ ░ █ ░  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│  1757 │ swear    │ ░ █ █ ░  │ █ █ ░ █  │ █ █ ░ █  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│  1170 │ mutual   │ ░ █ ░ ░  │ █ ░ ░ █  │ ░ ░ █ ░  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│   399 │ crack    │ ░ ░ ░ █  │ █ ░ ░ ░  │ █ █ █ █  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│  1056 │ loop     │ ░ █ ░ ░  │ ░ ░ █ ░  │ ░ ░ ░ ░  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│  1291 │ pattern  │ ░ █ ░ █  │ ░ ░ ░ ░  │ █ ░ █ █  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│   110 │ asset    │ ░ ░ ░ ░  │ ░ █ █ ░  │ █ █ █ ░  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│  1650 │ soda     │ ░ █ █ ░  │ ░ █ █ █  │ ░ ░ █ ░  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│  1123 │ middle   │ ░ █ ░ ░  │ ░ █ █ ░  │ ░ ░ █ █  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│  1235 │ olympic  │ ░ █ ░ ░  │ █ █ ░ █  │ ░ ░ █ █  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│   351 │ cloth    │ ░ ░ ░ █  │ ░ █ ░ █  │ █ █ █ █  │
├───────┼──────────┼──────────┼──────────┼──────────┤
│   633 │ excuse   │ ░ ░ █ ░  │ ░ █ █ █  │ █ ░ ░ █  │
└───────┴──────────┴──────────┴──────────┴──────────┘
```

### Generate a stamping card (Markdown)

```zsh
seeddots printcard --file seed.txt --format markdown
```

### Generate a stamping card (SVG)

```zsh
seeddots printcard "gravity lunar ritual ..." --format svg --output card.svg
```

## 🧠 How It Works

Each BIP39 word has a deterministic index (1–2048).
SeedDots converts that index into a 12‑bit binary string, then maps each bit
to a symbol (● or ○, 1 or 0, etc.) in three 4‑bit columns.

Example:

```zsh
word: abandon
index: 1
binary: 000000000001
dotmap: ○○○○ ○○○○ ○○○●
```

## 📁 Project Structure

```zsh
seeddots/
 ├── encoder.py        # Pure encoding/decoding logic
 ├── utils.py          # I/O, verification, card generation
 ├── dotmap.py         # CLI interface
 ├── data/
 │    └── bip39_english.txt
 └── tests/            # pytest suite
```

## 🛡️ Security Notes

SeedDots does not store, transmit, or log seed phrases.
All encoding/decoding happens locally on your machine.

> **This tool is an obfuscation layer, not a replacement for proper key security**.

## 📜 License

Distributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license, "seeddots" is free and open source software — do whatever you want, just don’t blame me if you brick your wallet.

## 🤝 Contributing

Pull requests, feature ideas, and symbol‑set suggestions are welcome.
Tests can be run with with `pytest -v`, please ensure that all tests are passing and that you've checked your code with the following packages before submitting a pull request:

- black
- flake8
- isort
- mypy
- pytest-cov

I am not adhering to them strictly, but try to clean up what's reasonable.

⭐ Acknowledgments

Inspired by metal seed plate stamping workflows and the desire to create a reversible, human‑friendly encoding system for secure backups.

## Issues

If you encounter any problems, please [file an issue](https://github.com/clamytoe/toepack/issues) along with a detailed description.

## Changelog

- **v0.1.1** Normalized output for saving to file.
- **v0.1.0** Initial commit.

[seeddots-logo-light]: images/logo-light.png#gh-light-mode-only
[seeddots-logo-dark]: images/logo-dark.png#gh-dark-mode-only
[python-version]:https://img.shields.io/badge/python-3.13.3-brightgreen.svg
[latest-version]:https://img.shields.io/badge/version-0.1.1-blue.svg
[issues-image]:https://img.shields.io/github/issues/clamytoe/seeddots.svg
[issues-url]:https://github.com/clamytoe/seeddots/issues
[fork-image]:https://img.shields.io/github/forks/clamytoe/seeddots.svg
[fork-url]:https://github.com/clamytoe/seeddots/network
[stars-image]:https://img.shields.io/github/stars/clamytoe/seeddots.svg
[stars-url]:https://github.com/clamytoe/seeddots/stargazers
[license-image]:https://img.shields.io/github/license/clamytoe/seeddots.svg
[license-url]:https://github.com/clamytoe/seeddots/blob/main/LICENSE
