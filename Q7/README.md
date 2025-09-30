# Q7 – Dog & Cat Image Classification
# ** 📌 Objective **

This program uses a pre-trained ResNet50 model from PyTorch to classify images of dogs and cats from a given folder. It then generates a PDF report and a CSV file summarizing the classification results.

# ** ⚙️ Features **

Loads and applies a ResNet50 pre-trained on ImageNet.

Classifies images as Dog, Cat, or Misclassified (other animal/object).

Prints classification results directly in the terminal.

Saves a PDF report with counts and detailed classifications.

Generates a CSV file containing all classification results.

# ** 📂 Input **

A folder containing images (.jpg, .jpeg, .png, .jfif, .webp).

Images of cats or dogs (other animals may be detected as misclassified).

Example Input Folder (dog_cat_images):

dog1.jpg

dog2.png

cat1.jpeg

random_animal.webp

# ** 📤 Output **

1️⃣ Console Output

Each image is printed with its classification:

[DOG] dog1.jpg  -->  Eskimo dog

[DOG] dog2.png  -->  boxer

[CAT] cat1.jpeg  -->  tabby cat

[Misclassified DOg] random_animal.webp  -->  red panda

2️⃣ PDF Report (dog_cat_classification_report.pdf)

Includes:

Total images checked

Number of dogs, cats, and misclassified items

Detailed predictions for each category

Sample Extract:

Dog & Cat Image Classification Report

Total images checked: 10

Predicted as dogs: 6

Predicted as cats: 3

Other: 1

Dog Predictions

dog1.jpg: Eskimo dog

dog2.png: boxer

Cat Predictions

cat1.jpeg: tabby cat

Other Predictions

random_animal.webp: red panda

3️⃣ CSV Report (classification_results.csv)

Contains structured results:

Image	Category	Label

dog1.jpg	DOG	Eskimo dog

dog2.png	DOG	boxer

cat1.jpeg	CAT	tabby cat

random_animal.webp	MIsclassified Dog	red panda

# ** 🛠️ How It Works **

Load ResNet50 with ImageNet weights.

Preprocess images (resize, crop, normalize).

Perform classification with softmax.

Identify:

Dogs → ImageNet classes 151–268

Cats → ImageNet classes 281–285

Other → Anything outside these ranges

Save results into PDF and CSV.

# ** ▶️ Usage **

Place all images inside the folder:

C:\Users\Home\Desktop\Nasir\Delloyd Internship\Q7\dog_cat_images


Run the script:

python q7_dog_cat_classifier.py


Check generated files:

dog_cat_classification_report.pdf

classification_results.csv

# ** 👨‍💻 Author **

Abdul Nasir

Delloyd Internship 2025
