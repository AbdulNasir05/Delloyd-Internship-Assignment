# ** 🧮 String Similarity Matching Program **
📌 Overview

This Python program analyzes how similar two strings are using several algorithms.
It creates detailed reports that include character-by-character comparisons, statistical summaries, and suggestions.

The program uses:

Exact Position Matching (direct character comparison)

Levenshtein Distance (minimum edits needed)

Jaccard Similarity (character set overlap)

Alignment Analysis (how strings align when their lengths differ)

It supports:

✅ Predefined examples (runs without user input)

✅ Batch comparison of multiple string pairs

✅ Detailed reports with visual indicators for matches and mismatches

# ** ⚙️ Features **

🔍 Exact match, mismatch, extra, and missing character detection

🔢 Levenshtein edit distance calculation

🎯 Jaccard similarity based on unique character sets

🔧 Alignment-based comparison for strings of different lengths

📊 Detailed reports with positions and statistics

📂 Batch processing for multiple string pairs

📂 File Structure
StringSimilarity
 ├── similarity_analysis.py   # Main Python script
 ├── README.md                # Documentation

# ** ▶️ Usage **
1. Run the program
python similarity_analysis.py

2. Predefined Examples

The program automatically compares pairs like:

"python" vs "pythnn"

"hello" vs "helloo"

"abcdef" vs "abcxyz"

"program" vs "program"

"similar" vs "similer"

3. Batch Comparison

Additional pairs are compared in batch mode, for example:

"hello" vs "hellp"

"world" vs "worl"

"test" vs "best"

"string" vs "strung"

"compute" vs "compete"

# ** 📊 Example Output **
🔹 Exact Position Matching
EXACT POSITION MATCH REPORT

String 1: 'python' (Length: 6)  
String 2: 'pythnn' (Length: 6)  
Similarity: 83.33%

Character-by-character analysis:
Position | String1 | String2 | Status
1        | p       | p       | MATCH
...

🔹 Levenshtein & Jaccard
LEVENSHTEIN SIMILARITY: 83.33%
Levenshtein Distance: 1 edit required

JACCARD SIMILARITY: 85.71%

🔹 Alignment (if lengths differ)
ALIGNMENT ANALYSIS
Aligned String 1: hello-
Aligned String 2: helloo
Aligned Similarity: 100.00%

🔹 Final Summary
FINAL SUMMARY
Exact Position Similarity: 83.33%
Levenshtein Similarity:    83.33%
Jaccard Similarity:        85.71%

RECOMMENDATION
The strings are VERY SIMILAR.

# ** 🛠️ Custom Input **

If you want to allow custom inputs, uncomment the following in main():

str1 = input("Enter first string (6-10 characters): ").strip()
str2 = input("Enter second string (6-10 characters): ").strip()

# ** 📑 Batch Results Example **
ADDITIONAL BATCH COMPARISON EXAMPLES
Pair 1: 'hello' vs 'hellp' → 83.33%
Pair 2: 'world' vs 'worl' → 80.00%
Pair 3: 'test' vs 'best' → 75.00%
Pair 4: 'string' vs 'strung' → 83.33%
Pair 5: 'compute' vs 'compete' → 85.71%

# ** 🚀 Applications **

📚 Plagiarism detection

🧬 DNA/protein sequence comparison

🤖 Fuzzy text matching in NLP

📝 Autocorrect and spell-check systems

🗄️ Record linkage in databases
