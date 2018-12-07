import pymysql
import datetime

class Processing(object):
    conn = pymysql.connect(host='rm-bp1ppxouwgu9ta1787o.mysql.rds.aliyuncs.com', port=3306, user='root', password='YKYroot123123', db='scrapyhub', charset='utf8')
    today = datetime.datetime.today().date()
    yesday = today - datetime.timedelta(days=1)
    cur = conn.cursor()

    @classmethod
    def return_columns_s(self,data):
        num = len(data[0])
        p = '%s'
        while num > 1:
            p +=',%s'
            num -=1
        return p

    @classmethod
    def processing_duplicate(self,sqlName,groupby,type=1,cussql=None):
        # This step is duplicate the same postUrl on today
        if type == 1:
            sql = "select * from {} where spider_date='{}' group by {}".format(sqlName,self.today,groupby)
            self.cur.execute(sql)
        elif type ==2:
            self.cur.execute(cussql)
        data = self.cur.fetchall()
        p = self.return_columns_s(data)
        # delete rows
        sql = "DELETE FROM {} where spider_date='{}'".format(sqlName,self.today)
        self.cur.execute(sql)
        # add rows
        sql = "INSERT INTO {} VALUES({})".format(sqlName,p)
        for row in data:
            self.cur.execute(sql,row)
            self.conn.commit()
        print("{} table {} duplicates success".format(self.today,sqlName))

    @classmethod
    def turncate_table(self,sqlName,type='today'):
        if type=='today':
            sql = 'delete from {} where spider_date={}'.format(sqlName,self.today)
            self.cur.execute(sql)
            print(sql)
        elif type == 'all':
            sql = 'truncate table {}'.format(sqlName)
            self.cur.execute(sql)
            print(sql)

    @classmethod
    def processing_toutiao(cls):
        # first combine talbe
        sql ="""
        select t1.*,t2.publish_date
        from
        (select *
        from leo_toutiao
        where spider_date ='{}'
        group by title,spider_date
        )t1
        left join
        (select *
        from leo_toutiao_date
        where spider_date ='{}'
        group by title,spider_date)t2
        on t1.title=t2.title
        group by t1.title,t1.spider_date
        """.format(cls.today,cls.today)
        cur = cls.conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        # then delete today's leo_toutiao_final
        sql = "DELETE FROM leo_toutiao_final where spider_date='{}'".format(cls.today)
        cls.cur.execute(sql)
        # Next: insert the data
        value = []
        for row in data:
            value.append(row)
        sql2 = "INSERT INTO leo_toutiao_final VALUES(%s,%s,%s,%s,%s,%s)"
        cur.executemany(sql2, value)
        cls.conn.commit()
        print('leo_toutiao_final is dupulicated')

