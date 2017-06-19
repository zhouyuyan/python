# -*- coding:utf-8 -*-
import cx_Oracle
import time


class connect(object):
    def oracle_connect(self, mobile):
        # 获取当前日期
        t = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 配置oracle数据库账号及密码
        conn = cx_Oracle.connect('用户名/密码')
        cursor = conn.cursor()
        # 查询验证码SQL，返回短信内容
        sql = r"select * from (select sms_inf from gwadm.SMSTSMmO where mbl_no = " + "'" + mobile + "'" + " and tx_dt = " + t + " order by OPR_TM desc)where rownum <= 1"
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        code = []
        # 遍历短信内容取出数字
        for i in row[0]:
            if i.isdigit():
                code.append(i)
        return ''.join(code)


if __name__ == "__main__":
    mobile = "手机号"
    conn = connect()
    tt = conn.oracle_connect(mobile)
    print(tt)
