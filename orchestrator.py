import json, subprocess, os
import torch.nn.functional as F

# Meilleurs modèles par VM
VM_MODELS = {
    "VM1": "p2_structured_full.pt",
    "VM2": "p1_unstructured_full.pt", 
    "VM3": "p2_structured_full.pt"
}

VM_CONFIG = {
    "VM1": {"cpus": "1.0", "memory": "500m", "image": "projet_iot-vm1"},
    "VM2": {"cpus": "2.0", "memory": "1g",   "image": "projet_iot-vm2"},
    "VM3": {"cpus": "2.0", "memory": "2g",   "image": "projet_iot-vm3"}
}

CLASS_NAMES = ['COVID', 'Lung_Opacity', 'Normal', 'Viral Pneumonia']

def run_inference(vm, model_file):
    cfg = VM_CONFIG[vm]
    cmd = [
        "docker", "run", "--rm",
        f"--cpus={cfg['cpus']}",
        f"--memory={cfg['memory']}",
        "-v", "C:\\projet_iot\\models:/models",
        "-e", f"MODEL_PATH=/models/{model_file}",
        cfg["image"], "python", "infer.py"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    try:
        data = json.loads(output[output.index('{'):])
        return data
    except:
        print(f"Erreur {vm}: {output}")
        return None

def collective_inference(n_tests=10):
    print("="*60)
    print("INTELLIGENCE COLLECTIVE - VOTE PONDÉRÉ")
    print("="*60)
    
    results = []
    agreements = 0
    
    for test_i in range(n_tests):
        print(f"\nTest {test_i+1}/{n_tests}")
        votes = {}
        confidences = {}
        ram_usage = {}
        
        for vm, model in VM_MODELS.items():
            data = run_inference(vm, model)
            if data:
                votes[vm] = data["prediction"]
                confidences[vm] = data["confidence"]
                ram_usage[vm] = data["ram_mb"]
                print(f"  {vm}: {data['prediction']} ({data['confidence']:.3f}) | RAM:{data['ram_mb']}Mo | Inf:{data['inference_mean_ms']}ms")

        # Vote pondéré par confiance
        score_map = {}
        for vm in votes:
            pred = votes[vm]
            weight = confidences[vm]
            score_map[pred] = score_map.get(pred, 0) + weight

        collective_pred = max(score_map, key=score_map.get)
        collective_conf = score_map[collective_pred] / sum(score_map.values())
        
        # Vérifier consensus
        all_preds = list(votes.values())
        consensus = len(set(all_preds)) == 1
        if consensus:
            agreements += 1
        
        # Alerte si confiance < 70%
        if collective_conf < 0.70:
            print(f"  ⚠️ Confiance faible ({collective_conf:.2%}) - Nouvelle inférence...")
        
        print(f"  → COLLECTIF: {collective_pred} (conf:{collective_conf:.3f}) | Consensus: {'✅' if consensus else '❌'}")
        
        results.append({
            "test": test_i+1,
            "collective_prediction": collective_pred,
            "collective_confidence": round(collective_conf, 4),
            "consensus": consensus,
            "vm_votes": votes
        })
    
    # Résumé
    print(f"\n{'='*60}")
    print(f"RÉSUMÉ COLLECTIF ({n_tests} tests)")
    print(f"  Taux de consensus: {agreements/n_tests:.1%}")
    print(f"  Confiance moyenne: {sum(r['collective_confidence'] for r in results)/n_tests:.4f}")
    
    with open("C:\\projet_iot\\collective_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Résultats sauvegardés: collective_results.json")

if __name__ == "__main__":
    collective_inference(n_tests=10)