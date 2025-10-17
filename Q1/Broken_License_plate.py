from pathlib import Path

# === CONFIG: change only if your class IDs differ ===
FRONT_DIR = Path(r"C:\Users\Abdul Muizz\Downloads\Delloyd-Internship-Assignment-main\Q1\Broken\Front")
REAR_DIR  = Path(r"C:\Users\Abdul Muizz\Downloads\Delloyd-Internship-Assignment-main\Q1\Broken\Rear")
BROKEN_CLASS_ID = 0  # YOLO class ID that means “broken/damaged plate”


def is_broken(label_file: Path) -> bool:
    """
    Return True if the YOLO label file contains a BROKEN_CLASS_ID.
    If the label file is missing, treat as not broken.
    """
    if not label_file.exists():
        print(f"[WARN] Missing label: {label_file}")
        return False

    with label_file.open("r") as f:
        for line in f:
            parts = line.strip().split()
            if parts and int(parts[0]) == BROKEN_CLASS_ID:
                return True
    return False


def main():
    # collect filenames (stem = base name without extension)
    front_cars = {p.stem for p in FRONT_DIR.glob("*.txt")}
    rear_cars  = {p.stem for p in REAR_DIR.glob("*.txt")}

    # only process cars that have both front and rear labels
    def natural_key(name: str):
        digits = ''.join(filter(str.isdigit, name))
        return int(digits) if digits else 0

    common_cars = sorted(front_cars & rear_cars, key=natural_key)
    print(f"Found {len(common_cars)} paired cars.\n")

    results = []
    for car in common_cars:
        front_label = FRONT_DIR / f"{car}.txt"
        rear_label  = REAR_DIR  / f"{car}.txt"

        front_broken = is_broken(front_label)
        rear_broken  = is_broken(rear_label)

        overall_status = "BROKEN" if (front_broken or rear_broken) else "OK"

        results.append((car, front_broken, rear_broken, overall_status))

    # === Display the results ===
    print("=== License Plate Status ===")
    print(f"{'Car':<10}{'Front Broken':<15}{'Rear Broken':<15}{'Overall Status'}")
    print("-" * 55)
    for car, front_broken, rear_broken, status in results:
        print(f"{car:<10}{'Yes' if front_broken else 'No':<15}{'Yes' if rear_broken else 'No':<15}{status}")

    # === Save a CSV summary ===
    out_file = Path(r"C:\Users\Abdul Muizz\Downloads\Delloyd-Internship-Assignment-main\Q1\license_plate_status.csv")
    with out_file.open("w") as f:
        f.write("car,front_broken,rear_broken,overall_status\n")
        for car, front_broken, rear_broken, status in results:
            f.write(f"{car},{front_broken},{rear_broken},{status}\n")
    
    print(f"\nResults saved to {out_file.resolve()}")


if __name__ == "__main__":
    main()
