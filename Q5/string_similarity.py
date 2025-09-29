def calculate_similarity(str1, str2):
    """
    Calculate similarity between two strings using multiple methods
    Returns similarity percentage and detailed analysis
    """
    # Method 1: Exact character matching
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
    
    # Handle remaining characters if strings are different lengths
    if len(str1) > len(str2):
        for i in range(min_len, len(str1)):
            match_details.append(('EXTRA', i, str1[i], '-'))
    elif len(str2) > len(str1):
        for i in range(min_len, len(str2)):
            match_details.append(('MISSING', i, '-', str2[i]))
    
    # Calculate similarity percentage
    similarity = (exact_matches / max_len) * 100 if max_len > 0 else 0
    
    return similarity, match_details, exact_matches, max_len

def levenshtein_distance(str1, str2):
    """
    Calculate Levenshtein distance between two strings
    (Minimum number of single-character edits required to change one string into the other)
    """
    if len(str1) < len(str2):
        return levenshtein_distance(str2, str1)
    
    if len(str2) == 0:
        return len(str1)
    
    previous_row = range(len(str2) + 1)
    for i, c1 in enumerate(str1):
        current_row = [i + 1]
        for j, c2 in enumerate(str2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def jaccard_similarity(str1, str2):
    """
    Calculate Jaccard similarity between character sets
    """
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return (intersection / union) * 100 if union > 0 else 0

def align_strings(str1, str2):
    """
    Perform dynamic programming alignment (Needleman-Wunsch-like)
    """
    # Simple alignment - find best starting position
    len1, len2 = len(str1), len(str2)
    
    if len1 == len2:
        return str1, str2  # No alignment needed
    
    # Try different alignments to maximize matches
    best_alignment = (str1, str2)
    best_matches = 0
    
    # Try shifting the shorter string
    if len1 < len2:
        shorter, longer = str1, str2
    else:
        shorter, longer = str2, str1
    
    for shift in range(len(longer) - len(shorter) + 1):
        aligned_shorter = '-' * shift + shorter + '-' * (len(longer) - len(shorter) - shift)
        
        if len1 < len2:
            temp_str1, temp_str2 = aligned_shorter, longer
        else:
            temp_str2, temp_str1 = aligned_shorter, longer
        
        # Count matches
        matches = sum(1 for a, b in zip(temp_str1, temp_str2) if a == b and a != '-' and b != '-')
        
        if matches > best_matches:
            best_matches = matches
            best_alignment = (temp_str1, temp_str2)
    
    return best_alignment

def generate_match_report(str1, str2, similarity, match_details, method_name):
    """
    Generate a detailed match report
    """
    print(f"\n{'='*60}")
    print(f"📊 {method_name} MATCH REPORT")
    print(f"{'='*60}")
    print(f"String 1: '{str1}' (Length: {len(str1)})")
    print(f"String 2: '{str2}' (Length: {len(str2)})")
    print(f"Similarity: {similarity:.2f}%")
    print(f"{'-'*60}")
    
    # Display character-by-character analysis
    print("Character-by-character analysis:")
    print("Position | String1 | String2 | Status")
    print("-" * 40)
    
    for status, pos, char1, char2 in match_details:
        pos_display = pos + 1  # Convert to 1-based indexing for display
        if status == 'MATCH':
            print(f"{pos_display:8} | {char1:7} | {char2:7} | ✅ MATCH")
        elif status == 'MISMATCH':
            print(f"{pos_display:8} | {char1:7} | {char2:7} | ❌ MISMATCH")
        elif status == 'EXTRA':
            print(f"{pos_display:8} | {char1:7} | {char2:7} | ➕ EXTRA CHARACTER")
        elif status == 'MISSING':
            print(f"{pos_display:8} | {char1:7} | {char2:7} | ➖ MISSING CHARACTER")
    
    # Summary statistics
    matches = sum(1 for detail in match_details if detail[0] == 'MATCH')
    mismatches = sum(1 for detail in match_details if detail[0] == 'MISMATCH')
    extras = sum(1 for detail in match_details if detail[0] == 'EXTRA')
    missing = sum(1 for detail in match_details if detail[0] == 'MISSING')
    
    print(f"{'-'*60}")
    print(f"📈 SUMMARY:")
    print(f"✅ Matches: {matches}")
    print(f"❌ Mismatches: {mismatches}")
    if extras > 0:
        print(f"➕ Extra characters: {extras}")
    if missing > 0:
        print(f"➖ Missing characters: {missing}")

def perform_aligned_comparison(str1, str2):
    """
    Perform comparison with alignment
    """
    print(f"\n{'🔧 ALIGNMENT ANALYSIS ':-^60}")
    
    # Perform alignment
    aligned_str1, aligned_str2 = align_strings(str1, str2)
    
    print(f"Aligned String 1: {aligned_str1}")
    print(f"Aligned String 2: {aligned_str2}")
    
    # Calculate similarity on aligned strings
    matches = 0
    total_comparable = 0
    alignment_details = []
    
    for i, (char1, char2) in enumerate(zip(aligned_str1, aligned_str2)):
        if char1 != '-' and char2 != '-':
            total_comparable += 1
            if char1 == char2:
                matches += 1
                alignment_details.append(('MATCH', i, char1, char2))
            else:
                alignment_details.append(('MISMATCH', i, char1, char2))
        elif char1 == '-':
            alignment_details.append(('MISSING', i, char1, char2))
        else:
            alignment_details.append(('EXTRA', i, char1, char2))
    
    aligned_similarity = (matches / total_comparable) * 100 if total_comparable > 0 else 0
    
    print(f"Aligned Similarity: {aligned_similarity:.2f}%")
    print(f"Comparable positions: {total_comparable}")
    print(f"Matches after alignment: {matches}")
    
    return aligned_similarity, alignment_details

def analyze_strings(str1, str2):
    """
    Analyze two strings and generate comprehensive report
    """
    print(f"\n{' ANALYSIS IN PROGRESS ':=^60}")
    
    # Validate string lengths
    if len(str1) < 6 or len(str1) > 10 or len(str2) < 6 or len(str2) > 10:
        print("⚠️  Warning: Strings should be 6-10 characters for optimal analysis")
        print("Continuing with analysis anyway...")
    
    # Method 1: Exact position matching
    similarity1, details1, matches, total = calculate_similarity(str1, str2)
    generate_match_report(str1, str2, similarity1, details1, "EXACT POSITION")
    
    # Method 2: Levenshtein similarity
    lev_distance = levenshtein_distance(str1, str2)
    max_len = max(len(str1), len(str2))
    lev_similarity = ((max_len - lev_distance) / max_len) * 100
    print(f"\n🔢 LEVENSHTEIN SIMILARITY: {lev_similarity:.2f}%")
    print(f"Levenshtein Distance: {lev_distance} edits required")
    
    # Method 3: Jaccard similarity
    jac_similarity = jaccard_similarity(str1, str2)
    print(f"\n🎯 JACCARD SIMILARITY: {jac_similarity:.2f}%")
    print("(Based on character set overlap)")
    
    # Method 4: Aligned comparison (if strings have different lengths)
    if len(str1) != len(str2):
        aligned_similarity, alignment_details = perform_aligned_comparison(str1, str2)
        
        # Display alignment details
        print(f"\n{' ALIGNMENT DETAILS ':-^60}")
        print("Position | Aligned1 | Aligned2 | Status")
        print("-" * 45)
        
        for status, pos, char1, char2 in alignment_details:
            pos_display = pos + 1
            if status == 'MATCH':
                print(f"{pos_display:8} | {char1:8} | {char2:8} | ✅ MATCH")
            elif status == 'MISMATCH':
                print(f"{pos_display:8} | {char1:8} | {char2:8} | ❌ MISMATCH")
            elif status == 'MISSING':
                print(f"{pos_display:8} | {char1:8} | {char2:8} | ➖ MISSING")
            elif status == 'EXTRA':
                print(f"{pos_display:8} | {char1:8} | {char2:8} | ➕ EXTRA")
    else:
        aligned_similarity = similarity1
    
    # Final comparison summary
    print(f"\n{'📋 FINAL SUMMARY ':=^60}")
    print(f"Exact Position Similarity: {similarity1:.2f}%")
    print(f"Levenshtein Similarity:    {lev_similarity:.2f}%")
    print(f"Jaccard Similarity:        {jac_similarity:.2f}")
    
    if len(str1) != len(str2):
        print(f"Aligned Similarity:       {aligned_similarity:.2f}%")
    
    # Recommendation
    print(f"\n{'💡 RECOMMENDATION ':-^60}")
    avg_similarity = (similarity1 + lev_similarity + jac_similarity) / 3
    if avg_similarity > 80:
        print("The strings are VERY SIMILAR")
    elif avg_similarity > 60:
        print("The strings are MODERATELY SIMILAR")
    elif avg_similarity > 40:
        print("The strings are SOMEWHAT SIMILAR")
    else:
        print("The strings are NOT VERY SIMILAR")
    
    return avg_similarity

def main():
    """
    Main function to run the string similarity analysis
    """
    print("🎯 STRING SIMILARITY MATCHING PROGRAM")
    print("=" * 50)
    
    # Option 1: Use predefined examples (no user input required)
    examples = [
        ("python", "pythnn"),
        ("hello", "helloo"),
        ("abcdef", "abcxyz"),
        ("program", "program"),
        ("similar", "similer")
    ]
    
    print("Using predefined examples (no user input required):")
    print("-" * 50)
    
    for i, (str1, str2) in enumerate(examples, 1):
        print(f"\nExample {i}: '{str1}' vs '{str2}'")
        print("-" * 30)
        analyze_strings(str1, str2)
        if i < len(examples):
            print("\n" + "="*70)
    
    # Option 2: Uncomment below if you want to try custom input
    # (but keep it commented to avoid the EOF error)
    """
    try:
        # Get input strings
        str1 = input("Enter first string (6-10 characters): ").strip()
        str2 = input("Enter second string (6-10 characters): ").strip()
        
        if str1 and str2:
            analyze_strings(str1, str2)
        else:
            print("Using default examples since no input provided.")
            analyze_strings("example", "exampel")
            
    except EOFError:
        print("Input not available. Using predefined examples.")
        analyze_strings("python", "pythnn")
    """

def batch_comparison(string_pairs):
    """
    Compare multiple string pairs at once
    """
    print(f"\n{' BATCH COMPARISON ':=^60}")
    results = []
    
    for i, (s1, s2) in enumerate(string_pairs, 1):
        similarity, details, _, _ = calculate_similarity(s1, s2)
        results.append((s1, s2, similarity))
        print(f"Pair {i}: '{s1}' vs '{s2}' → {similarity:.2f}%")
    
    return results

if __name__ == "__main__":
    main()
    
    # Additional batch comparison examples
    print("\n" + "="*70)
    print("ADDITIONAL BATCH COMPARISON EXAMPLES")
    print("="*70)
    
    example_pairs = [
        ("hello", "hellp"),
        ("world", "worl"),
        ("test", "best"),
        ("string", "strung"),
        ("compute", "compete")
    ]
    
    batch_results = batch_comparison(example_pairs)
    
    print(f"\n{' BATCH RESULTS SUMMARY ':-^60}")
    for s1, s2, similarity in batch_results:
        print(f"'{s1}' vs '{s2}': {similarity:.2f}% similarity")