FROM python:3.7.5-slim

COPY requirements.txt requirements.txt

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8080

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]