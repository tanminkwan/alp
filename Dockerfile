FROM python:3.10.10-bullseye

RUN apt-get -y update && apt-get install -y fonts-nanum
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm -rf ~/.cache/matplotlib/*
RUN fc-cache -fv
COPY . ./alp
WORKDIR /alp
EXPOSE 5000
CMD [ "python3", "app.py"]
