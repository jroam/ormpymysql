#coding=utf-8
import redis

"""操作redis的类库
插件包安装地址: 
"""
def redis_conn(db):
    '''类例化，一般处理一些连接操作'''
    try:
        return redis.StrictRedis(host=db["redis_host"], port=db["redis_port"], db=db["redis_db"],password=db["redis_pwd"])
    except Exception as e:
        return False



    