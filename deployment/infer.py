import torch, time, psutil, os, json, sys
import torchvision.transforms as transforms
from PIL import Image

MODEL_PATH = os.environ.get("MODEL_PATH", "/models/baseline_best.pt")
CLASS_NAMES = ['COVID', 'Lung_Opacity', 'Normal', 'Viral Pneumonia']

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

print(f"Chargement: {MODEL_PATH}")
model = torch.load(MODEL_PATH, map_location="cpu")
model.eval()

# 10 inférences sur une image test
img = torch.randn(1, 3, 224, 224)
times = []
for _ in range(10):
    start = time.time()
    with torch.no_grad():
        out = model(img)
    times.append((time.time()-start)*1000)

ram = psutil.Process().memory_info().rss / 1024 / 1024
cpu = psutil.cpu_percent(interval=1)
pred = CLASS_NAMES[out.argmax().item()]
conf = torch.softmax(out, dim=1).max().item()

result = {
    "model": MODEL_PATH,
    "prediction": pred,
    "confidence": round(conf, 4),
    "inference_mean_ms": round(sum(times)/len(times), 2),
    "inference_std_ms": round((sum((t-sum(times)/len(times))**2 for t in times)/len(times))**0.5, 2),
    "cpu_percent": cpu,
    "ram_mb": round(ram, 1)
}

print(json.dumps(result, indent=2))