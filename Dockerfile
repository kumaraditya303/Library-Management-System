FROM python:3.10.2

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
ADD . /app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi"]
