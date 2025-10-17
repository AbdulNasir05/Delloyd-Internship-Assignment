import random
import string
from difflib import SequenceMatcher
import sys

# ------------------ ANSI COLORS ------------------ #
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

# ------------------ LICENSE PLATE GENERATOR ------------------ #
class LicensePlateGenerator:
    """Generates valid and invalid Indian license plates."""

    def generate_valid_plate(self):
        """Generate a valid Indian plate (e.g., MH12AB1234)."""
        state = ''.join(random.choices(string.ascii_uppercase, k=2))
        district = ''.join(random.choices(string.digits, k=2))
        series = ''.join(random.choices(string.ascii_uppercase, k=2))
        number = ''.join(random.choices(string.digits, k=4))
        return f"{state}{district}{series}{number}"

    def generate_invalid_plate(self):
        """Generate a random invalid plate."""
        length = random.randint(5, 12)
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length))

# ------------------ SIMILARITY FUNCTIONS ------------------ #
def levenshtein_distance(s1, s2):
    """Compute Levenshtein distance."""
    s1, s2 = s1.upper(), s2.upper()
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def jaccard_similarity(s1, s2):
    """Compute Jaccard similarity based on character sets."""
    s1, s2 = s1.upper(), s2.upper()
    set1, set2 = set(s1), set(s2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0

def calculate_similarity(plate1, plate2):
    """Weighted similarity using SequenceMatcher and Levenshtein."""
    plate1, plate2 = plate1.upper(), plate2.upper()
    if not plate1 and not plate2:
        return 1.0
    if not plate1 or not plate2:
        return 0.0
    seq_match = SequenceMatcher(None, plate1, plate2).ratio()
    lev_dist = levenshtein_distance(plate1, plate2)
    lev_sim = 1 - (lev_dist / max(len(plate1), len(plate2))) if max(len(plate1), len(plate2)) > 0 else 0
    return seq_match * 0.6 + lev_sim * 0.4

# ------------------ TEST CLASS ------------------ #
class TestLicensePlateMatching:
    def setup_method(self):
        self.generator = LicensePlateGenerator()
        self.results = {"valid": [], "invalid": []}
        print("\n" + "="*80)
        print("🚀 STARTING LICENSE PLATE MATCHING TESTS")
        print("="*80)

    def teardown_method(self):
        self.generate_summary()

    # ------------------ TESTING METHODS ------------------ #
    def test_valid_plate_matching(self, n_tests=1000):
        print("\n🔧 Testing Valid License Plates...")
        for i in range(n_tests):
            plate = self.generator.generate_valid_plate()
            noisy_plate = plate[:-1] + random.choice(string.ascii_uppercase + string.digits)
            similarity = calculate_similarity(plate, noisy_plate)
            passed = similarity >= 0.7
            self.results["valid"].append((plate, noisy_plate, similarity, passed))
            assert similarity >= 0.6, f"Valid plate similarity too low: {plate} vs {noisy_plate} - {similarity*100:.2f}%"
            if (i+1) % 200 == 0:
                print(f"  Completed {i+1}/{n_tests} valid tests...")

    def test_invalid_plate_matching(self, n_tests=1000):
        print("\n🔧 Testing Invalid License Plates...")
        for i in range(n_tests):
            valid_plate = self.generator.generate_valid_plate()
            invalid_plate = self.generator.generate_invalid_plate()
            similarity = calculate_similarity(valid_plate, invalid_plate)
            passed = similarity < 0.5
            self.results["invalid"].append((valid_plate, invalid_plate, similarity, passed))
            assert similarity < 0.7, f"Invalid plate similarity too high: {valid_plate} vs {invalid_plate} - {similarity*100:.2f}%"
            if (i+1) % 200 == 0:
                print(f"  Completed {i+1}/{n_tests} invalid tests...")

    # ------------------ SUMMARY ------------------ #
    def generate_summary(self):
        def summarize(category):
            data = self.results[category]
            total = len(data)
            passed = sum(1 for r in data if r[3])
            failed = total - passed
            avg_sim = sum(r[2] for r in data)/total*100 if total else 0
            print(f"\n📊 {BOLD}{CYAN}{category.upper()} PLATES SUMMARY{RESET}")
            print(f"Total: {total}, Passed: {GREEN}{passed}{RESET}, Failed: {RED}{failed}{RESET}, Avg Similarity: {BOLD}{avg_sim:.2f}%{RESET}")
            print("Sample cases (first 3):")
            for r in data[:3]:
                color = GREEN if r[3] else RED
                print(f"  {r[0]} vs {r[1]} - {BOLD}{r[2]*100:.2f}%{RESET} - {color}{'PASS' if r[3] else 'FAIL'}{RESET}")

        summarize("valid")
        summarize("invalid")

# ------------------ RUN MANUALLY ------------------ #
if __name__ == "__main__":
    test_instance = TestLicensePlateMatching()
    test_instance.setup_method()
    test_instance.test_valid_plate_matching()
    test_instance.test_invalid_plate_matching()
    test_instance.teardown_method()
    print("\n🎉 ALL TESTS COMPLETED!")
