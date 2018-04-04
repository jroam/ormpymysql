### 使用手册
'''
    mysql数据库操作类 包地址：http://dev.mysql.com/downloads/connector/python/

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

