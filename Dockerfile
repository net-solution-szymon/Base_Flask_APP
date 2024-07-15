FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

EXPOSE 5000

ENV FLASK_APP main

RUN apt-get update
RUN apt-get -y install cron nano

USER root
RUN chmod +x ./script.sh


# Add the cron job
RUN crontab -l | { cat; echo "0 8 * * * /usr/src/app/script.sh"; } | crontab - 

RUN service cron start

# CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--limit-request-line", "0", "--limit-request-field_size", "0", "main:app"]
ENTRYPOINT cron && gunicorn -w 4 --bind 0.0.0.0:5000 --limit-request-line 0 --limit-request-field_size 0 main:app