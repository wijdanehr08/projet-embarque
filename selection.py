import csv

# Charger les résultats
rows = []
with open("C:\\projet_iot\\matrix_results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# Normaliser les métriques (0-1, plus petit = meilleur pour RAM/CPU/inférence)
def normalize(values, inverse=False):
    mn, mx = min(values), max(values)
    if mx == mn:
        return [1.0]*len(values)
    if inverse:
        return [(mx-v)/(mx-mn) for v in values]
    return [(v-mn)/(mx-mn) for v in values]

for vm_name, weights in [("VM1", {"ram":0.40,"cpu":0.40,"acc":0.20}),
                          ("VM2", {"ram":0.30,"cpu":0.30,"acc":0.40}),
                          ("VM3", {"ram":0.15,"cpu":0.25,"acc":0.60})]:
    vm_rows = [r for r in rows if r["VM"]==vm_name]
    
    rams  = [float(r["RAM_mb"]) for r in vm_rows]
    cpus  = [float(r["CPU_percent"]) for r in vm_rows]
    accs  = [float(r["Confidence"]) for r in vm_rows]
    infs  = [float(r["Inference_mean_ms"]) for r in vm_rows]
    
    ram_n = normalize(rams, inverse=True)
    cpu_n = normalize(cpus, inverse=True)
    acc_n = normalize(accs, inverse=False)
    
    scores = []
    for i, r in enumerate(vm_rows):
        if vm_name == "VM1":
            score = weights["ram"]*ram_n[i] + weights["cpu"]*cpu_n[i] + weights["acc"]*acc_n[i]
        elif vm_name == "VM2":
            inf_n = normalize(infs, inverse=True)
            score = weights["ram"]*ram_n[i] + weights["cpu"]*inf_n[i] + weights["acc"]*acc_n[i]
        else:
            inf_n = normalize(infs, inverse=True)
            score = weights["acc"]*acc_n[i] + weights["cpu"]*inf_n[i] + weights["ram"]*ram_n[i]
        scores.append((score, r["Technique"], r))
    
    scores.sort(reverse=True)
    best = scores[0]
    print(f"\n{'='*50}")
    print(f"{vm_name} - Meilleure technique: {best[1]}")
    print(f"  Score: {best[0]:.4f}")
    print(f"  RAM: {best[2]['RAM_mb']} Mo")
    print(f"  CPU: {best[2]['CPU_percent']}%")
    print(f"  Inférence: {best[2]['Inference_mean_ms']} ms")
    print(f"  Confidence: {best[2]['Confidence']}")
    print(f"\nTop 3:")
    for s, t, r in scores[:3]:
        print(f"  {t}: {s:.4f}")