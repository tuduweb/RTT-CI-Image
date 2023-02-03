#!/bin/bash
wget https://github.com/RT-Thread/toolchains-ci/releases/download/v1.3/gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2 # -q
sudo tar xjf gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2 -C /opt
/opt/gcc-arm-none-eabi-10-2020-q4-major/bin/arm-none-eabi-gcc --version