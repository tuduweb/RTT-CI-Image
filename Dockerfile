FROM ubuntu:20.04
#FROM ubuntu:latest
LABEL MAINTAINER tuduweb<tuduweb@outlook.com>


#WORKDIR $MYPATH

#RUN yum -y install net-tools

#RUN 	sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
#	&& sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list \
RUN	apt-get clean \
	&& apt-get update \
	&& apt-get install python3 python-is-python3 pip git gcc-multilib libncurses5-dev scons -y #-qq #quiet

#env
RUN mkdir /root/.env \
	&& mkdir /root/.env/tools \
	&& mkdir /root/.env/packages \
	&& mkdir /root/.env/packages/packages \
	&& mkdir /root/.env/tools/scripts \
	&& touch /root/.env/packages/Kconfig \
# echo 'source "$PKGS_DIR/packages/Kconfig"' > /root/.env/packages/Kconfig
	&& git clone https://github.com/RT-Thread/env.git /root/.env/tools/scripts/


#RUN python3 -m pip install --upgrade pip \
#	&& pip install --default-timeout=100 requests

#RUN pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install requests

#EXPOSE 80

#ENV	RTT_CC=gcc

CMD echo "----in docker----"
#CMD /bin/bash

# docker build -t ciimage:0.1 .
# docker run -it --mount type=bind,source=/home/tuduweb/development/CI/mountPkg,target=/mountPkg ciimage:0.1
