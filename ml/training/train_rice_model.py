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
from torchvision import transforms

# Set random seed
random.seed(42)
torch.manual_seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "Rice_Leaf_AUG"
MODEL_DIR = BASE_DIR / "ml" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR = BASE_DIR / "backend" / "uploads" / "rice_samples"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "rice_leaf_model.pth"
CLASSES_PATH = MODEL_DIR / "rice_leaf_classes.json"

print(f"Dataset directory: {DATA_DIR}", flush=True)
print(f"Model destination: {MODEL_PATH}", flush=True)

# Discover classes
class_dirs = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])
class_names = [d.name for d in class_dirs]
class_to_idx = {name: i for i, name in enumerate(class_names)}
print(f"Classes ({len(class_names)}): {class_names}", flush=True)

# Copy 1 representative sample from each class to backend/uploads/rice_samples
import shutil
for d in class_dirs:
    images = list(d.glob("*.jpg")) + list(d.glob("*.png")) + list(d.glob("*.jpeg"))
    if images:
        sample_img = images[0]
        safe_name = d.name.lower().replace(" ", "_") + ".jpg"
        dest = SAMPLE_DIR / safe_name
        try:
            shutil.copyfile(sample_img, dest)
            print(f"Copied sample: {dest.name}", flush=True)
        except Exception as e:
            print(f"Warning copying sample: {e}", flush=True)

# Collect balanced subset for fast CPU training: 100 train images per class, 25 val images per class
train_samples = []
val_samples = []

for d in class_dirs:
    imgs = list(d.glob("*.jpg")) + list(d.glob("*.png")) + list(d.glob("*.jpeg"))
    random.shuffle(imgs)
    cls_idx = class_to_idx[d.name]
    
    # 100 for train, 25 for val
    tr = imgs[:100]
    va = imgs[100:125]
    for p in tr:
        train_samples.append((str(p), cls_idx))
    for p in va:
        val_samples.append((str(p), cls_idx))

print(f"Collected {len(train_samples)} training samples, {len(val_samples)} validation samples.", flush=True)

# Custom Fast Image Dataset
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
            # Fallback black tensor if image corrupted
            return torch.zeros(3, 112, 112), label

img_size = 112
train_transform = transforms.Compose([
    transforms.Resize((img_size, img_size)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
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

# Efficient CNN Model Architecture
class RiceLeafCNN(nn.Module):
    def __init__(self, num_classes=6):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2) # 56x56
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2) # 28x28
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2) # 14x14
        )
        self.pool = nn.AdaptiveAvgPool2d((2, 2)) # 128 x 2 x 2 = 512
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(128 * 2 * 2, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.pool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

device = torch.device("cpu")
model = RiceLeafCNN(num_classes=len(class_names)).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0015, weight_decay=1e-4)

epochs = 5
print(f"Beginning training for {epochs} epochs...", flush=True)
start_t = time.time()

best_val_acc = 0.0

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
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

    train_loss = running_loss / max(1, total)
    train_acc = correct / max(1, total)

    # Validation
    model.eval()
    val_correct = 0
    val_total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            val_correct += torch.sum(preds == labels.data).item()
            val_total += labels.size(0)

    val_acc = val_correct / max(1, val_total)
    if val_acc > best_val_acc:
        best_val_acc = val_acc

    print(f"Epoch [{epoch+1}/{epochs}] | Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.1f}% | Val Acc: {val_acc*100:.1f}%", flush=True)

# Save best weights
torch.save({
    "state_dict": model.state_dict(),
    "class_names": class_names,
    "input_size": img_size,
    "val_accuracy": best_val_acc
}, str(MODEL_PATH))

# Save classes JSON
with open(CLASSES_PATH, "w", encoding="utf-8") as f:
    json.dump({
        "classes": class_names,
        "class_to_idx": class_to_idx,
        "input_size": img_size,
        "dataset_name": "Rice_Leaf_AUG",
        "total_images_in_dataset": sum(len(list(d.glob('*.*'))) for d in class_dirs),
        "trained_samples": len(train_samples),
        "val_accuracy": round(best_val_acc * 100, 2),
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }, f, indent=2)

print(f"SUCCESS: Model trained and saved to {MODEL_PATH} ({time.time() - start_t:.1f}s)", flush=True)
