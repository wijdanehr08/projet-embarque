FROM python:3.10-slim

WORKDIR /app

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install psutil pillow

COPY infer.py .

CMD ["python", "infer.py"]