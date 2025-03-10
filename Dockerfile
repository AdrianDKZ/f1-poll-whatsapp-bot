FROM python:3.11.9

WORKDIR /app

RUN apt-get update
RUN apt-get install -y locales locales-all

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir ./src
COPY src/ src/

CMD ["python", "-m", "src.main"]