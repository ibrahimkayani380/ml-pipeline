FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG GIT_SHA=unknown
ENV GIT_SHA=$GIT_SHA
RUN python train.py
EXPOSE 8000
CMD ["python", "app.py"]
