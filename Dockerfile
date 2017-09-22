FROM python
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y\
    python-dev pkg-config

RUN apt-get update && apt-get install -y\
    libav-tools libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libavresample-dev libavfilter-dev

RUN mkdir -p /opt/data-picker
WORKDIR /opt/data-picker

ADD requirements.txt /opt/data-picker
RUN pip install -r requirements.txt
COPY . /opt/data-picker

EXPOSE 80
