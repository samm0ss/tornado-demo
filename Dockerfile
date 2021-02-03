FROM python:3.8.6-slim
ENTRYPOINT ["python"]

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-input && rm requirements.txt
COPY requirements-dev.txt requirements-dev.txt
RUN python -m venv --system-site-packages /venv-test && . /venv-test/bin/activate && pip install -r requirements-dev.txt && rm requirements-dev.txt

WORKDIR /app

COPY . .