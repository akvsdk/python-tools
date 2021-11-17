import os
import shutil
from pathlib import Path


def dex2smail(path):
    path = Path(path)  # 文件夹目录
    out_path = str(path.absolute()) + '/smali'  # 输出文件夹
    makeDir(out_path)
    for file in path.glob('*.dex'):
        # sh = f'jadx -j 1 -r -d {out_path} {path}\\{file}'
        sh = f'java -jar /Users/j1ang/Documents/code/hook/baksmali-2.4.0.jar d {file} -o {out_path}'
        print(sh)
        os.system(sh)


def tree(directory):
    print(f'+ {directory}')
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = '    ' * depth
        print(f'{spacer}+ {path.name}')


def remove_file(old_path, new_path, fileName):
    new_dir = Path(new_path + fileName).parent
    # 需要处理smali_classes3 之后的字符
    makeDir(new_dir)
    print("old_path:    " + str(old_path))
    print("new_path:    " + str(new_path + fileName))
    shutil.move(str(old_path), str(new_path + fileName))


fileNum = 0
dirName = 0


def smailArchive(path):
    """
    smail切割到不同文件夹
    :param path: 目标目录
    :return:
    """
    global fileNum
    global dirName
    dir_path = Path(path)
    list = dir_path.iterdir()
    for file in list:
        if file.is_file():
            if fileNum % archivesCount == 0:
                dirName += 1
            fileNum += 1
            if fileNum > archivesCount:
                newDir = '%s%s/' % (path_new, dirName)
                fileName = str(file.relative_to('{}{}'.format(path_main, '/smali')))
                print(newDir)
                print(fileNum)
                remove_file(file, newDir, fileName)
        elif file.is_dir():
            smailArchive(str(file.absolute()))


def visitDir(path):
    """
    统计文件夹大小及文件个数
    :param path: 目录
    :return:
    """
    totalSize = 0
    fileNum = 0
    dirNum = 0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        print(sub_path)
        if os.path.isfile(sub_path):
            fileNum = fileNum + 1  # 统计文件数量
            totalSize = totalSize + os.path.getsize(sub_path)  # 文件总大小
        elif os.path.isdir(sub_path):
            dirNum = dirNum + 1  # 统计文件夹数量
            visitDir(sub_path)  # 递归遍历子文件夹
    print('The total size of ' + path + ' is:' + sizeConvert(totalSize))
    print('The total number of files in ' + path + ' is:', fileNum)
    print('The total number of directories in ' + path + ' is:', dirNum)


def sizeConvert(size):  # 单位换算
    K, M, G = 1024, 1024 ** 2, 1024 ** 3
    if size >= G:
        return str(size / G) + 'G Bytes'
    elif size >= M:
        return str(size / M) + 'M Bytes'
    elif size >= K:
        return str(size / K) + 'K Bytes'
    else:
        return str(size) + 'Bytes'


def makeDir(path):
    new_dir = Path(path)
    if new_dir.exists():
        if new_dir.is_file():
            print("是文件")
        elif new_dir.is_dir():
            print("是目录")
        else:
            print("不是文件也不是目录")
    else:
        print("目录不存在:" + str(new_dir))
        # Path.mkdir(new_dir)
        os.makedirs(new_dir)


# dex 文件夹
package = '/Users/j1ang/Documents/apk/com.rumtel.mobiletv'
# smil 生成文件夹
path_main = package
path_new = package + '/smali_classes'
# 单文件夹最多方法数
archivesCount = 5000

if __name__ == '__main__':
    dex2smail(path_main)
    smailArchive(path_main + '/smali/')
    # total = Path(path_main)
    # for file in total.iterdir():
    #     if file.is_dir():
    #         os.system(f"""cd {file.absolute()} && ls -lR| grep "^-" | wc -l""")
    # visitDir(path)
    # print(len(list(Path(path).iterdir())))
    # tree(Path('/Users/j1ang/Documents/apk/com.rumtel.mobiletv/smali'))
