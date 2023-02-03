#!/bin/bash
if [[ -z "$RTT_ROOT" ]]; then
    echo "RTT_ROOT is null. fault."
    exit 1
fi
# must run in RT-Thread directory
cd $RTT_ROOT
python -c "import tools.menuconfig; tools.menuconfig.touch_env()"
scons -C bsp/$RTT_BSP