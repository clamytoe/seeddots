#!/usr/bin/env python
"""
dotmap.py — CLI interface for SeedDots.

This file contains:
- Click commands (encode, decode, preview, printcard, symbol_key)
- Rich table rendering
- Clipboard interactions

All encoding logic lives in encoder.py.
All utilities (I/O, verification, card generation) live in utils.py.
"""

import cairosvg
import click
import pyperclip
from rich.console import Console
from rich.table import Table

from seeddots.encoder import (
    SYMBOL_SETS,
    encode_word,
    decode_columns,
    binary_to_dotmap,
    index_to_binary,
)
from seeddots.utils import (
    load_wordlist,
    logo_gen,
    save_logo_png,
    normalize_encoded,
    resolve_phrase_input,
    parse_dot_file,
    generate_markdown_card,
    generate_svg_card,
    verify_phrase,
)

console = Console()


# ---------------------------------------------------------------------------
# CLI group
# ---------------------------------------------------------------------------


@click.group()
def cli():
    """SeedDots — Encode and decode BIP39 seed phrases into dotmaps."""
    pass


# ---------------------------------------------------------------------------
# Encode command
# ---------------------------------------------------------------------------


@cli.command()
@click.argument("phrase", required=False)
@click.option("--file", type=click.Path(exists=True), help="Path to seed phrase file")
@click.option("--from-clipboard", is_flag=True, help="Read mnemonic from clipboard")
@click.option("--copy-output", is_flag=True, help="Copy encoded dotmap to clipboard")
@click.option("--wordlist", default="bip39_english.txt", help="BIP39 wordlist path")
@click.option(
    "--symbol-set",
    default="ascii",
    type=click.Choice(list(SYMBOL_SETS.keys())),
    help="Symbol set for output dotmap",
)
@click.option(
    "--preview-symbols",
    default="dot",
    type=click.Choice(list(SYMBOL_SETS.keys())),
    help="Symbol set for console preview",
)
def encode(
    phrase, file, from_clipboard, copy_output, wordlist, symbol_set, preview_symbols
):
    """Encode a mnemonic phrase into a dotmap."""
    wl = load_wordlist(wordlist)
    phrase = resolve_phrase_input(file, from_clipboard, phrase)

    if not phrase:
        console.print("[red]No phrase provided.[/red]")
        return

    words = phrase.split()
    encoded_lines = []

    table = Table(title="🔐 BIP39 Dotmap Encoding", show_lines=True)
    table.add_column("Index", justify="right")
    table.add_column("Word", style="cyan")
    table.add_column("Column 1", justify="center")
    table.add_column("Column 2", justify="center")
    table.add_column("Column 3", justify="center")

    for word in words:
        try:
            col1_prev, col2_prev, col3_prev = encode_word(word, wl, preview_symbols)
            col1_out, col2_out, col3_out = encode_word(word, wl, symbol_set)

            index = wl.index(word) + 1

            table.add_row(str(index), word, col1_prev, col2_prev, col3_prev)
            col1_out = normalize_encoded(col1_out)
            col2_out = normalize_encoded(col2_out)
            col3_out = normalize_encoded(col3_out)
            print(f"{col1_out} {col2_out} {col3_out}")
            encoded_lines.append(f"{col1_out} {col2_out} {col3_out}")

        except ValueError:
            console.print(f"[red]Word not found:[/red] {word}")

    console.print(table)

    if copy_output:
        pyperclip.copy("\n".join(encoded_lines))
        console.print("[bold magenta]Output copied to clipboard.[/bold magenta]")


# ---------------------------------------------------------------------------
# Decode command
# ---------------------------------------------------------------------------


@cli.command()
@click.option("--file", type=click.Path(exists=True), help="Path to dotmap file")
@click.option("--from-clipboard", is_flag=True, help="Read dotmap from clipboard")
@click.option("--copy-output", is_flag=True, help="Copy decoded phrase to clipboard")
@click.option("--wordlist", default="bip39_english.txt", help="BIP39 wordlist path")
@click.option(
    "--symbol-set",
    default="ascii",
    type=click.Choice(list(SYMBOL_SETS.keys())),
    help="Symbol set used in the dotmap input",
)
@click.option(
    "--preview-symbols",
    default="dot",
    type=click.Choice(list(SYMBOL_SETS.keys())),
    help="Symbol set for console preview",
)
def decode(file, from_clipboard, copy_output, wordlist, symbol_set, preview_symbols):
    """Decode a dotmap back into a mnemonic phrase."""
    wl = load_wordlist(wordlist)

    if file:
        lines = parse_dot_file(file)
    elif from_clipboard:
        raw = pyperclip.paste().strip()
        lines = raw.splitlines()
    else:
        console.print("[yellow]Enter dotmap lines. Type 'done' to finish.[/yellow]")
        lines = []
        while True:
            line = input("Dotmap: ").strip()
            if line.lower() == "done":
                break
            lines.append(line)

    if not lines:
        console.print("[red]No dotmap input provided.[/red]")
        return

    decoded_words = []

    table = Table(title="🧩 Decoded BIP39 Words", show_lines=True)
    table.add_column("Index", justify="right")
    table.add_column("Word", style="green")
    table.add_column("Column 1", justify="center")
    table.add_column("Column 2", justify="center")
    table.add_column("Column 3", justify="center")

    for line in lines:
        try:
            if "  " in line:  # Support previously formatted dotmaps with double spaces
                col1, col2, col3 = line.split("  ")
                col1, col2, col3 = col1.strip(), col2.strip(), col3.strip()
            else:
                col1, col2, col3 = line.split()

            word = decode_columns(col1, col2, col3, wl, symbol_set)
            decoded_words.append(word)

            # Preview columns
            binary = index_to_binary(wl.index(word) + 1)
            col1_prev, col2_prev, col3_prev = binary_to_dotmap(binary, preview_symbols)

            table.add_row(
                str(wl.index(word) + 1), word, col1_prev, col2_prev, col3_prev
            )

        except Exception as e:
            console.print(f"[red]Invalid input:[/red] {e}")
            continue

    console.print(table)

    if copy_output:
        pyperclip.copy(" ".join(decoded_words))
        console.print("[bold magenta]Output copied to clipboard.[/bold magenta]")

    # Verification
    verified, info = verify_phrase(
        decoded_words,
        lines,
        wl,
        symbol_set,
        encode_fn=encode_word,
    )

    if verified:
        console.print(
            "[bold green]✅ Phrase verified: no corruption detected.[/bold green]"
        )
    else:
        console.print("[bold red]⚠️ Verification failed.[/bold red]")

        assert info is not None  # type narrowing for VSCode/mypy

        for i, word, orig, recon in info:
            console.print(f"[yellow]Line {i}:[/yellow] {word}")
            console.print(f"  Original: {orig}")
            console.print(f"  Re-encoded: {recon}")


# ---------------------------------------------------------------------------
# Preview command
# ---------------------------------------------------------------------------


@cli.command()
@click.argument("word")
@click.option(
    "--symbol-set",
    default="dot",
    type=click.Choice(list(SYMBOL_SETS.keys())),
    help="Symbol set for preview",
)
def preview(word, symbol_set):
    """Preview the dotmap for a single word."""
    wl = load_wordlist()
    try:
        col1, col2, col3 = encode_word(word, wl, symbol_set)
        console.print(f"\n{word.upper()} → {col1} {col2} {col3}")
    except ValueError:
        console.print(f"[red]Word not found:[/red] {word}")


# ---------------------------------------------------------------------------
# Printcard command
# ---------------------------------------------------------------------------


@cli.command()
@click.argument("phrase", required=False)
@click.option("--file", type=click.Path(exists=True), help="Path to seed phrase file")
@click.option("--wordlist", default="bip39_english.txt", help="BIP39 wordlist path")
@click.option(
    "--format",
    default="markdown",
    type=click.Choice(["markdown", "png", "svg"]),
    help="Output format",
)
@click.option("--output", type=click.Path(), help="Optional path to save output")
def printcard(phrase, file, wordlist, format, output):
    """Generate a printable stamping card for OneKey plates."""

    wl = load_wordlist(wordlist)
    phrase = resolve_phrase_input(file, False, phrase)

    if not phrase:
        console.print("[red]No phrase provided.[/red]")
        return

    words = phrase.split()
    entries = []

    for i, word in enumerate(words, 1):
        try:
            index = wl.index(word)
            binary = index_to_binary(index)
            entries.append((i, word, index, binary))
        except ValueError:
            console.print(f"[red]Word not found:[/red] {word}")
            return

    # Generate content
    if format == "markdown":
        content = generate_markdown_card(entries)
    elif format == "svg":
        content = generate_svg_card(entries)
    elif format == "png":
        svg_content = generate_svg_card(entries)
        content = cairosvg.svg2png(bytestring=svg_content.encode("utf-8"))
    else:
        raise ValueError(f"Unknown format: {format}")

    # Save or print
    if output:
        if format == "png":
            assert isinstance(content, (bytes, bytearray))
            with open(output, "wb") as f:
                f.write(content)
        else:
            assert isinstance(content, str)
            with open(output, "w", encoding="utf-8") as f:
                f.write(content)

        console.print(f"[green]Saved to {output}[/green]")
    else:
        click.echo(content)


# ---------------------------------------------------------------------------
# Symbol key
# ---------------------------------------------------------------------------


@cli.command()
def symbol_key():
    """Show symbol set mappings."""
    for name, (one, zero) in SYMBOL_SETS.items():
        console.print(f"[bold]{name:>6}[/bold]:\t{one} = 1\t{zero} = 0")


# ---------------------------------------------------------------------------
# Print logo
# ---------------------------------------------------------------------------


@cli.command()
@click.option("--style", default="dark", type=click.Choice(["dark", "light"]))
@click.option("--save", type=click.Path(), help="Save logo as PNG")
def logo(style, save):
    """Print or save the SeedDots logo."""
    if save:
        save_logo_png(style, save)
        console.print(f"[green]Saved logo to {save}[/green]")
    else:
        console.print(logo_gen(style))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    cli()
