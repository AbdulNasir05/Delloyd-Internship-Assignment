# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def calculate_similarity(str1, str2):
    min_len = min(len(str1), len(str2))
    max_len = max(len(str1), len(str2))
    exact_matches = 0
    match_details = []

    for i in range(min_len):
        if str1[i] == str2[i]:
            exact_matches += 1
            match_details.append(('MATCH', i, str1[i], str2[i]))
        else:
            match_details.append(('MISMATCH', i, str1[i], str2[i]))

    if len(str1) > len(str2):
        for i in range(min_len, len(str1)):
            match_details.append(('EXTRA', i, str1[i], '-'))
    elif len(str2) > len(str1):
        for i in range(min_len, len(str2)):
            match_details.append(('MISSING', i, '-', str2[i]))

    similarity = (exact_matches / max_len) * 100 if max_len > 0 else 0
    return similarity, match_details


def levenshtein_distance(str1, str2):
    if len(str1) < len(str2):
        return levenshtein_distance(str2, str1)
    if len(str2) == 0:
        return len(str1)
    prev_row = range(len(str2) + 1)
    for i, c1 in enumerate(str1):
        curr_row = [i + 1]
        for j, c2 in enumerate(str2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def jaccard_similarity(str1, str2):
    set1, set2 = set(str1), set(str2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return (intersection / union) * 100 if union > 0 else 0


def align_strings(str1, str2):
    len1, len2 = len(str1), len(str2)
    if len1 == len2:
        return str1, str2

    if len1 < len2:
        shorter, longer = str1, str2
    else:
        shorter, longer = str2, str1

    best_matches = 0
    best_alignment = (shorter, longer)
    for shift in range(len(longer) - len(shorter) + 1):
        aligned_shorter = '-' * shift + shorter + '-' * (len(longer) - len(shorter) - shift)
        temp_str1, temp_str2 = (aligned_shorter, longer) if len1 < len2 else (longer, aligned_shorter)
        matches = sum(1 for a, b in zip(temp_str1, temp_str2) if a == b and a != '-')
        if matches > best_matches:
            best_matches = matches
            best_alignment = (temp_str1, temp_str2)
    return best_alignment


def generate_aligned_report(str1, str2):
    aligned_str1, aligned_str2 = align_strings(str1, str2)
    match_details = []

    for i, (c1, c2) in enumerate(zip(aligned_str1, aligned_str2)):
        if c1 == c2 and c1 != '-':
            match_details.append(('MATCH', i, c1, c2))
        elif c1 == '-':
            match_details.append(('MISSING', i, c1, c2))
        elif c2 == '-':
            match_details.append(('EXTRA', i, c1, c2))
        else:
            match_details.append(('MISMATCH', i, c1, c2))

    similarity = sum(1 for d in match_details if d[0] == 'MATCH') / max(len(aligned_str1), len(aligned_str2)) * 100

    print(f"\nAligned Comparison Table:")
    print("="*50)
    print("Pos | Str1 | Str2 | Status")
    for status, pos, c1, c2 in match_details:
        if status == "MATCH":
            symbol = f"{GREEN}✅ MATCH{RESET}"
        elif status == "MISMATCH":
            symbol = f"{RED}❌ MISMATCH{RESET}"
        elif status == "EXTRA":
            symbol = f"{YELLOW}➕ EXTRA{RESET}"
        else:
            symbol = f"{YELLOW}➖ MISSING{RESET}"
        print(f"{pos+1:^3} | {c1:^4} | {c2:^4} | {symbol}")
    print(f"Aligned similarity: {BOLD}{CYAN}{similarity:.2f}%{RESET}")
    return similarity


def analyze_strings(str1, str2):
    similarity, match_details = calculate_similarity(str1, str2)

    print(f"\nComparing '{str1}' vs '{str2}'")
    print("="*50)
    print("Position | Str1 | Str2 | Status")
    for status, pos, c1, c2 in match_details:
        if status == "MATCH":
            symbol = f"{GREEN}✅ MATCH{RESET}"
        elif status == "MISMATCH":
            symbol = f"{RED}❌ MISMATCH{RESET}"
        elif status == "EXTRA":
            symbol = f"{YELLOW}➕ EXTRA{RESET}"
        else:
            symbol = f"{YELLOW}➖ MISSING{RESET}"
        print(f"{pos+1:^8} | {c1:^4} | {c2:^4} | {symbol}")
    print(f"Exact position similarity: {BOLD}{CYAN}{similarity:.2f}%{RESET}")

    lev_dist = levenshtein_distance(str1, str2)
    lev_similarity = ((max(len(str1), len(str2)) - lev_dist) / max(len(str1), len(str2))) * 100
    print(f"Levenshtein similarity: {BOLD}{CYAN}{lev_similarity:.2f}%{RESET} (Distance: {lev_dist})")

    jac_similarity = jaccard_similarity(str1, str2)
    print(f"Jaccard similarity: {BOLD}{CYAN}{jac_similarity:.2f}%{RESET}")

    # Always perform aligned comparison
    aligned_similarity = generate_aligned_report(str1, str2)

    avg_similarity = (similarity + lev_similarity + jac_similarity + aligned_similarity) / 4
    print("\nRecommendation:")
    if avg_similarity > 80:
        print(f"{GREEN}The strings are VERY SIMILAR{RESET}")
    elif avg_similarity > 60:
        print(f"{YELLOW}The strings are MODERATELY SIMILAR{RESET}")
    elif avg_similarity > 40:
        print(f"{YELLOW}The strings are SOMEWHAT SIMILAR{RESET}")
    else:
        print(f"{RED}The strings are NOT VERY SIMILAR{RESET}")
    print("="*50)


def main():
    print("🎯 STRING SIMILARITY MATCHING PROGRAM")
    while True:
        str1 = input("\nEnter first string (6-10 chars) or press Enter to exit: ").strip()
        if str1 == "":
            print("Exiting program. Goodbye!")
            break
        str2 = input("Enter second string (6-10 chars): ").strip()
        if str2 == "":
            print("Exiting program. Goodbye!")
            break
        if not (6 <= len(str1) <= 10 and 6 <= len(str2) <= 10):
            print(f"{RED}Strings must be 6-10 characters. Try again.{RESET}")
            continue
        analyze_strings(str1, str2)


if __name__ == "__main__":
    main()
