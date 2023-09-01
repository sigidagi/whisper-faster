FROM python:3.9
MAINTAINER Sigitas Dagilis

WORKDIR /home
RUN apt-get update

COPY requirements.txt . 
COPY start_transcriptor.py . 

RUN ls --recursive ${WORKDIR}

RUN pip install -r requirements.txt

CMD ["python", "/home/start_transcriptor.py"]
