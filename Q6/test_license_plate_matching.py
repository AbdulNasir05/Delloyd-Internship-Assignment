import random
import string
import time
import pytest
from difflib import SequenceMatcher
import sys

class LicensePlateGenerator:
    """Generates valid and invalid Indian license plates."""

    def generate_valid_plate(self):
        """Generate a valid format Indian plate (e.g., MH12AB1234)."""
        state = ''.join(random.choices(string.ascii_uppercase, k=2))
        district = ''.join(random.choices(string.digits, k=2))
        series = ''.join(random.choices(string.ascii_uppercase, k=2))
        number = ''.join(random.choices(string.digits, k=4))
        return f"{state}{district}{series}{number}"

    def generate_invalid_plate(self):
        """Generate an invalid plate (random messy string)."""
        length = random.randint(5, 12)
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=length))


# ---------------- SIMILARITY FUNCTIONS ---------------- #

def levenshtein_distance(s1, s2):
    """Compute Levenshtein distance."""
    s1, s2 = s1.upper(), s2.upper()  # normalize to uppercase
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
    s1, s2 = s1.upper(), s2.upper()  # normalize to uppercase
    set1, set2 = set(s1), set(s2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0


def calculate_similarity(plate1, plate2):
    """Calculate weighted similarity between two plates."""
    plate1, plate2 = plate1.upper(), plate2.upper()  # normalize

    # Handle edge case: both empty
    if not plate1 and not plate2:
        return 1.0  # 100% similar

    # Handle case: one empty, one not
    if not plate1 or not plate2:
        return 0.0  # 0% similar

    seq_match = SequenceMatcher(None, plate1, plate2).ratio()
    lev_dist = levenshtein_distance(plate1, plate2)
    lev_sim = 1 - (lev_dist / max(len(plate1), len(plate2))) if max(len(plate1), len(plate2)) > 0 else 0

    # Weighted combo
    return (seq_match * 0.6 + lev_sim * 0.4)

# ---------------- TEST CLASS ---------------- #

class TestLicensePlateMatching:
    def setup_method(self):
        self.generator = LicensePlateGenerator()
        self.results = {
            "valid": {"total": 0, "passed": 0, "failed": 0, "similarities": [], "details": []},
            "invalid": {"total": 0, "passed": 0, "failed": 0, "similarities": [], "details": []},
        }
        print("\n" + "="*80)
        print("🚀 STARTING LICENSE PLATE MATCHING TESTS")
        print("="*80)

    def teardown_method(self):
        self.generate_test_report()

    def generate_test_report(self):
        """Generate comprehensive test report that will be visible"""
        # Force output to be displayed
        sys.stdout.flush()
        
        print("\n" + "="*80)
        print("📊 LICENSE PLATE MATCHING TEST REPORT")
        print("="*80)

        total_tests = self.results["valid"]["total"] + self.results["invalid"]["total"]
        total_passed = self.results["valid"]["passed"] + self.results["invalid"]["passed"]
        success_rate = (total_passed / total_tests * 100) if total_tests else 0

        print("\n📈 OVERALL STATISTICS:")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {total_passed}")
        print(f"Failed: {total_tests - total_passed}")
        print(f"Success Rate: {success_rate:.2f}%")

        # Valid plates detailed report
        valid = self.results["valid"]
        print(f"\n✅ VALID LICENSE PLATES TESTING:")
        print(f"Tests: {valid['total']}")
        print(f"Passed: {valid['passed']}")
        print(f"Failed: {valid['failed']}")
        if valid['total'] > 0:
            print(f"Success Rate: {(valid['passed'] / valid['total'] * 100):.2f}%")
            
            # Similarity statistics for valid plates
            if valid["similarities"]:
                avg_sim = sum(valid["similarities"]) / len(valid["similarities"]) * 100
                min_sim = min(valid["similarities"]) * 100
                max_sim = max(valid["similarities"]) * 100
                print(f"Similarity - Avg: {avg_sim:.2f}%, Max: {max_sim:.2f}%, Min: {min_sim:.2f}%")

        # Invalid plates detailed report
        invalid = self.results["invalid"]
        print(f"\n❌ INVALID LICENSE PLATES TESTING:")
        print(f"Tests: {invalid['total']}")
        print(f"Passed: {invalid['passed']}")
        print(f"Failed: {invalid['failed']}")
        if invalid['total'] > 0:
            print(f"Success Rate: {(invalid['passed'] / invalid['total'] * 100):.2f}%")
            
            # Similarity statistics for invalid plates
            if invalid["similarities"]:
                avg_sim = sum(invalid["similarities"]) / len(invalid["similarities"]) * 100
                min_sim = min(invalid["similarities"]) * 100
                max_sim = max(invalid["similarities"]) * 100
                print(f"Similarity - Avg: {avg_sim:.2f}%, Max: {max_sim:.2f}%, Min: {min_sim:.2f}%")

        # Sample test cases
        self.print_sample_cases()
        
        # Failed cases summary
        self.print_failed_cases()

    def print_sample_cases(self):
        """Print sample test cases"""
        print(f"\n🔍 SAMPLE TEST CASES:")
        
        # Valid plates samples
        if self.results["valid"]["details"]:
            print(f"Valid Plate Examples (First 3):")
            for i, detail in enumerate(self.results["valid"]["details"][:3]):
                status = "✅ PASS" if detail["passed"] else "❌ FAIL"
                print(f"  {i+1}. {detail['plate1']} vs {detail['plate2']} - {detail['similarity']*100:.2f}% - {status}")
        
        # Invalid plates samples
        if self.results["invalid"]["details"]:
            print(f"Invalid Plate Examples (First 3):")
            for i, detail in enumerate(self.results["invalid"]["details"][:3]):
                status = "✅ PASS" if detail["passed"] else "❌ FAIL"
                print(f"  {i+1}. {detail['plate1']} vs {detail['plate2']} - {detail['similarity']*100:.2f}% - {status}")

    def print_failed_cases(self):
        """Print failed test cases"""
        failed_valid = [d for d in self.results["valid"]["details"] if not d["passed"]]
        failed_invalid = [d for d in self.results["invalid"]["details"] if not d["passed"]]
        
        if failed_valid:
            print(f"\n⚠️  Failed Valid Plate Cases:")
            for i, detail in enumerate(failed_valid[:5]):  # Show first 5 failures
                print(f"  {detail['plate1']} vs {detail['plate2']} - {detail['similarity']*100:.2f}%")
        
        if failed_invalid:
            print(f"\n⚠️  Failed Invalid Plate Cases:")
            for i, detail in enumerate(failed_invalid[:5]):  # Show first 5 failures
                print(f"  {detail['plate1']} vs {detail['plate2']} - {detail['similarity']*100:.2f}%")

    # ---------------- ACTUAL TESTS ---------------- #

    def test_valid_plate_matching(self):
        """Test 1000 valid license plate pairs"""
        print("\n🔧 Testing Valid License Plate Matching (1000 pairs)...")
        
        for i in range(1000):  # Increased to 1000 tests
            plate = self.generator.generate_valid_plate()
            # Create a similar plate with minor variation
            if len(plate) > 1:
                # Change last character
                noisy_plate = plate[:-1] + random.choice(string.ascii_uppercase + string.digits)
            else:
                noisy_plate = plate + random.choice(string.ascii_uppercase + string.digits)

            similarity = calculate_similarity(plate, noisy_plate)
            
            # Store detailed information
            test_detail = {
                "plate1": plate,
                "plate2": noisy_plate,
                "similarity": similarity,
                "passed": similarity >= 0.7
            }
            
            self.results["valid"]["total"] += 1
            self.results["valid"]["similarities"].append(similarity)
            self.results["valid"]["details"].append(test_detail)

            if similarity >= 0.7:
                self.results["valid"]["passed"] += 1
            else:
                self.results["valid"]["failed"] += 1

            # Assertion for pytest
            assert similarity >= 0.6, f"Valid plate similarity too low: {plate} vs {noisy_plate} - {similarity*100:.2f}%"
            
            # Progress indicator for large test runs
            if (i + 1) % 200 == 0:
                print(f"  Completed {i + 1}/1000 valid plate tests...")

    def test_invalid_plate_matching(self):
        """Test 1000 invalid license plate pairs"""
        print("\n🔧 Testing Invalid License Plate Matching (1000 pairs)...")
        
        for i in range(1000):  # Increased to 1000 tests
            valid_plate = self.generator.generate_valid_plate()
            invalid_plate = self.generator.generate_invalid_plate()

            similarity = calculate_similarity(valid_plate, invalid_plate)
            
            # Store detailed information
            test_detail = {
                "plate1": valid_plate,
                "plate2": invalid_plate,
                "similarity": similarity,
                "passed": similarity < 0.5
            }
            
            self.results["invalid"]["total"] += 1
            self.results["invalid"]["similarities"].append(similarity)
            self.results["invalid"]["details"].append(test_detail)

            if similarity < 0.5:
                self.results["invalid"]["passed"] += 1
            else:
                self.results["invalid"]["failed"] += 1

            # Assertion for pytest
            assert similarity < 0.7, f"Invalid plate similarity too high: {valid_plate} vs {invalid_plate} - {similarity*100:.2f}%"
            
            # Progress indicator for large test runs
            if (i + 1) % 200 == 0:
                print(f"  Completed {i + 1}/1000 invalid plate tests...")

# ---------------- EDGE CASES ---------------- #

def test_edge_cases():
    print("\n🔧 Testing Edge Cases...")

    edge_cases = [
        ("", "", 100.0, "Empty strings"),
        ("AB1234", "", 0.0, "One empty string"),
        ("AB1234", "AB1234", 100.0, "Exact match"),
        ("AB1234", "AB1235", 83.0, "Single digit difference"),
        ("AB1234", "AC1234", 83.0, "Single letter difference"),
        ("ab12cd3456", "AB12CD3456", 100.0, "Case difference (normalized)"),
    ]

    for plate1, plate2, expected_similarity, description in edge_cases:
        similarity = calculate_similarity(plate1, plate2) * 100
        print(f"  Edge Case: {description} | {plate1} vs {plate2} => {similarity:.2f}%")
        assert abs(similarity - expected_similarity) <= 20, f"Edge case failed: {description}"

# ---------------- PERFORMANCE TEST ---------------- #

def test_performance():
    print("\n🔧 Testing Performance (1000 operations)...")
    start_time = time.time()

    generator = LicensePlateGenerator()
    for i in range(1000):
        plate1 = generator.generate_valid_plate()
        plate2 = generator.generate_valid_plate()
        calculate_similarity(plate1, plate2)
        
        # Progress indicator
        if (i + 1) % 200 == 0:
            print(f"  Completed {i + 1}/1000 similarity calculations...")

    elapsed = time.time() - start_time
    print(f"✅ Performance test completed in {elapsed:.4f} seconds")
    assert elapsed < 5, f"Performance test took too long: {elapsed:.2f} seconds!"

# ---------------- RUN DIRECTLY ---------------- #

if __name__ == "__main__":
    print("🚀 RUNNING LICENSE PLATE TESTS DIRECTLY")
    print("="*50)
    
    # Create test instance and run manually
    test_instance = TestLicensePlateMatching()
    test_instance.setup_method()
    
    try:
        test_instance.test_valid_plate_matching()
        test_instance.test_invalid_plate_matching()
        print("✅ All main tests completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    test_instance.teardown_method()
    
    # Run additional tests
    print("\n" + "="*50)
    print("RUNNING ADDITIONAL TESTS")
    print("="*50)
    
    test_edge_cases()
    test_performance()
    
    print("\n🎉 ALL TESTS COMPLETED!")