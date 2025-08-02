FROM rasa/rasa-sdk:3.6.2

COPY . /app/actions
WORKDIR /app/actions

RUN pip install --no-cache-dir -r requirements.txt

USER 1001
