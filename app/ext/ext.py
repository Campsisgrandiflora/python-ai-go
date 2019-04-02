import re

# 正则表达式用于除去HTML标签
pat = re.compile('<[^>]+>', re.S)


# 除去标签
def remove_tag(test):
    return pat.sub('', test)


# 将列表转换为字典
def change_list_to_dic(List):
    dic = dict()
    for item in List:
        dic[item[0]] = item[1]
    return dic


# 两个字典求并集
def dict_union():
    pass


test1 = {1: {}}
demokeyurl = "F:/programming/python/ai-go/app/static/keyword/demokey.dat"
demandkeyurl = "F:/programming/python/ai-go/app/static/keyword/demandkey.dat"

# 在线运行代码的代码 ######################################################
import os, sys, subprocess
import cProfile
import pstats


def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')


# EXEC = sys.executable
# b = os.popen('python test.py', 'r')
# fpath = 'test.py'


def runningcode(fpath, EXEC=sys.executable):
    r = dict()
    try:
        print('Execute: %s %s' % (EXEC, fpath))
        r['output'] = decode(subprocess.check_output([EXEC, fpath], stderr=subprocess.STDOUT, timeout=5))
    except subprocess.CalledProcessError as e:
        r = dict(error='Exception', output=decode(e.output))
    except subprocess.TimeoutExpired as e:
        r = dict(error='Timeout', output='执行超时')
    except subprocess.CalledProcessError as e:
        r = dict(error='Error', output='执行错误')
    return r


