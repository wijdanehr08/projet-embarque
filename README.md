# Projet IoT - Inférence Médicale Embarquée
## Master Data Science - ENS Martil

## Dataset
COVID-19 Radiography Database - 21165 images - 4 classes (COVID, Normal, Lung_Opacity, Viral Pneumonia)

**Dépôt GitHub :** https://github.com/wijdanehr08/projet-embarque/tree/main

## Architecture Baseline
MobileNetV2 - Accuracy: 85% - Taille: 8.74 Mo

## Techniques d'optimisation appliquées
| ID | Technique | Accuracy | Taille | Inférence |
|----|-----------|----------|--------|-----------|
| Q1 | Dynamic Quantization | 0.8496 | 8.70 Mo | 13.57 ms |
| Q2 | Static PTQ | 0.8496 | 8.70 Mo | 11.63 ms |
| Q3 | QAT | 0.8499 | 8.70 Mo | 6.00 ms |
| Q4 | Weight-Only | 0.8496 | 8.70 Mo | 5.77 ms |
| Q5 | Mixed Precision | 0.8496 | 8.70 Mo | 6.20 ms |
| P1 | Unstructured Pruning | 0.8413 | 8.72 Mo | 6.02 ms |
| P2 | Structured Pruning | 0.8216 | 8.72 Mo | 5.90 ms |
| P3 | Magnitude Pruning | 0.8550 | 8.72 Mo | 6.35 ms |

## VMs Docker
| VM | CPU | RAM | Meilleure technique |
|----|-----|-----|---------------------|
| VM1 | 1 core | 500 Mo | P2 Structured |
| VM2 | 2 cores | 1 Go | P1 Unstructured |
| VM3 | 2 cores | 2 Go | P2 Structured |

## Intelligence Collective
- Taux de consensus: 100%
- Confiance moyenne: 1.0000
- 10 tests effectués

## Supervision ThingsBoard
- Dashboard: IoT Medical Monitoring
- Télémétrie: prediction, confidence, inference_time_ms, ram_usage_mb, cpu_usage_pct

## Structure du projet
- `environment/` - docker-compose.yml
- `deployment/` - Scripts de déploiement
- `collective/` - Orchestrateur vote pondéré
- `thingsboard/` - Client MQTT/HTTP
- `results/` - Matrices CSV et JSON
- `vm1/ vm2/ vm3/` - Dockerfiles par VM
