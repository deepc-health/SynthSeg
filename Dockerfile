FROM tensorflow/tensorflow:2.0.1-gpu-py3

COPY ./ /synthseg
WORKDIR /synthseg

RUN pip3 install -r requirements.txt

CMD ["python", "-u", "run_seg.py"]