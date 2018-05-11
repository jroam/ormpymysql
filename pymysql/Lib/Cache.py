import os
import hashlib
def mkdir(path):
    '''执行创建多重文件夹目录'''
    path=path.strip()
    path=path.rstrip("\\")

    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def file_put_content(filename,strs,mod="a"):
    ''' 写入文件，若没有会自动创建, mod 为w 直接写
        成功返回true 失败返回False 
    '''
    try:
        f=open(filename,mod)
        f.write(strs+"\n")
        f.close()
        return True
    except Exception as e:
        print(e)
        return False

def file_get_content(filename,mod="r"):
    '''获取文件内容
        成功返回内容 失败返回False 
    '''
    f=open(filename,mod)
    try:
        
        strs=f.read()
        f.close()
        return strs
    except Exception as e:
        f.close()
        return False


def md5(strs,codetype="utf-8"):
    '''对字符串进行md5加密'''
    tt=hashlib.md5(strs.encode('utf-8'))
    return(tt.hexdigest())


def deletefile(filename):
    '''删除缓存文件'''
    try:
        os.remove(filename)
        return True
    except Exception as e:
        return False