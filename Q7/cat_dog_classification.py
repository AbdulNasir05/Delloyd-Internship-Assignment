import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import csv

# ---------- SETTINGS ----------
image_folder = r"C:\Users\Home\Desktop\Nasir\Delloyd Internship\Q7\dog_cat_images"
report_name = "dog_cat_classification_report.pdf"
csv_name = "classification_results.csv"

# ---------- MODEL ----------
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model = model.to(device).eval()

# Load ImageNet class labels
from torchvision.models import ResNet50_Weights
categories = ResNet50_Weights.DEFAULT.meta["categories"]

# Predefined dog & cat classes (using ImageNet index ranges)
# Dog breeds = indices 151–268 (118 classes)
dog_indices = list(range(151, 269))
dog_classes = [categories[i] for i in dog_indices]

# Domestic cats = indices 281–285 (5 classes)
cat_indices = list(range(281, 286))
cat_classes = [categories[i] for i in cat_indices]


# ---------- TRANSFORMS ----------
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

# ---------- PREDICTION FUNCTION ----------
def predict_image(img_path):
    img = Image.open(img_path).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        out = model(x)
    probs = torch.nn.functional.softmax(out[0], dim=0)
    top_prob, top_id = torch.topk(probs, 1)
    return categories[top_id], float(top_prob)

# ---------- CLASSIFICATION ----------
predicted_cats, predicted_dogs, misclassified = [], [], []

for fname in os.listdir(image_folder):
    if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".jfif", ".webp")):
        continue

    img_path = os.path.join(image_folder, fname)
    label, conf = predict_image(img_path)  # get top1 only

    if label in dog_classes:
        marker = "[DOG]"
        output = f"{marker} {fname}  -->  {label}"
        predicted_dogs.append((fname, label))
    elif label in cat_classes:
        marker = "[CAT]"
        output = f"{marker} {fname}  -->  {label}"
        predicted_cats.append((fname, label))
    else:
        marker = "[Misclassified DOg]"
        output = f"{marker} {fname}  -->  {label}"
        misclassified.append((fname, label))

    print(output)

# ---------- PDF REPORT ----------
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(report_name, pagesize=A4)
story = []

story.append(Paragraph("<b>Dog & Cat Image Classification Report</b>", styles['Title']))
story.append(Spacer(1, 12))

total_images = len([f for f in os.listdir(image_folder)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.jfif', '.webp'))])
story.append(Paragraph(f"Total images checked: {total_images}", styles['Normal']))
story.append(Paragraph(f"Predicted as dogs: {len(predicted_dogs)}", styles['Normal']))
story.append(Paragraph(f"Predicted as cats: {len(predicted_cats)}", styles['Normal']))
story.append(Paragraph(f"Other: {len(misclassified)}", styles['Normal']))
story.append(Spacer(1, 12))

if predicted_dogs:
    story.append(Paragraph("<b>Dog Predictions</b>", styles['Heading2']))
    for fname, label in predicted_dogs:
        story.append(Paragraph(f"{fname}: {label}", styles['Normal']))
    story.append(Spacer(1, 12))

if predicted_cats:
    story.append(Paragraph("<b>Cat Predictions</b>", styles['Heading2']))
    for fname, label in predicted_cats:
        story.append(Paragraph(f"{fname}: {label}", styles['Normal']))
    story.append(Spacer(1, 12))

if misclassified:
    story.append(Paragraph("<b>Other Predictions</b>", styles['Heading2']))
    for fname, label in misclassified:
        story.append(Paragraph(f"{fname}: {label}", styles['Normal']))
    story.append(Spacer(1, 12))

doc.build(story)
print(f"\nPDF report saved as: {report_name}")

# ---------- CSV REPORT ----------
with open(csv_name, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Image", "Category", "Label"])

    for fname, label in predicted_dogs:
        writer.writerow([fname, "DOG", label])
    for fname, label in predicted_cats:
        writer.writerow([fname, "CAT", label])
    for fname, label in misclassified:
        writer.writerow([fname, "MIsclassified Dog", label])

print(f"CSV results saved as: {csv_name}")
