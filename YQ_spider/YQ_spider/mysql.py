import pymysql
host ='xxxxx'
class MySQL():
    conn = pymysql.connect(host=host,port=3306,password='XXXXX',user='root',db='scrapyhub',charset='utf8')
    @classmethod
    def execute(cls,sql):
        cur = cls.conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data

    @classmethod
    def s_return(cls,data):
        lenNum = len(data[0])
        stat_s ='%s'
        s = ',%s'
        while lenNum > 1:
            stat_s += s
            lenNum -=1
        return stat_s

    @classmethod
    def insert_data(cls,sqlName,data):
        cur = cls.conn.cursor()
        s_str = cls.s_return(data)
        sql = "INSERT INTO {} VALUES({})".format(sqlName,s_str)
        cur.executemany(sql,data)
        cls.conn.commit()

