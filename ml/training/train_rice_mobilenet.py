import os
import sys
import json
import time
import random
from pathlib import Path
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models

random.seed(42)
torch.manual_seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "Rice_Leaf_AUG"
MODEL_DIR = BASE_DIR / "ml" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR = BASE_DIR / "backend" / "uploads" / "rice_samples"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "rice_leaf_mobilenet.pth"
CLASSES_PATH = MODEL_DIR / "rice_leaf_classes.json"

print(f"Data Dir: {DATA_DIR}")
print(f"Target Model: {MODEL_PATH}")

class_dirs = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])
class_names = [d.name for d in class_dirs]
class_to_idx = {name: i for i, name in enumerate(class_names)}
print(f"Found {len(class_names)} classes: {class_names}")

# Copy 1 high quality sample from each class into sample dir for UI/API
import shutil
for d in class_dirs:
    images = list(d.glob("*.jpg")) + list(d.glob("*.png")) + list(d.glob("*.jpeg"))
    if images:
        sample_img = images[0]
        safe_name = d.name.lower().replace(" ", "_") + ".jpg"
        dest = SAMPLE_DIR / safe_name
        try:
            shutil.copyfile(sample_img, dest)
            print(f"Sample copied: {dest.name}")
        except Exception as e:
            print(f"Error copying sample: {e}")

# Sample 150 images per class for train, 35 for validation
train_samples = []
val_samples = []

for d in class_dirs:
    imgs = list(d.glob("*.jpg")) + list(d.glob("*.png")) + list(d.glob("*.jpeg"))
    random.shuffle(imgs)
    cls_idx = class_to_idx[d.name]
    tr = imgs[:150]
    va = imgs[150:185]
    for p in tr:
        train_samples.append((str(p), cls_idx))
    for p in va:
        val_samples.append((str(p), cls_idx))

print(f"Train samples: {len(train_samples)}, Val samples: {len(val_samples)}")

class FastLeafDataset(Dataset):
    def __init__(self, samples, transform=None):
        self.samples = samples
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        try:
            with Image.open(path) as img:
                img = img.convert("RGB")
                if self.transform:
                    img = self.transform(img)
                return img, label
        except Exception:
            return torch.zeros(3, 160, 160), label

img_size = 160
train_transform = transforms.Compose([
    transforms.Resize((img_size, img_size)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((img_size, img_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_dataset = FastLeafDataset(train_samples, transform=train_transform)
val_dataset = FastLeafDataset(val_samples, transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=0)

# Pretrained MobileNetV2 with transfer learning
device = torch.device("cpu")
model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

# Freeze base features initially, replace classifier
for param in model.features.parameters():
    param.requires_grad = False

num_ftrs = model.classifier[1].in_features
model.classifier = nn.Sequential(
    nn.Dropout(0.2),
    nn.Linear(num_ftrs, 128),
    nn.ReLU(inplace=True),
    nn.Dropout(0.2),
    nn.Linear(128, len(class_names))
)
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.classifier.parameters(), lr=0.003, weight_decay=1e-4)

epochs = 5
print(f"Stage 1: Training classifier head for {epochs} epochs...")
best_acc = 0.0
best_state = None

for epoch in range(epochs):
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * inputs.size(0)
        _, preds = torch.max(outputs, 1)
        correct += torch.sum(preds == labels.data).item()
        total += labels.size(0)

    train_acc = correct / max(1, total)

    model.eval()
    val_correct, val_total = 0, 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            val_correct += torch.sum(preds == labels.data).item()
            val_total += labels.size(0)

    val_acc = val_correct / max(1, val_total)
    print(f"Epoch [{epoch+1}/{epochs}] | Loss: {running_loss/max(1,total):.4f} | Train Acc: {train_acc*100:.1f}% | Val Acc: {val_acc*100:.1f}%")
    if val_acc > best_acc:
        best_acc = val_acc
        best_state = {k: v.cpu() for k, v in model.state_dict().items()}

# Unfreeze top feature layers for fine-tuning
for param in model.features[-3:].parameters():
    param.requires_grad = True

optimizer = optim.Adam([
    {"params": model.features[-3:].parameters(), "lr": 0.0003},
    {"params": model.classifier.parameters(), "lr": 0.001}
], weight_decay=1e-4)

fine_epochs = 3
print(f"Stage 2: Fine-tuning top layers for {fine_epochs} epochs...")
for epoch in range(fine_epochs):
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * inputs.size(0)
        _, preds = torch.max(outputs, 1)
        correct += torch.sum(preds == labels.data).item()
        total += labels.size(0)

    model.eval()
    val_correct, val_total = 0, 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            val_correct += torch.sum(preds == labels.data).item()
            val_total += labels.size(0)

    val_acc = val_correct / max(1, val_total)
    print(f"Fine Epoch [{epoch+1}/{fine_epochs}] | Train Acc: {correct/max(1,total)*100:.1f}% | Val Acc: {val_acc*100:.1f}%")
    if val_acc > best_acc:
        best_acc = val_acc
        best_state = {k: v.cpu() for k, v in model.state_dict().items()}

# Save best weights
torch.save({
    "state_dict": best_state or model.state_dict(),
    "class_names": class_names,
    "input_size": img_size,
    "backbone": "mobilenet_v2",
    "val_accuracy": round(best_acc * 100, 2)
}, str(MODEL_PATH))

# Update classes metadata JSON
with open(CLASSES_PATH, "w", encoding="utf-8") as f:
    json.dump({
        "classes": class_names,
        "class_to_idx": class_to_idx,
        "input_size": img_size,
        "backbone": "mobilenet_v2",
        "dataset_name": "Rice_Leaf_AUG",
        "total_images_in_dataset": sum(len(list(d.glob('*.*'))) for d in class_dirs),
        "trained_samples": len(train_samples),
        "val_accuracy": round(best_acc * 100, 2),
        "model_file": "rice_leaf_mobilenet.pth",
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }, f, indent=2)

print(f"SUCCESS: Saved MobileNetV2 model to {MODEL_PATH} with validation accuracy {best_acc*100:.1f}%")
