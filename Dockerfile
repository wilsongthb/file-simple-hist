FROM python:3.10
COPY ./requirements.txt /var/req/requirements.txt
WORKDIR /var/req/
RUN pip install -r requirements.txt
