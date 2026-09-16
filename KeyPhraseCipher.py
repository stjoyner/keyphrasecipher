import string
import sys

def encode_keyphrase_cipher():
    keyphrase = input("Enter keyphrase: ")
    print("Enter plaintext (press Ctrl+D or Ctrl+Z on a new line when finished):")
    
    # Ingest multi-line stream from stdin
    raw_plaintext = sys.stdin.read()

    # Filter out line-break characters (CR, LF)
    plaintext = raw_plaintext.replace('\r', '').replace('\n', '')

    # Construct prefix from unique alphabetic characters in keyphrase
    key_chars = []
    for char in keyphrase.upper():
        if char.isalpha() and char not in key_chars:
            key_chars.append(char)

    # Append remaining unrepresented elements of Z/26Z in natural order
    cipher_alphabet = key_chars + [c for c in string.ascii_uppercase if c not in key_chars]

    # Map both lowercase and uppercase domain elements to the uppercase codomain
    domain = string.ascii_lowercase + string.ascii_uppercase
    codomain = "".join(cipher_alphabet) * 2
    trans_table = str.maketrans(domain, codomain)

    ciphertext = plaintext.translate(trans_table)
    print("Ciphertext:", ciphertext)

if __name__ == "__main__":
    encode_keyphrase_cipher() 
