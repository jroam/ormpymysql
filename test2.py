#coding=utf-8
import pymysql.Lib.MyDB as dbdb

db=dbdb.MyDB()
mr=db.table("gentuanyou") #指定表名

#构建条件
wd={}
wd["title"]=["like","%四川%"]

#执行查询
rs=mr.cache(True,360).field("gentuanyouid ,title").where(wd).limit("0,5").select()

#打印结果
print(rs)