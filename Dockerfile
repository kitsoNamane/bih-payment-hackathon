FROM python:3.11.3-slim-bullseye

WORKDIR /app

COPY . .

CMD pip3 install --no-cache-dir -r requirements.txt && ./run_project.sh

EXPOSE 6000
