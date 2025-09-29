from pathlib import Path

# === CONFIG: change only if your class IDs differ ===
FRONT_DIR = Path(r"C:\Users\Home\Desktop\Nasir\Delloyd Internship\Q1\Broken\Front")
REAR_DIR  = Path(r"C:\Users\Home\Desktop\Nasir\Delloyd Internship\Q1\Broken\Rear")
BROKEN_CLASS_ID = 1        # YOLO class ID that means “broken/damaged plate”

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
        return int(''.join(filter(str.isdigit, name)))  # e.g., "car10" -> 10

    common_cars = sorted(front_cars & rear_cars, key=natural_key)
    print(f"Found {len(common_cars)} paired cars.\n")

    results = []
    for car in common_cars:
        front_label = FRONT_DIR / f"{car}.txt"
        rear_label  = REAR_DIR  / f"{car}.txt"

        status = "BROKEN" if (is_broken(front_label) or is_broken(rear_label)) else "OK"
        results.append((car, status))

    print("=== License Plate Status ===")
    for car, status in results:
        print(f"{car}: {status}")

    # Save a CSV summary
    out_file = Path("license_plate_status.csv")
    with out_file.open("w") as f:
        f.write("car,status\n")
        for car, status in results:
            f.write(f"{car},{status}\n")

    print(f"\nResults saved to {out_file.resolve()}")

if __name__ == "__main__":
    main()