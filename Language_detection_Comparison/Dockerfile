FROM python:3
#FROM continuumio/miniconda3

#COPY environment.yml /
#RUN conda install -c conda-forge cld2-cffi
#RUN conda install -c conda-forge pyicu
RUN apt update && apt install -y build-essential manpages-dev python-numpy libicu-dev
COPY requirements.txt /
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_md
RUN python -m spacy link en_core_web_md en
RUN CFLAGS="-Wno-narrowing" pip3 install cld2-cffi
RUN pip install future Cython
RUN pip install cysignals pyfasttext whatthelang
#RUN conda env create -f environment.yml -n X5GON
#SHELL ["conda", "run", "-n", "X5GON", "/bin/bash", "-c"]
