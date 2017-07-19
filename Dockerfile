FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN apt-get update && apt-get install -y nmap python2.7 python-pycurl python-libxml2 python-beautifulsoup python-geoip
 RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap-dev
 RUN ln -s /opt/sqlmap-dev/sqlmap.py /bin/sqlmap
 RUN git clone https://github.com/epsylon/xsser.git /opt/xsser
 RUN ln -s /opt/xsser/xsser/xsser /bin/xsser
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/