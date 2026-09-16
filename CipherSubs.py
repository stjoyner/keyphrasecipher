import sys


def load_ciphertext() -> str:
    """Ingest ciphertext from command-line argument file path or prompt."""
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Enter path to ciphertext file (.txt): ").strip()

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def get_substitutions() -> dict[int, str]:
    """Collect k user-defined mappings from ciphertext (uppercase) to plaintext (lowercase)."""
    while True:
        try:
            k = int(input("Enter number of substitutions to perform: "))
            if k >= 0:
                break
            print("Please enter a non-negative integer.")
        except ValueError:
            print("Invalid input. Enter an integer.")

    mapping = {}
    print(
        "\nEnter each pair separated by space (e.g., 'B e' maps ciphertext 'B' to plaintext 'e'):"
    )

    for i in range(1, k + 1):
        while True:
            user_input = (
                input(f"Mapping {i}/{k}: ").strip().split()
            )
            if len(user_input) == 2:
                cipher_char, plain_char = user_input[0], user_input[1]
                if len(cipher_char) == 1 and len(plain_char) == 1:
                    # Translate mapping to Unicode ordinal keys for str.maketrans
                    mapping[ord(cipher_char)] = plain_char
                    break
            print(
                "  Invalid format. Enter a single ciphertext character followed by a single plaintext character."
            )

    return mapping


def main():
    try:
        ciphertext = load_ciphertext()
    except FileNotFoundError:
        print("Error: Specified file not found.", file=sys.stderr)
        sys.exit(1)

    mapping = get_substitutions()

    # Apply partial endomorphism via translation table
    trans_table = str.maketrans(mapping)
    modified_text = ciphertext.translate(trans_table)

    print("\n" + "=" * 60)
    print("TRANSFORMED CIPHERTEXT")
    print("=" * 60)
    print(modified_text)


if __name__ == "__main__":
    main()
