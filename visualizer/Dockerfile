FROM centos:7

RUN yum -y install gcc openssl-devel bzip2-devel libffi-devel wget make yum install xz-devel mysql-devel mesa-libGL
RUN cd /opt
RUN wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz
RUN tar xzf Python-3.8.5.tgz
RUN cd Python-3.8.5 && ./configure --enable-optimizations && make altinstall
RUN rm Python-3.8.5.tgz

RUN mkdir /code
RUN mkdir /var/log/python
WORKDIR /code
COPY requirements.txt /code/
RUN python3.8 -m ensurepip --upgrade
RUN pip3.8 install -r requirements.txt
COPY . /code/
EXPOSE 8000