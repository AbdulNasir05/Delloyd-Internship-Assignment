# 🚗 License Plate Matching & Similarity Testing

# ** 📌 Overview **

This Python program tests the similarity of Indian license plates using various string-matching algorithms. It generates valid and invalid license plates, compares them, and produces a detailed test report.

The system uses:

Levenshtein Distance (minimum edits needed)

SequenceMatcher Ratio (from difflib)

Jaccard Similarity (character set overlap)

It is set up for unit testing with pytest but can also run independently, providing a full console report.

# ** ⚙️ Features **

✅ Automatic generation of valid and invalid plates

🔍 Similarity calculation using multiple algorithms

📊 Detailed test report with statistics, samples, and failures

🚦 Edge case testing (empty strings, case differences, single-character changes)

⚡ Performance testing (1000 operations in under 5 seconds)

📝 Clear output showing success rates, examples, and failed cases

# ** 📂 File Structure **
LicensePlateMatching
 
 ├── license_plate_tests.py   # Main Python test script
 
 ├── README.md                # Documentation

# ** ▶️ Usage **
1. Run directly (without pytest)
python license_plate_tests.py


This will:

Run 1000 valid plate comparisons

Run 1000 invalid plate comparisons

Execute edge case tests

Conduct performance tests

Generate a console report

2. Run with pytest
pytest -v license_plate_tests.py


This executes all tests with assertions.

# ** 📊 Example Output **
🔹 Startup
🚀 RUNNING LICENSE PLATE TESTS DIRECTLY
==================================================
🚀 STARTING LICENSE PLATE MATCHING TESTS
==================================================

🔹 Valid Plates Testing

🔧 Testing Valid License Plate Matching (1000 pairs)...

  Completed 200/1000 valid plate tests...
  
  Completed 400/1000 valid plate tests...
...

🔹 Invalid Plates Testing

🔧 Testing Invalid License Plate Matching (1000 pairs)...

  Completed 200/1000 invalid plate tests...
  
  Completed 400/1000 invalid plate tests...
...

🔹 Final Report
📊 LICENSE PLATE MATCHING TEST REPORT
==================================================

📈 OVERALL STATISTICS:

Total Tests: 2000

Passed: 1945

Failed: 55

Success Rate: 97.25%

✅ VALID LICENSE PLATES TESTING:

Tests: 1000

Passed: 980

Failed: 20

Success Rate: 98.00%

Similarity - Avg: 92.35%, Max: 100.00%, Min: 65.00%

❌ INVALID LICENSE PLATES TESTING:

Tests: 1000

Passed: 965

Failed: 35

Success Rate: 96.50%

Similarity - Avg: 28.42%, Max: 62.00%, Min: 10.00%

Sample Test Cases

# ** 🔍 SAMPLE TEST CASES: **

Valid Plate Examples (First 3):

  1. MH12AB1234 vs MH12AB1235 - 90.00% - ✅ PASS
 
  2. DL09CD5678 vs DL09CD567X - 88.00% - ✅ PASS
 
  3. KA45EF9999 vs KA45EF9998 - 91.00% - ✅ PASS

Invalid Plate Examples (First 3):

  1. MH12AB1234 vs A1B2C3D! - 25.00% - ✅ PASS

  2. TN34ZZ4321 vs QWERTY12 - 30.00% - ✅ PASS

  3. DL99JK8765 vs $$$AB123 - 15.00% - ✅ PASS

# ** 🧪 Edge Cases **

Examples tested:

"" vs "" → 100% similarity (empty strings)

"AB1234" vs "" → 0% similarity (one empty string)

"AB1234" vs "AB1234" → 100% similarity (exact match)

"AB1234" vs "AB1235" → ~83% similarity (single digit difference)

"AB1234" vs "AC1234" → ~83% similarity (single letter difference)

"ab12cd3456" vs "AB12CD3456" → 100% similarity (case-insensitive)

# ** ⚡ Performance **

🔧 Testing Performance (1000 operations)...

  Completed 200/1000 similarity calculations...
  
  Completed 400/1000 similarity calculations...
...

✅ Performance test completed in 0.45 seconds

# ** 📦 Requirements **

Python 3.7+

pytest (for test execution)

Install pytest if not already installed:

pip install pytest

# ** 👨‍💻 Author **

Abdul Nasir

Delloyd Internship 2025
