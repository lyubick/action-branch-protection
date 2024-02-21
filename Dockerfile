FROM python:3.11-slim

WORKDIR /

ADD requirements.txt /
ADD set_protection.py /

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/set_protection.py"]
