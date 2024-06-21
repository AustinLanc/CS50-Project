FROM ubuntu:22.04

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --trusted-host=pypi.org --trusted-host=files.pythonhosted.org -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8080/tcp

CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]
