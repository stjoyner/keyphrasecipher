# Keyphrase Cipher Suite

This suite provides Python scripts for keyphrase-based monoalphabetic substitution encryption, user-directed ad hoc quantitative frequency and adjacency analysis, and interactive partial decryption.

---

## Suite Components

### 1. `KeyPhraseCipher.py`
Generates a monoalphabetic substitution cipher from a keyphrase and encrypts a multi-line plaintext.

* **Cipher Construction:** Removes spaces and duplicate letters from the user-provided keyphrase to form a prefix, then appends all remaining unrepresented alphabet letters in standard alphabetical order.
* **Input Parsing:** Strips line breaks (`\r`, `\n`) and non-alphabetic whitespace adjustments prior to translation. Non-alphabetic symbols pass through unchanged.
* **Usage:**
  ```bash
  python KeyPhraseCipher.py
* Can also accept redirected input:
  ```bash
  python KeyPhraseCipher.py < plaintext.txt

### 2. `LetterFreq.py`

Performs comprehensive unigram and bigram frequency distribution analyses on a target text file or stdin stream.
Features:
Unigram Analysis: Computes absolute counts, relative frequencies, and identifies letters with zero occurrences.
Unigram Adjacency: Evaluates preceding, following, and total distinct adjacent letters for the top 3 most frequent unigrams across word boundaries.
Bigram Analysis: Computes 2-gram frequencies over the contiguous letter stream.
Top-3 Bigram Profiling: Reports reversal counts (e.g., TH vs HT) and preceding/following trigram boundary extensions.
* **Usage:**
  ```bash
  # Via CLI argument (recommended for large files)
  python LetterFreq.py ciphertext.txt

  # Via standard input pipeline
  cat ciphertext.txt | python LetterFreq.py

### 3. `CipherSubs.py`

Applies user-defined partial character substitutions to a ciphertext file to aid iterative manual cryptanalysis.
Features:
Maps targeted uppercase ciphertext letters to lowercase plaintext letters.
Unmapped uppercase letters, pre-existing lowercase letters, numbers, punctuation, and whitespace remain completely unchanged.
Allows safe iterative execution on partially decrypted files.
* **Usage:**
  ```bash
  python CipherSubs.py ciphertext.txt
Interactive Prompt Example:
Plaintext
Enter number of substitutions to perform: 2
Mapping 1/2: B e
Mapping 2/2: G t

**Recommended Workflow**

* **Encryption:**
  ```bash
  python KeyPhraseCipher.py < message.txt > ciphertext.txt

* **Frequency & Adjacency Analysis:**
  ```bash
  python LetterFreq.py ciphertext.txt

* **Iterative Decryption:**
  ```bash
  python CipherSubs.py ciphertext.txt > partial_decryption.txt

