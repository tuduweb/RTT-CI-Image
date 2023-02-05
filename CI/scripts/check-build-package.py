#!/usr/bin/env python
import os
import sys
import json
import re
import shutil

### base
def create_pkgs_dict(pkgs_path):
    """
    create pkgs list from env
    eg. `package.json` in `~/.env/packages/packages/multimedia/LVGL/LVGL/`

    :param pkgs_path: packages dist path
    :return: dist
    """
    dicts = []
    json_path = []

    for path, dir_list, file_list in os.walk(pkgs_path):
        for file_name in file_list:
            if file_name == "package.json":
                json_path.append(path)

    for path in json_path:
        with open(os.path.join(path, 'package.json'), 'rb') as f:
            data = json.load(f)
            if 'name' in data and 'enable' in data and 'site' in data:
                dict = {'name': data['name'], 'enable': data['enable']}
                ver_dict = []

                for ver in data['site']:
                    if not os.access(os.path.join(path, 'Kconfig'), os.R_OK):
                        print(os.path.join(path, 'Kconfig') + "  No files!!")
                        break
                    f = open(os.path.join(path, 'Kconfig'))
                    text = f.read()
                    f.close()
                    pattern = re.compile('(?<=(config ))(((?!(config|default|bool)).)*?)(?=(\n)(((?!('
                                         'config|default|bool)).)*?)((default|bool)([^a-z]*?)(' + ver[
                                             'version'] + ')))', re.M | re.S)
                    if not (pattern.search(text) is None) and 'version' in ver:
                        ver_dict.append({'version': ver['version'], 'enable': pattern.search(text).group()})

                dict.setdefault('pkg', ver_dict)
                dicts.append(dict)
    return dicts

def get_pkgs_config(dict, pkgs):
    nolatest = False # args.nolatest
    pkgs_list = []
    if type(pkgs) is str:
        pkgs_list.append(pkgs)
    else:
        pkgs_list = list(pkgs)
    pkgs_return = []
    for data in dict:
        for pkg in pkgs_list:
            pattern = re.compile('(.*)(?=:)')
            pkg_copy = pkg
            if (':' in pkg and not (pattern.search(pkg) is None)):
                pkg_copy = pattern.search(pkg).group()
            if 'name' in data and (data['name'] == pkg_copy or pkg_copy == 'all'):
                part = data.copy()
                pkg_vers = []
                if ':' in pkg:
                    for pkg_ver in part['pkg']:
                        if pkg_ver['version'] in pkg:
                            pkg_vers.append(pkg_ver)
                else:
                    for pkg_ver in part['pkg']:
                        if (not nolatest) or ((nolatest) and (not pkg_ver['version'] == 'latest')):
                            pkg_vers.append(pkg_ver)
                if pkg_vers:
                    part['pkg'] = pkg_vers
                    pkgs_return.append(part)
                if not pkg_copy == 'all':
                    pkgs_list.remove(pkg)
                if not pkgs_list:
                    return pkgs_return
    return 


def find_pkg(pkg_name, pkg_ver):
    """
    find package detail from center

    :param pkg_name:    package name.
    :param pkg_ver:     package version. (eg: lastest, v1.0.0)
    :return: None
    """




    pass


def build_project(bsp_path, pkg_name, pkg_version, pkg_enable, pkg_ver_enable):
    
    pkg = {'name': 'hello', 'version': 123}
    log_path = 'log.tmp'
    flag = 'Success'

    cwd = os.getcwd()

    # bsp_new_path = bsp_path + '-' + pkg['name'] + '-' + pkg_ver_enable['version']
    bsp_new_path = bsp_path + '-' + pkg_name + '-' + pkg_version

    if os.path.exists(bsp_new_path):
        shutil.rmtree(bsp_new_path)

    shutil.copytree(bsp_path, bsp_new_path)


    # will download the package via `pkgs --update`
    # bsp_path -> bsp_new_path
    print('new bsp config path', os.path.join(bsp_new_path, '.config'))
    f = open(os.path.join(bsp_new_path, '.config'), 'a')
    f.write('\nCONFIG_' + pkg_enable + '=y\nCONFIG_' + pkg_ver_enable + '=y\n')
    f.close()

    command = '(cd ' + bsp_new_path + ' && scons --pyconfig-silent)'
    print(command)
    ret = os.system(command + ' > ' + log_path + ' 2>&1')
    if ret == 0:
        flag = 'Success'
    else:
        flag = 'Failure'


    f = open(os.path.join(bsp_new_path, '.config'))
    text = f.read()
    f.close()

    if (re.compile(pkg_enable + '=').search(text) is None) or (re.compile(pkg_ver_enable + '=').search(text) is None):
        flag = 'Invalid'

    print("flag 222", pkg_enable, pkg_ver_enable, re.compile(pkg_enable + '=').search(text))

    if flag == 'Success':
        command = '(cd ' + bsp_new_path + ' && ~/.env/tools/scripts/pkgs --update)'
        print(command)
        ret = os.system(command + ' >> ' + log_path + ' 2>&1')
        if ret == 0:
            flag = 'Success'
        else:
            flag = 'Failure'


    print("flag 333", bsp_new_path, flag)

    # check for addition package eg. whether package hello in bsp/../packages/...
    # check path has name (hha)

    if flag == 'Success':
        flag = 'Failure'
        for name in os.listdir(os.path.join(bsp_new_path,'packages')):
            if name in bsp_new_path:
                flag = 'Success'
                break


    # run scons to build ..
    if flag == 'Success':
        os.environ['RTT_CC'] = 'gcc'
        os.environ['RTT_EXEC_PATH'] = "/home/tuduweb/development/rtos/CI/mountPkg/gcc-arm-none-eabi-10-2020-q4-major/bin"# os.path.join(cwd, toolkit_bin) #RTT_EXEC_PATH=/opt/gcc-arm-none-eabi-10-2020-q4-major/bin
        command = 'scons -j16'
        print(bsp_new_path + ' ' + command)

        ret = os.system(command + ' -C ' + bsp_new_path) #+ ' >> ' + log_path + ' 2>&1')
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
    rtt_path = "/home/tuduweb/development/rtos/rt-thread/"
    work_path = root_path

    bsp_name = "qemu-vexpress-a9"
    pkg_name = "hello"
    pkg_ver = "v1.0.0"

    pkgs_name = [pkg_name]

    if sys.platform != 'win32':
        home_dir = os.environ['HOME']
    else:
        home_dir = os.environ['USERPROFILE']

    get_env("/home/tuduweb/development/rtos/rt-thread/")

    pkgs_all_dict = create_pkgs_dict(os.path.join(home_dir, '.env/packages/packages'))
    # print(pkgs_all_dict)

    # for dist in pkgs_all_dict:
    #     print(dist)

    pkgs_config = get_pkgs_config(pkgs_all_dict, pkgs_name)
    print(pkgs_config)

    pkg_config = pkgs_config[0]
    print(pkg_config)

    build_project("/home/tuduweb/development/rtos/rt-thread/bsp/qemu-vexpress-a9", pkg_config['name'], "v1.0.0", "PKG_USING_HELLO", "PKG_USING_HELLO_V10000")
