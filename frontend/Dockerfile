FROM python:3.10-slim

RUN pip install flask

WORKDIR /app

COPY . /app

EXPOSE 3000

CMD ["python", "app.py"]