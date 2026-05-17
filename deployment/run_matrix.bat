@echo off
set MODELS=baseline_full.pt q1_dynamic_full.pt q2_ptq_full.pt q3_qat_full.pt q4_weightonly_full.pt q5_mixed_full.pt p1_unstructured_full.pt p2_structured_full.pt p3_magnitude_full.pt

for %%M in (%MODELS%) do (
    echo Testing VM1 - %%M
    docker run --rm --cpus=1.0 --memory=500m -v C:\projet_iot\models:/models -e MODEL_PATH=/models/%%M projet_iot-vm1 python infer.py > vm1_%%M.json 2>&1

    echo Testing VM2 - %%M
    docker run --rm --cpus=2.0 --memory=1g -v C:\projet_iot\models:/models -e MODEL_PATH=/models/%%M projet_iot-vm2 python infer.py > vm2_%%M.json 2>&1

    echo Testing VM3 - %%M
    docker run --rm --cpus=2.0 --memory=2g -v C:\projet_iot\models:/models -e MODEL_PATH=/models/%%M projet_iot-vm3 python infer.py > vm3_%%M.json 2>&1
)

echo DONE!