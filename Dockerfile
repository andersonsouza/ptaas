FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN apt-get update && apt-get install -y nmap python2.7
 RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap-dev
 RUN ln -s /opt/sqlmap-dev/sqlmap.py /bin/sqlmap
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/