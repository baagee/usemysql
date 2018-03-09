# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Author :       dangliuhui
   date：          2018/3/9
-------------------------------------------------
"""
import pymysql


class MySQLDB(object):
    link = None
    cursor = None

    def __init__(self, config):
        config = {
            'host': config.get('host', 'localhost'),
            'port': config.get('port', 3306),
            'user': config.get('user'),
            'password': config.get('password'),
            'db': config.get('database'),
            'charset': config.get('charset', 'utf8'),
            'cursorclass': pymysql.cursors.DictCursor
        }
        try:
            self.link = pymysql.connect(**config)
            self.cursor = self.link.cursor()
            print("Database connected")
        except Exception as e:
            raise e

    def update(self, sql, params=[]):
        """
        更新数据
        :param sql: 更新sql
        :param params:  参数
        :return:
        """
        return self.__execute(sql, params)

    def get_all(self, sql, params=[]):
        """
        查询数据
        :param sql: 查询sql
        :param params:  参数
        :return: 返回结果列表[{},{}]
        """
        res = self.__execute(sql, params)
        if res > 0:
            return self.cursor.fetchall()
        else:
            return None

    def get_one(self, sql, params=[]):
        """
        获取一个
        :param sql: 查询语句
        :param params: 参数
        :return: 返回结果字典
        """
        res = self.__execute(sql, params)
        if res > 0:
            return self.cursor.fetchone()
        else:
            return None

    def insert(self, sql, params=[]):
        """
        插入数据
        :param sql:要执行的sql语句
        :param params: sql语句里绑定参数
        :return: 返回插入ID
        """
        res = self.__execute(sql, params)
        if res == 1:
            return self.cursor.lastrowid
        else:
            return None

    def delete(self, sql, params=[]):
        """
        删除数据
        :param sql: 删除sql
        :param params:  参数
        :return:
        """
        return self.__execute(sql, params)

    def __del__(self):
        if self.cursor != None:
            self.cursor.close()
        if self.link != None:
            self.link.close()
            print('Database connection closure')

    def __execute(self, sql, params):
        try:
            count = self.cursor.execute(sql, params)
            self.link.commit()
            return count
        except Exception as e:
            self.link.rollback()
            raise e
