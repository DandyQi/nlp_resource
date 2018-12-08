# -*- coding: utf-8 -*-

# Author: Dandy Qi
# Created time: 2018/12/7 14:42
# File usage: database operation

import pymysql
import configparser


class DBProcess:
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read("config.conf")

        db_host = cf.get("db", "db_remote_host")
        db_user = cf.get("db", "db_user")
        db_password = cf.get("db", "db_password")
        db_table = cf.get("db", "db_table")

        self.db = pymysql.connect(db_host, db_user, db_password, db_table)

    def get_word(self, token):
        sql = "SELECT category, norm_token, extra " \
              "FROM entity " \
              "WHERE (token='%s' OR norm_token='%s' OR find_in_set('%s', synonym))" \
              "UNION " \
              "SELECT category, norm_token, extra " \
              "FROM relation " \
              "WHERE (token='%s' OR norm_token='%s' OR find_in_set('%s', synonym))" \
              % (token, token, token, token, token, token)
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(sql)
            print(e)

    def fetch_lexicon(self):
        sql = "SELECT token, synonym, norm_token, pos FROM entity " \
              "UNION SELECT token, synonym, norm_token, pos FROM relation"
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(sql)
            print(e)


if __name__ == "__main__":
    db = DBProcess()
    res = db.fetch_lexicon()

    print(res)
