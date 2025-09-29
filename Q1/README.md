# **License Plate Damage Detection (Q1)**

This program checks front and rear license plate labels to determine whether a vehicle’s license plate is BROKEN/DAMAGED or OK, based on YOLO output files.

# **🔎 How It Works** 

Each vehicle has a front and rear YOLO .txt label file.

The program looks for a specific YOLO class ID (BROKEN_CLASS_ID) that indicates a damaged plate.

Status is evaluated as follows:

Front Status → from the front label file

Rear Status → from the rear label file

Overall Status → BROKEN if either side is broken, otherwise OK

Results are printed in the console and also saved in a CSV file (license_plate_status.csv).

# **⚙️ Configuration** 

At the top of the script, update the following as needed:

FRONT_DIR = Path(r"C:\...\Q1\Broken\Front")   # Folder with front labels
REAR_DIR  = Path(r"C:\...\Q1\Broken\Rear")    # Folder with rear labels
BROKEN_CLASS_ID = 1                           # YOLO class ID for "broken plate"

# **▶️ Usage** 

Place YOLO .txt label files for front and rear plates in their respective folders:

Q1/Broken/Front/car1.txt
Q1/Broken/Rear/car1.txt


# Run the script: 

python broken_plate_check.py


# The program will:

Match vehicles with both front and rear labels.

Check each label for BROKEN_CLASS_ID.

Print results to the console.

Save results in license_plate_status.csv.

# **📊 Example Output** 
Found 12 paired cars.

=== License Plate Status ===
Car        Front      Rear       Overall   
----------------------------------------
car1       BROKEN     OK         BROKEN
car2       OK         BROKEN     BROKEN
car3       BROKEN     BROKEN     BROKEN
...
car12      OK         OK         OK


CSV (license_plate_status.csv):

car,front_status,rear_status,overall_status
car1,BROKEN,OK,BROKEN
car2,OK,BROKEN,BROKEN
car3,BROKEN,BROKEN,BROKEN
...
car12,OK,OK,OK

# **📦 Requirements** 

Python 3.7+

Standard library only (pathlib, csv) – no extra dependencies

# **👤 Author** 

Abdul Nasir

Delloyd Internship 2025
