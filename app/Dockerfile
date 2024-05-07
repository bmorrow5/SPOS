FROM python:3.9.19

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8001

CMD ["python", "app.py"]
