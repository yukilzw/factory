## factory
Python server side.
Mainly used for develop of client rather then release.

#### How to start tornado server for Mock?
You have two choices available:
1. install `python3.6`; change the directory to `./tornado` and run `pip install -r requirements.txt` in command; At last run `python main.py` start server.

2. If you've ever installed Docker,this might be suit for you.
    - `docker pull python:3.6.4`
    - `docker build -t factory .`
    - `docker run -p 1236:1236 -d factory:latest`