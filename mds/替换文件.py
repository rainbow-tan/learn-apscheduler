# -*- encoding=utf-8 -*-
import datetime
import json
import logging
import logging.handlers
import os
import shutil


def create_folder(folder):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            msg = 'Success create folder:{}'.format(folder)
            print(msg)
        except Exception as e:
            msg = 'Failed create folder:{}, exception:{}'.format(folder, e)
            print(msg)


def delete_folder(folder):
    folder = os.path.abspath(folder)
    if os.path.isdir(folder):
        try:
            shutil.rmtree(folder)
            msg = 'Success delete folder:{}'.format(folder)
            print(msg)
        except Exception as e:
            msg = 'Failed delete folder:{}, exception:{}'.format(folder, e)
            print(msg)


def delete_file(file):
    file = os.path.abspath(file)
    if os.path.isfile(file):
        try:
            os.remove(file)
            msg = 'Success delete file:{}'.format(file)
            print(msg)
        except Exception as e:
            msg = 'Failed delete file:{}, exception:{}'.format(file, e)
            print(msg)


def copy_file(src, dst):
    # 目标文件存在,直接覆盖
    # 目标是文件夹,则在文件夹中生成同名文件
    create_folder(os.path.dirname(dst))
    try:
        shutil.copy2(src, dst)
        msg = 'Success copy file:{} to :{}'.format(os.path.abspath(src), os.path.abspath(dst))
        print(msg)
    except Exception as e:
        msg = 'Fail copy file:{} to :{}, exception:{}'.format(os.path.abspath(src), os.path.abspath(dst), e)
        print(msg)


def copy_folder(src, dst, delete=True):
    """
    :param src:
    :param dst:
    :param delete: 目标文件夹存在时,是否删除
    :return:
    """
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    if delete:
        delete_folder(dst)
    try:
        shutil.copytree(src, dst)
        msg = 'Success copy folder:{} to path:{}'.format(src, dst)
        print(msg)
    except Exception as e:
        msg = 'Fail copy folder:{} to path:{}, exception:{}'.format(src, dst, e)
        print(msg)


def read_file(file, mode='r', line_type=False, encoding=None):
    file = os.path.abspath(file)
    if line_type:
        content = []
    else:
        content = ''
    if os.path.isfile(file):
        with open(file, mode, encoding=encoding) as f:
            if line_type:
                content = f.readlines()
            else:
                content = f.read()
    return content


def write_file(file, info, mode='w', encoding=None, indent=4):
    create_folder(os.path.dirname(file))
    with open(file, mode, encoding=encoding) as f:
        if isinstance(info, str):
            f.write(info)
        elif isinstance(info, list):
            info = map(lambda x: str(x), info)
            f.writelines(info)
        elif isinstance(info, dict):
            info = json.dumps(info, indent=indent, ensure_ascii=False)
            f.write(info)
        else:
            msg = 'The type I don\'t know'
            print(msg)


def load_json_by_file(file, default=None):
    if default is None:
        default = dict()
    data = default
    file = os.path.abspath(file)
    if os.path.isfile(file):
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                msg = 'Success load json file:{}'.format(file)
                print(msg)
            except Exception as e:
                msg = 'Failed load json file:{}  exception:{}'.format(file, e)
                print(msg)
    else:
        msg = 'Can not find file:{} for load json'.format(file)
        print(msg)
    return data


def load_json_by_string(string, default=None):
    if default is None:
        default = dict()
    data = default
    try:
        data = json.loads(string)
        msg = 'Success load json string:{}'.format(string)
        print(msg)
    except Exception as e:
        msg = 'Failed load json string:{},  exception:{}'.format(string, e)
        print(msg)
    return data


def now(fmt='%Y%m%d%H%M%S'):
    string = datetime.datetime.now().strftime(fmt)
    return string


def string_to_date(string, fmt='%Y-%m-%d %H:%M:%S'):
    # 2021-01-28 10:51:26
    date = datetime.datetime.strptime(string, fmt)
    return date


def date_to_string(date, fmt='%Y-%m-%d %H:%M:%S'):
    # 2021-01-28 10:51:26
    string = date.strftime(fmt)
    return string


def traverse_folder(folder, only_first=False):
    folder = os.path.abspath(folder)
    all_files = []
    all_dirs = []
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for one_file in files:
                all_files.append(os.path.join(root, one_file))  # 所有文件
            for one_dir in dirs:
                all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹
            if only_first:
                break
    else:
        msg = 'Can not find folder:{} for traverse'.format(folder)
        print(msg)
    return all_dirs, all_files
def main():
    _,files = traverse_folder('.',True)
    for f in files:
        if '_network' in f and '.md' in f:
            name = f.replace("_network","")
            copy_file(f,name)
            delete_file(f)

if __name__ == '__main__':
    main()