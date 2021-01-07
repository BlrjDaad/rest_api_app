FROM python:3.6

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirement.txt /Rest-API-app/requirement.txt

WORKDIR /Rest-API-app
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \

    && rm -rf /var/lib/apt/lists/*


RUN pip3 install --upgrade pip  setuptools
RUN pip3 install -r requirement.txt

COPY . /rest_server

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
