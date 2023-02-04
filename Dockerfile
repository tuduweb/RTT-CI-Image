FROM ubuntu:20.04
#FROM ubuntu:latest
LABEL MAINTAINER tuduweb<tuduweb@outlook.com>

ENV isLocal 0

#RUN yum -y install net-tools

RUN ln -fs /bin/bash /bin/sh  #切换 sh 为bash
RUN if [[ ${isLocal} = 1 ]]; then \
		sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
		&& sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list ; \
	fi
RUN	apt-get clean \
	&& apt-get update \
	&& apt-get install python3 python-is-python3 pip git gcc-multilib libncurses5-dev scons -y #-qq #quiet

# clean apt cache
RUN rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apk/*

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
RUN if [ ${isLocal} = 1 ]; then pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple ; fi
RUN if [[ "$isLocal" = 1 ]]; then pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple/ ; else pip install requests ; fi

#EXPOSE 80

ENV	RTT_CC=gcc RTT_ROOT=/mountPkg/rt-thread RTT_EXEC_PATH=/mountPkg/gcc-arm-none-eabi-10-2020-q4-major/bin \
	RTT_BSP=qemu-vexpress-a9 RTT_TOOL_CHAIN=sourcery-arm

WORKDIR $RTT_ROOT

#RUN python -c "import tools.menuconfig; tools.menuconfig.touch_env()"
#RUN source ~/.env/env.sh && pushd bsp/$RTT_BSP && pkgs --update && popd
# scons -C bsp/$RTT_BSP
#CMD echo "----in docker----"
CMD /bin/bash

# docker build -t ciimage:0.1 .
# docker run -it --mount type=bind,source=/home/tuduweb/development/CI/mountPkg,target=/mountPkg ciimage:0.1
