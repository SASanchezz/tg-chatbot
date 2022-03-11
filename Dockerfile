FROM python:3.8

WORKDIR /usr/src/app/

COPY . /usr/src/app/
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]