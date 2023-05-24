FROM ubuntu:20.04
WORKDIR /usr/src



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

RUN apt-get -y update
RUN apt-get install -y python3-pip
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


COPY base.dcm .
COPY main.py .
COPY downloadFile.py .
COPY Google.py .
COPY run_from_xnat.sh .
COPY predict.py . 
COPY imgTOdcm.py .
COPY command.json .
COPY client_secret_75469628766-mcsp2blgek6u9g587sl6dsani4ekvpao.apps.googleusercontent.com.json .
ADD token_drive_v3.pickle .
VOLUME /usr/src/model
RUN python3 -m pip install -r req.txt

# CMD ["--network=host", "sh run_from_xnat.sh /input #PROJECT_ID# #SUBJECT_ID# #SESSION_ID#"]
# CMD ["--network=host", "bash"]
ENTRYPOINT [] 