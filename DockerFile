FROM python:3.6.4

WORKDIR /dockerEnv

ADD . /dockerEnv

RUN pip install -r /dockerEnv/tornado/requirements.txt

CMD ["python", "/dockerEnv/tornado/main.py"]