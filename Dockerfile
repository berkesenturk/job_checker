FROM python:3.6-alpine

COPY . ./app
WORKDIR /app

RUN pip install -r requirements.txt
#Install Cron
RUN apt-get update
RUN apt-get -y install cron


# Add the cron job
RUN crontab -l | { cat; echo "0 10 * * * bash /src/main.py"; } | crontab -

# Run the command on container startup
CMD ["python", "./src/main.py"]
