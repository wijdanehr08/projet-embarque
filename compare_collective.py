import json, csv

with open("C:\\projet_iot\\collective_results.json") as f:
    results = json.load(f)

consensus_rate = sum(r["consensus"] for r in results) / len(results)
avg_conf = sum(r["collective_confidence"] for r in results) / len(results)

print(f"Taux de consensus : {consensus_rate:.1%}")
print(f"Confiance moyenne : {avg_conf:.4f}")

with open("C:\\projet_iot\\collective_comparison.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["test","collective_prediction","collective_confidence","consensus"])
    writer.writeheader()
    for r in results:
        writer.writerow({
            "test": r["test"],
            "collective_prediction": r["collective_prediction"],
            "collective_confidence": r["collective_confidence"],
            "consensus": r["consensus"]
        })
print("✅ collective_comparison.csv sauvegardé!")