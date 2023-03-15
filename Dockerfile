FROM python:3.9.8
ADD . /GraphApp
WORKDIR /GraphApp
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN pip3 install gunicorn
EXPOSE 5000
CMD python3 server.py prod
