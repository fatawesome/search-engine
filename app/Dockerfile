FROM python:3.7.5

LABEL MAINTAINER="Ilya Alonov <i.alonov@innopolis.ru>"

ENV GROUP_ID=1000 \
    USER_ID=1000 \
    PYTHONUNBUFFERED=0

RUN mkdir app
COPY . /app

RUN pip install -r app/requirements.txt
RUN pip install gunicorn

RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader reuters

EXPOSE 5000

CMD gunicorn -w 4 --bind 0.0.0.0:5000 app.wsgi --log-level debug --reload --timeout 500
