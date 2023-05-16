# syntax=docker/dockerfile:1
FROM python:3.11.0
WORKDIR /app
RUN apk add --no-cache gcc musl-dev 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "python3", "app.py"]