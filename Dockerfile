FROM python:3.11.2
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/ 
EXPOSE 8000
CMD gunicorn tutor.wsgi --log-file -
WORKDIR /code/
