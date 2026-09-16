import collections
import string
import sys


def get_input_text() -> str:
    """Ingest input from CLI file argument if present; fallback to standard input stream."""
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            return file.read()
    print(
        "Reading from standard input (press Ctrl+D or Ctrl+Z on a new line when finished):",
        file=sys.stderr,
    )
    return sys.stdin.read()


def analyze_unigram_neighbors(tokens: list[str], target_char: str) -> dict:
    """Computes adjacent letter statistics for a unigram."""
    n = len(tokens)
    preceding = set()
    following = set()

    for i, char in enumerate(tokens):
        if char == target_char:
            if i > 0:
                preceding.add(tokens[i - 1])
            if i < n - 1:
                following.add(tokens[i + 1])

    adjacent_all = preceding | following
    adjacent_other = adjacent_all - {target_char}

    return {
        "preceding_distinct": preceding,
        "following_distinct": following,
        "adjacent_all_count": len(adjacent_all),
        "adjacent_other_count": len(adjacent_other),
        "adjacent_other_set": sorted(adjacent_other),
    }


def analyze_bigram_context(tokens: list[str], bigram: str) -> dict:
    """Computes boundary context sets (preceding/following unigrams) for a bigram."""
    n = len(tokens)
    c1, c2 = bigram[0], bigram[1]
    preceding = set()
    following = set()

    for i in range(n - 1):
        if tokens[i] == c1 and tokens[i + 1] == c2:
            if i > 0:
                preceding.add(tokens[i - 1])
            if i + 2 < n:
                following.add(tokens[i + 2])

    return {
        "preceding_distinct": sorted(preceding),
        "following_distinct": sorted(following),
        "preceding_count": len(preceding),
        "following_count": len(following),
    }


def main():
    raw_text = get_input_text()

    # Strip line breaks (\r, \n) and map to upper-case alphabetic subset
    stripped_text = raw_text.replace("\r", "").replace("\n", "")
    tokens = [char.upper() for char in stripped_text if char.isalpha()]
    n = len(tokens)

    if n == 0:
        print(
            "Error: Target sample contains no alphabetic tokens.",
            file=sys.stderr,
        )
        sys.exit(1)

    # -------------------------------------------------------------
    # 1. UNIGRAM ANALYSIS
    # -------------------------------------------------------------
    unigram_counts = collections.Counter(tokens)
    sorted_unigrams = sorted(
        unigram_counts.items(), key=lambda item: (-item[1], item[0])
    )

    formatted_unigram_counts = ", ".join(
        f"'{char}': {count}" for char, count in sorted_unigrams
    )

    canonical_alphabet = set(string.ascii_uppercase)
    absent_letters = sorted(canonical_alphabet - set(unigram_counts.keys()))

    print(f"Total alphabetic length N = {n}\n")
    print("Absolute letter counts (descending frequency):")
    print(f"{{{formatted_unigram_counts}}}\n")

    print(f"{'Letter':<8}{'Count':<10}{'Relative Frequency':<20}")
    print("-" * 38)
    for char, count in sorted_unigrams:
        rel_freq = count / n
        print(f"{char:<8}{count:<10}{rel_freq:<20.6f}")

    print("\nLetters with zero frequency in sample:")
    print(absent_letters if absent_letters else "None")

    # Unigram Adjacency Analysis (Top 3)
    top_3_unigrams = [
        char for char, _ in sorted_unigrams[: min(3, len(sorted_unigrams))]
    ]
    print("\n" + "=" * 60)
    print("UNIGRAM ADJACENCY ANALYSIS (TOP 3 MOST FREQUENT LETTERS)")
    print("=" * 60)

    for char in top_3_unigrams:
        adj = analyze_unigram_neighbors(tokens, char)
        print(f"\nTarget Letter: '{char}' (Occurrences: {unigram_counts[char]})")
        print(
            f"  - Distinct preceding letters: {len(adj['preceding_distinct'])}"
        )
        print(
            f"  - Distinct following letters: {len(adj['following_distinct'])}"
        )
        print(
            f"  - Total distinct adjacent letters (preceding OR following): {adj['adjacent_all_count']}"
        )
        print(
            f"  - Distinct OTHER letters adjacent (excluding '{char}'): {adj['adjacent_other_count']}"
        )
        print(f"    Set of other adjacent letters: {adj['adjacent_other_set']}")

    # -------------------------------------------------------------
    # 2. BIGRAM ANALYSIS
    # -------------------------------------------------------------
    if n < 2:
        print("\nInsufficient tokens for bigram analysis (N < 2).")
        return

    bigrams = [f"{tokens[i]}{tokens[i+1]}" for i in range(n - 1)]
    n_bigrams = len(bigrams)  # N - 1

    bigram_counts = collections.Counter(bigrams)
    sorted_bigrams = sorted(
        bigram_counts.items(), key=lambda item: (-item[1], item[0])
    )

    formatted_bigram_counts = ", ".join(
        f"'{bg}': {count}" for bg, count in sorted_bigrams
    )

    print("\n" + "=" * 60)
    print("BIGRAM FREQUENCY ANALYSIS")
    print("=" * 60)
    print(f"Total bigram tokens N_bg = {n_bigrams}\n")
    print("Absolute bigram counts (descending frequency):")
    print(f"{{{formatted_bigram_counts}}}\n")

    print(f"{'Bigram':<8}{'Count':<10}{'Relative Frequency':<20}")
    print("-" * 38)
    for bg, count in sorted_bigrams:
        rel_freq = count / n_bigrams
        print(f"{bg:<8}{count:<10}{rel_freq:<20.6f}")

    # Top 3 Bigram Structural Analysis
    top_3_bigrams = [
        bg for bg, _ in sorted_bigrams[: min(3, len(sorted_bigrams))]
    ]
    print("\n" + "=" * 60)
    print("TOP 3 BIGRAM DETAILED ANALYSIS")
    print("=" * 60)

    for bg in top_3_bigrams:
        count = bigram_counts[bg]
        rel_freq = count / n_bigrams
        reversed_bg = bg[::-1]
        reversed_count = bigram_counts.get(reversed_bg, 0)
        reversed_rel_freq = reversed_count / n_bigrams

        bg_ctx = analyze_bigram_context(tokens, bg)

        print(f"\nTarget Bigram: '{bg}'")
        print(f"  - Absolute Count: {count}")
        print(f"  - Relative Frequency (P_{{N-1}}^{(2)}): {rel_freq:.6f}")
        print(
            f"  - Reversal Bigram '{reversed_bg}' Count: {reversed_count} (Freq: {reversed_rel_freq:.6f})"
        )
        print(
            f"  - Distinct preceding unigrams (Trigram w_1+{bg}): {bg_ctx['preceding_count']}"
        )
        print(f"    Set: {bg_ctx['preceding_distinct']}")
        print(
            f"  - Distinct following unigrams (Trigram {bg}+w_2): {bg_ctx['following_count']}"
        )
        print(f"    Set: {bg_ctx['following_distinct']}")


if __name__ == "__main__":
    main()
