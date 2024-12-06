FROM python:latest

WORKDIR /app

RUN apt-get update
RUN apt-get install -y locales locales-all

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/commands.py .
COPY src/commit_database.py .
COPY src/constants.py .
COPY src/main.py .
COPY src/schedule.py .
COPY src/utils.py .

CMD ["python", "main.py"]