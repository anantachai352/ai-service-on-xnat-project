FROM ubuntu:20.04
# LABEL maintainer="p.sovatha@vamstack.com"
WORKDIR /usr/src
# ADD run.sh /home


COPY req.txt .


ENV DEBIAN_FRONTEND="noninteractive"
ENV DEBCONF_NONINTERACTIVE_SEEN true
# RUN apt -y update
ENV LANG en_US.utf8
RUN . /etc/os-release \
&& echo "deb mirror://mirrors.ubuntu.com/mirrors.txt $VERSION_CODENAME main restricted universe multiverse" > /etc/apt/sources.list \
&& echo "deb mirror://mirrors.ubuntu.com/mirrors.txt $VERSION_CODENAME-updates main restricted universe multiverse" >> /etc/apt/sources.list \
&& echo "deb mirror://mirrors.ubuntu.com/mirrors.txt $VERSION_CODENAME-backports main restricted universe multiverse" >> /etc/apt/sources.list \
&& echo "deb mirror://mirrors.ubuntu.com/mirrors.txt $VERSION_CODENAME-security main restricted universe multiverse" >> /etc/apt/sources.list \
&& apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
# RUN add-apt-repository -y ppa:deadsnakes/ppa
# RUN apt -y update
# RUN apt install -y libgl1-mesa-glx
# RUN apt install -y python3.8
RUN apt-get -y update
RUN apt-get install -y python3-pip

COPY command.json .
COPY dicomTojpeg.py .
COPY run_from_xnat.sh .

RUN python3 -m pip install -r req.txt



ENTRYPOINT []