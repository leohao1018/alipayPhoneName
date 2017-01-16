#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author leo hao
# os windows 7

import pymssql


class Business:
    @staticmethod
    def get_users():
        userlist = []
        # u = UserInfo('彭乐乐', '362528199511050519')
        # userlist.append(u)
        # u = UserInfo('陆洪伟', '321322199401262230')
        # userlist.append(u)
        # u = UserInfo('王鑫', '370702197908076512')
        # userlist.append(u)
        # u = UserInfo('吕明', '420983198902014415')
        # userlist.append(u)
        # u = UserInfo('谢念', '522122198905222024')
        # userlist.append(u)
        # u = UserInfo('盛方龙', '330182199209011753')
        # userlist.append(u)
        # u = UserInfo('路爱梅', '150125198205144529')
        # userlist.append(u)
        u = UserInfo('王兴', '330183198609221129')
        userlist.append(u)
        u = UserInfo('宫乐', '341125199201233816')
        userlist.append(u)
        u = UserInfo('李明', '342401197004073419')
        userlist.append(u)
        return userlist

    @staticmethod
    def get_phones():
        phones = []

        conn = pymssql.connect(host='.\sql2008r2', user='sa', password='1qaz@WSX', database='alipay')
        cur = conn.cursor()
        cur.execute("SELECT top 19 Id, Phone, RealName FROM dbo.PhoneRealName WITH (NOLOCK) WHERE Status = 0 ORDER BY Id")
        for row in cur:
            phones.append(PhoneRealName(row[0], row[1], row[2]))
        conn.close()

        return phones

    @staticmethod
    def update_real_name_by_phone(phone, realname, remark):
        if phone is not None and phone != '' and realname is not None and realname != '':
            conn = pymssql.connect(host='.\sql2008r2', user='sa', password='1qaz@WSX', database='alipay')
            cur = conn.cursor()

            sql = "UPDATE dbo.PhoneRealName SET RealName = '%s', Remark = '%s', Status = 1, UpdateTime = GETDATE() WHERE Phone = '%s'" % (
            realname, remark, phone)

            sql = sql.encode('utf-8')
            res = cur.execute(sql)
            print(res)
            conn.commit()
            conn.close()


class UserInfo:
    def __init__(self, username, certno):
        self.UserName = username
        self.CertNo = certno


class PhoneRealName:
    def __init__(self, Id, Phone, RealName):
        self.Id = Id
        self.Phone = Phone
        self.RealName = RealName
