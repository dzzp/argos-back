FROM python
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/data-picker
WORKDIR /opt/data-picker

ADD requirements.txt /opt/data-picker
RUN pip install -r requirements.txt
COPY . /opt/data-picker

EXPOSE 80
