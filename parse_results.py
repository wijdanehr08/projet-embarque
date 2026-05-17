import json, os, csv

vms = ["vm1", "vm2", "vm3"]
models = ["baseline_full.pt", "q1_dynamic_full.pt", "q2_ptq_full.pt", "q3_qat_full.pt",
          "q4_weightonly_full.pt", "q5_mixed_full.pt", "p1_unstructured_full.pt",
          "p2_structured_full.pt", "p3_magnitude_full.pt"]

rows = []
for vm in vms:
    for m in models:
        fname = f"C:\\projet_iot\\{vm}_{m}.json"
        if os.path.exists(fname):
            with open(fname) as f:
                content = f.read()
            try:
                data = json.loads(content[content.index('{'):])
                rows.append({
                    "VM": vm.upper(),
                    "Technique": m.replace("_full.pt",""),
                    "Prediction": data.get("prediction",""),
                    "Confidence": data.get("confidence",""),
                    "Inference_mean_ms": data.get("inference_mean_ms",""),
                    "Inference_std_ms": data.get("inference_std_ms",""),
                    "CPU_percent": data.get("cpu_percent",""),
                    "RAM_mb": data.get("ram_mb","")
                })
                print(f"✅ {vm} - {m}")
            except Exception as e:
                print(f"❌ {vm} - {m}: {e}")
        else:
            print(f"❌ Manquant: {fname}")

with open("C:\\projet_iot\\matrix_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"\n✅ matrix_results.csv généré! ({len(rows)} lignes)")