FROM python:alpine as base

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR .

COPY requirements.txt . 


RUN pip3 install -r requirements.txt

RUN mkdir code
RUN cd code

EXPOSE 5500
