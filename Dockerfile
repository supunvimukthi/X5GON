FROM tensorflow/tensorflow:latest

#ENV NUM_CORES 12

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
                       nginx \
		       python3-pip

RUN pip3 install numpy
RUN pip3 install Pillow
RUN pip3 install tensorflow
RUN pip3 install flask gevent gunicorn && \
        rm -rf /root/.cache

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

RUN mkdir -p /opt/ml
COPY ml /opt/ml
RUN mkdir -p /opt/program
COPY program /opt/program
#RUN rm -f /opt/program/predictor-backup.py
WORKDIR /opt/program

RUN chmod 755 serve
