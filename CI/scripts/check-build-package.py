#!/usr/bin/env python
import os
import re
import shutil

def build_project(bsp_path, pkg_name, pkg_ver):
    
    pkg = {'name': 'hello', 'version': 123}
    log_path = 'log.tmp'
    flag = 'Success'

    cwd = os.getcwd()

    # bsp_path_new = bsp_path + '-' + pkg['name'] + '-' + pkg_ver['version']
    bsp_path_new = bsp_path + '-' + pkg_name + '-' + pkg_ver

    if os.path.exists(bsp_path_new):
        shutil.rmtree(bsp_path_new)

    shutil.copytree(bsp_path, bsp_path_new)


    # will download the package via `pkgs --update`
    # bsp_path -> bsp_path_new
    print('new bsp config path', os.path.join(bsp_path_new, '.config'))
    f = open(os.path.join(bsp_path_new, '.config'),'a')
    f.write('\nCONFIG_' + pkg_name + '=y\nCONFIG_' + pkg_ver + '=y\n')
    f.close()
    # return
    #exit(0)

    command = '(cd ' + bsp_path_new + ' && scons --pyconfig-silent)'
    print(command)
    ret = os.system(command + ' > ' + log_path + ' 2>&1')
    if ret == 0:
        flag = 'Success'
    else:
        flag = 'Failure'


    f = open(os.path.join(bsp_path_new, '.config'))
    text = f.read()
    f.close()
    
    print(text)

    if (re.compile(pkg_name + '=').search(text) is None) or (re.compile(pkg_ver + '=').search(text) is None):
        flag = 'Invalid'

    if flag == 'Success':
        command = '(cd ' + bsp_path_new + ' && ~/.env/tools/scripts/pkgs --update)'
        print(command)
        ret = os.system(command + ' >> ' + log_path + ' 2>&1')
        if ret == 0:
            flag = 'Success'
        else:
            flag = 'Failure'


    print("flag 333", bsp_path_new, flag)

    # check for addition package eg. hello to bsp/../packages/...
    # check path has name (hha)

    # if flag == 'Success':
    #     flag = 'Failure'
    #     for name in os.listdir(os.path.join(bsp_path_new,'packages')):
    #         if name in bsp_path_new:
    #             flag = 'Success'
    #             break
    # print("flag444", name, bsp_path_new, os.path.join(bsp_path_new,'packages'), flag)
    # run scons to build ..
    if flag == 'Success':
        os.environ['RTT_CC'] = 'gcc'
        #os.environ['RTT_EXEC_PATH'] = os.path.join(cwd, tools) #RTT_EXEC_PATH=/opt/gcc-arm-none-eabi-10-2020-q4-major/bin
        command = 'scons -j16'
        print(bsp_path_new + ' ' + command)

        ret = os.system(command + ' -C ' + bsp_path_new) #+ ' >> ' + log_path + ' 2>&1')
        if ret == 0:
            flag = 'Success'
        else:
            flag = 'Failure'

    print("build all end. flag", flag)


def build(bsp_path, pkg_name, pkg_ver, tools, log_path):
    # 0 Initial 1 Success 2 Failure 3 Invalid
    flag = 'Success'
    logs = []
    if not os.path.isdir(bsp_path):
        print(bsp_path, 'No path !!!')
        return
    print('build', bsp_path, pkg_name, pkg_ver, tools)
    cwd = os.getcwd()
    f = open(os.path.join(bsp_path, '.config'),'a')
    f.write('\nCONFIG_' + pkg_name + '=y\nCONFIG_' + pkg_ver + '=y\n')
    f.close()
    pass

def get_env(rtt_path):
    os.chdir(rtt_path)
    #os.system('python3 -c "import tools.menuconfig; tools.menuconfig.touch_env()"')
    os.chdir(root_path)

if __name__ == '__main__':
    print("hello world")

    root_path = os.getcwd()

    get_env("/home/tuduweb/development/rtos/rt-thread/")

    build_project("/home/tuduweb/development/rtos/rt-thread/bsp/qemu-vexpress-a9", "PKG_USING_HELLO", "PKG_USING_HELLO_V10000")
