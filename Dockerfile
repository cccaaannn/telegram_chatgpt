FROM python:3.11-slim-buster

WORKDIR /telegram_chatgpt

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "telegram_chatgpt"]