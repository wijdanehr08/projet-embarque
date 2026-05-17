import requests, json, time, subprocess

THINGSBOARD_HOST = "http://localhost:9090"

DEVICES = {
    "VM1": {"token": "EqmxyZfS1sBN0ZGsFl55", "model": "p2_structured_full.pt", "cpus": "1.0", "memory": "500m", "image": "projet_iot-vm1"},
    "VM2": {"token": "BIfEWNxfwqSIhomF4l74", "model": "p1_unstructured_full.pt", "cpus": "2.0", "memory": "1g", "image": "projet_iot-vm2"},
    "VM3": {"token": "ze8ZXAznpt68a2uA38iA", "model": "p2_structured_full.pt", "cpus": "2.0", "memory": "2g", "image": "projet_iot-vm3"},
}

def run_inference(vm_name, cfg):
    cmd = ["docker", "run", "--rm", f"--cpus={cfg['cpus']}", f"--memory={cfg['memory']}",
           "-v", "C:\\projet_iot\\models:/models",
           "-e", f"MODEL_PATH=/models/{cfg['model']}",
           cfg["image"], "python", "infer.py"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    try:
        return json.loads(output[output.index('{'):])
    except:
        return None

def send_telemetry(token, payload):
    url = f"{THINGSBOARD_HOST}/api/v1/{token}/telemetry"
    r = requests.post(url, json=payload)
    return r.status_code == 200

print("Démarrage envoi télémétrie ThingsBoard via HTTP...")

for i in range(5):
    print(f"\n--- Cycle {i+1}/5 ---")
    for vm_name, cfg in DEVICES.items():
        data = run_inference(vm_name, cfg)
        if data:
            payload = {
                "vm_id": vm_name,
                "technique": cfg["model"].replace("_full.pt",""),
                "prediction": data["prediction"],
                "confidence": data["confidence"],
                "inference_time_ms": data["inference_mean_ms"],
                "cpu_usage_pct": data["cpu_percent"],
                "ram_usage_mb": data["ram_mb"]
            }
            ok = send_telemetry(cfg["token"], payload)
            print(f"  {vm_name} → {data['prediction']} ({data['confidence']:.3f}) | HTTP: {'✅' if ok else '❌'}")
    time.sleep(2)

print("\n✅ Télémétrie terminée!")