FROM python:3.8
WORKDIR /code
ENV FLASK_APP=open_science.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt update && apt install python3-dev \
                        gcc \
                        libc-dev \
                        libpq-dev \
                        poppler-utils \
                        build-essential \
                        libpoppler-cpp-dev \
                        pkg-config -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chmod 755 ./docker_entrypoint.sh
RUN python3 download_nltk.py

EXPOSE 5000

ENTRYPOINT [ "./docker_entrypoint.sh" ]
