#coding=utf-8
 
from ..conf import conf as config
import mysql.connector
import os
from . import  Cache
import pickle
import time

class MyDB:
    '''mysql数据库操作类 包地址：http://dev.mysql.com/downloads/connector/python/

    使用示例(传入配置文件):
    import pymysql.Lib.MyDB as dbdb
    db=dbdb.MyDB()


    # 查询
    wdata={}
    wdata["title"]=["like","%九寨%"]
    mr=dbdb.table("gentuanyou")
    rs=mr.field("gentuanyouid,title").where(wdata).limit("0,5").order("gentuanyouid asc").select()
    print(mr.lastsql)
    print(rs)


    #  更新操作
    rs=mr.where(wdata).save(data)

    # 删除操作
    rs=mr.where(wdata).delete()

    # 添加操作
    data={}
    data["title"]="张三四2"
    data["type"]="e22"
    mr.add(data)


    '''
    cnx=""
    cursor=""
    wheredirt ={} #存放要生成查询的条件
    orderstr="" # 生成后的排序语句
    tbname="" #此次操作的tbname
    fieldname="*"  # 此次要查询的字段
    qz="" # 数据表前缀
    limitstr="" #sql的限制部份
    groupstr=""  #sql的groupby部份
    lastsql="" # 最近执行的sql
    savedict={}
    joinstr="" #两表联查生成sql
    flag_cache =False #是否要缓存
    cache_time=0 # 缓存的时间，单位秒
    cache_path="" # 缓存文件的路径

    def __init__(self,db=None):
        '''类例化，一般处理一些连接操作'''
        if db==None:
            db=config.conf["db"]
        self.qz=db["prefix"]
        self.cnx = mysql.connector.connect(user=db["user"],passwd=db["passwd"],host=db["host"],port=db["port"], database=db["dbname"])
        self.cursor = self.cnx.cursor()

    def initcs(self):
        '''恢复一些参数，以便下次调用'''
        self.wheredirt ={} #存放要生成查询的条件
        self.orderstr="" # 生成后的排序语句
        self.fieldname="*"  # 此次要查询的字段
        self.limitstr="" #sql的限制部份
        self.groupstr=""  #sql的groupby部份
        self.savedict={}
        self.joinstr="" #两表联查生成sql
        



    def createquerysql(self):
        '''构建查询的语句'''
        temps=""
        for k in self.wheredirt:
            sqls=""
            if(type(self.wheredirt[k])==list):
                v=self.wheredirt[k]
                if type(v[1])==str : v[1]=self.escape(v[1])
                if v[0]=="eq":
                    sqls= type(v[1])==str  and  "='"+v[1]+"'" or  "="+str(v[1])
                if v[0]=="neq":
                    sqls= type(v[1])==str  and  "<>'"+v[1]+"'" or  "<>"+str(v[1])
                if v[0]=="gt":
                    sqls= type(v[1])==str  and  ">'"+v[1]+"'" or  ">"+str(v[1])
                if v[0]=="lt":
                    sqls= type(v[1])==str  and  "<'"+v[1]+"'" or  "<"+str(v[1])
                if v[0]=="in": #只能是str 或list
                    sqls= type(v[1])==str  and  " in("+v[1]+")" or  " in('"+"','".join(v[1])+"')"

                if v[0]=="exp":
                    sqls=" "+v[1]
                if v[0]=="_string":
                    sqls=" "+v[1]
                if v[0]=="like":
                    sqls=" like '"+v[1]+"'"
            else:
                if(k!="_string"):
                    sqls= type(self.wheredirt[k])==str  and  "='"+self.escape(self.wheredirt[k])+"'" or  "="+str(self.wheredirt[k])
                else:
                    sqls=str(self.wheredirt[k])


            if(k=="_string"): k=""
            temps=temps+" ("+k+sqls+") and"

        temps=temps[:-3]
        return temps
        


    def createupdatesql(self):
        '''构建保存的语句 savedict'''
        temps=""
        for k in self.savedict:
            sqls= type(self.savedict[k])==str  and  "='"+self.escape(self.savedict[k])+"' " or  "="+self.savedict[k]+""
            temps=temps+" "+k+sqls+" "+","

        temps=temps[0:-1]
        return temps

    def select(self):
        '''结合where里的用select法去查询'''
        temps=self.createquerysql()
        sql="select "+self.fieldname+" from "+self.qz+self.tbname
        
        if self.joinstr!="":
            sql=sql+self.joinstr

        if temps!="":
            sql=sql+" where "+temps
        if self.groupstr!="" :
            sql=sql+" group by "+self.groupstr
        if self.orderstr!="":
            sql=sql+" order by "+self.orderstr

       
        if self.limitstr!="" :
            sql=sql+" limit "+self.limitstr

        
        self.initcs() #回收一些参数
        return self.fetchall(sql)

    def find(self):
        temps=self.createquerysql()
        sql="select "+self.fieldname+" from "+self.qz+self.tbname
        if self.joinstr!="":
            sql=sql+" "+self.joinstr

        if temps!="":
            sql=sql+" where "+temps
        if self.groupstr!="" :
            sql=sql+" group by "+self.groupstr
        if self.orderstr!="":
            sql=sql+" order by "+self.orderstr

        sql=sql+" limit 0,1"
        self.initcs() #回收一些参数
        return self.fetchone(sql)


    def delete(self):
        '''删除操作,避免删除所有的记录，where部份不能为空'''
        temps=self.createquerysql()
        if len(temps)<5: return False
        sql="delete from "+self.qz+self.tbname +" where "+temps
        
        self.initcs() #回收一些参数
        self.lastsql=sql
        self.execute(sql)
        return self.cursor.rowcount

    def query_iter(self,sqls):
        '''执行多条语句时选择用,执行这条语句后，需要再次执行commit()方法'''
        try:
            temps=self.cursor.execute(sqls)
            return 1
        except:
            return 0




    def add(self,dict1):
        '''添加操作'''
        self.savedict=dict1

        sql_data=self.createaddsql()

        sql="insert into "+self.qz+self.tbname+" "+sql_data
        try:
            self.lastsql=sql
            self.cursor.execute(sql)
            lastrowid=self.cursor.lastrowid
            self.cnx.commit()
            return lastrowid
        except:
            return 0
        finally:
            self.initcs()



    def createaddsql(self):
        '''生成插入的sql语句'''
        temps_k=""
        temps_v=""
        for k in self.savedict:
            temps_k=temps_k+k+","
            temps_v= type(self.savedict[k])==str  and  temps_v+" '"+self.escape(self.savedict[k])+"',"\
             or  temps_v+" "+str(self.savedict[k])+","
            #temps_v+= " %("+k+")s,"
            
            

        temps=""
        temps_k=temps_k[0:-1]
        temps_v=temps_v[0:-1]
        if temps_k!="" : temps="("+temps_k+") values ("+temps_v+")"
        return temps



    def save(self,dict1):
        '''保存值'''
        self.savedict=dict1
        if len(self.wheredirt)<1: return False
        sql_data=self.createupdatesql()
        sql_where=self.createquerysql()
        sql="update "+self.qz+self.tbname+" set "+sql_data
        if sql_where!="" :
            sql+=" where "+sql_where
        
        #print(sql)
        try:
            self.lastsql=sql
            flags=self.cursor.execute(sql)
            #lastid=self.cursor.lastrowid #要在commit()前，不然会返回0
            self.cnx.commit()
            self.initcs()
            return self.cursor.rowcount
        except:
            return False



    def join(self,str1):
        '''两表联查生成sql'''
        self.joinstr=self.joinstr+" "+str1
        return self


    def limit(self,str1):
        '''构建limit部份'''
        self.limitstr=str1
        return self

    def group(self,str1):
        '''sql语句的group by部份'''
        self.groupstr=str1
        return self

    def table(self,str1,qz=""):
        '''传入此次查询的表名'''

        self.tbname=str1
       
        if qz!="" :
            self.qz=qz
        return self

    def field(self,str1):
        self.fieldname=str1
        return self


    def order(self,str1):
        '''生成排序的语句'''
        if str1!="" : 
            self.orderstr=str1
        return self


    def formatrs(self,rows):
        '''为查询的数据结果加字段名处理，
        fieldname是返回的字段名列表，
        rows是返回的数据列表
        '''
        r=[]
        for x in rows:
            temp=dict(zip(self.cursor.column_names,x))
            for x1 in temp:
                if temp[x1]==None: temp[x1]=""
            r.append(temp)
        return r

    def writecache(self,sql,strs):
        '''执行缓存或取缓存内容'''
        if self.flag_cache==False:
            return False
        t=pickle.dumps(strs)
        Cache.file_put_content(self.cache_path+"/"+Cache.md5(sql)+".txt",t,"wb")
    

    def readcache(self,sql):
        '''读取缓存内容'''
        filename=self.cache_path+"/"+Cache.md5(sql)+".txt"

        if self.flag_cache==False or os.path.exists(filename)==False:
            Cache.deletefile(filename)
            return False
        



        #查看是否超出缓存时间
        fileinfo=os.stat(filename)
        edittime=int(fileinfo.st_mtime)
        nowtile=int(time.time())

        if edittime+self.cache_time<nowtile :

            Cache.deletefile(filename)
            return False

        content=pickle.loads(Cache.file_get_content(filename,"rb"))

        return content

    def cache(self,flag,timenum):
        '''是否要缓存查询的结果'''
        if flag==True:
            md5str=Cache.md5(time.strftime("%Y-%m-%d")+"logs")
            md5str1=md5str[:2]
            md5str2=md5str[2:4]
            self.cache_path=config.conf["logpath"]["path"]+"/"+md5str1+"/"+md5str2
            Cache.mkdir(self.cache_path)
            self.flag_cache=True
            self.cache_time=timenum
        return self


    def fetchall(self,sql):
        '''查询数据，返回一个列表，里面的每一行是一个字典，带字段名
             cursor 为连接光标
             sql为查询语句
        '''

        try:

            self.lastsql=sql
            rows=self.readcache(sql)
            if self.readcache(sql)!=False:
                return rows

            self.cursor.execute(sql)
            rows=self.cursor.fetchall()
            rows=self.formatrs(rows)

            self.writecache(sql,rows) #写入缓存
            return rows
        except:
            return False
        
    def execute(self,sql):
        '''
        插入或更新记录 成功返回最后的id
        '''
        self.cursor.execute(sql)
        self.cnx.commit()
        return self.cursor.lastrowid

    def query(self,sql):
        '''
        直接以sql语句查询
        '''
        self.initcs() #回收一些参数
        return self.fetchall(sql)

    def where(self,dist1):
        if type(dist1)!=dict: return False
        self.wheredirt=dist1
        return self

    def fetchone(self,sql):
        '''获取单行'''
        # self.lastsql=sql
        # self.cursor.execute(sql)
        # rows=self.cursor.fetchone()
        # if rows==None: return {}
        # return dict(zip(self.cursor.column_names,rows))

        try:

            self.lastsql=sql
            rows=self.readcache(sql)
            if self.readcache(sql)!=False:
                return rows

            self.cursor.execute(sql)
            rows=self.cursor.fetchone()
            if rows==None: return {}
            rows=dict(zip(self.cursor.column_names,rows))
            self.writecache(sql,rows) #写入缓存
            return rows
        except:
            return False

    def escape(self,str1):
        '''针对字符串做转义'''
        #return str1.replace("\"","\\\"").replace("\'","\\\'")
        return str1.replace("\"","\\\"")

    def close(self):
        '''结束查询和关闭连接'''
        self.cnx.close()
        self.cursor.close()


    def getpath(self):
        '''获取调用文件的目录，而不是此文件的目录'''
        return os.getcwd()



