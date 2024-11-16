FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/commands.py .
COPY src/commit_database.py .
COPY src/constants.py .
COPY src/main.py .
COPY src/schedule.py .

CMD ["python", "main.py"]