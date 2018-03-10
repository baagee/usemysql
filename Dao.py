# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Author :       dangliuhui
   date：          2018/3/9
-------------------------------------------------
"""
from .MySQLDB import MySQLDB


class Dao(object):
    __table = ''
    mysql_db_obj = None
    table_schemas = {}

    def __init__(self, config):
        self.mysql_db_obj = MySQLDB(config)

    def set_table(self, table):
        """
        设置当前操作表
        :param table: 表名
        :return: self
        """
        self.__table = table
        if table not in self.table_schemas:
            self.__get_table_desc()
        return self

    def get_table(self):
        """
        获取当前操作表
        :return: 表名
        """
        return self.__table

    def create(self, data={}):
        """
        插入数据
        :param data: 数据字典
        :return: 插入ID
        """
        fields = ''
        values = []
        holder = ''
        for field, value in data.items():
            if field in self.table_schemas[self.__table]['fields'].keys():
                fields += '`' + field + '`,'
                values.append(value)
                holder += '%s,'
        fields = fields.strip(',')
        holder = holder.strip(',')
        sql = 'INSERT INTO `%s`(%s) VALUES (%s)' % (self.__table, fields, holder)
        return self.mysql_db_obj.insert(sql, values)

    def batch_create(self, data=[]):
        pass

    def get_all(self, conditions, fields=['*'], group_by='', having={}, order_by={}, limit=[]):
        """
        查找所有满足条件的
        :param conditions: 条件
        :return: 结果列表 [{},{}]
        """
        sql = 'SELECT '
        where, values = self.__where(conditions)
        for field in fields:
            if field == '*':
                sql += ' * '
                break
            else:
                if field in self.table_schemas[self.__table]['fields'].keys():
                    sql += '`' + field + '`,'
        sql = sql.strip(',') + ' FROM `%s` WHERE %s' % (self.__table, where)
        if group_by != '':
            sql += ' GROUP BY `%s`' % (group_by)
        if len(having) > 0:
            having_, values_ = self.__where(having)
            values.extend(values_)
            sql += ' HAVING %s' % (having_)
        if len(order_by) > 0:
            order_by_str = ''
            for k, v in order_by.items():
                order_by_str += ' `%s` %s,' % (k, v.upper())
            sql += ' ORDER BY%s' % order_by_str.strip(',')
        if len(limit) > 0:
            sql += ' LIMIT %s' % (','.join(map(str, limit)))
        return self.mysql_db_obj.get_all(sql, values)

    def get_one(self, conditions):
        """
        查找一条记录
        :param conditions: 条件
        :return: 字典
        """
        where, values = self.__where(conditions)
        sql = 'SELECT * FROM `%s` WHERE %s LIMIT 1' % (self.__table, where)
        return self.mysql_db_obj.get_one(sql, values)

    def save(self, conditions, data):
        """
        更新数据
        :param conditions: 条件
        :param data: 更新字典
        :return: 影响函数
        """
        values = []
        fields = ''
        where, values_ = self.__where(conditions)

        for field, value in data.items():
            if field in self.table_schemas[self.__table]['fields'].keys():
                fields += '`' + field + '` = %s,'
                values.append(value)
        values.extend(values_)
        fields = fields.strip(',')
        where = where.strip('AND')
        sql = 'UPDATE `%s` SET %s WHERE %s' % (self.__table, fields, where)
        return self.mysql_db_obj.update(sql, values)

    def delete(self, conditions):
        """
        删除数据
        :param conditions: 删除条件
        :return: 影响行数
        """
        where, values = self.__where(conditions)
        sql = 'DELETE FROM `%s` WHERE %s' % (self.__table, where)
        return self.mysql_db_obj.delete(sql, values)

    def __where(self, conditions):
        """
        :param conditions:
        {
            filed:[>|<|=|like,value],
            field:[[not] in,[1,2,3,4,5]]
            field:[[not] between,[1,20]]
        }
        :return: where values
        """
        where = ''
        values = []
        for field, item in conditions.items():
            if field in self.table_schemas[self.__table]['fields'].keys():
                if item[0].upper() in 'NOT IN':
                    val_str = ''
                    if (isinstance(item[1], list)):
                        for i in item[1]:
                            if isinstance(i, str):
                                val_str += '"%s",' % i
                            elif isinstance(i, int):
                                val_str += '%s,' % i
                        where += '`' + field + '` ' + item[0].upper() + ' (' + val_str.strip(',') + ') AND '
                    else:
                        raise Exception('conditions error')
                elif item[0].upper() in 'NOT BETWEEN':
                    if isinstance(item[1], list):
                        where += '`' + field + '` ' + item[0].upper() + ' %s AND %s AND '
                        values.append(item[1][0])
                        values.append(item[1][1])
                    else:
                        raise Exception('conditions error')
                else:
                    where += '`' + field + '` ' + item[0].upper() + ' %s AND '
                    values.append(item[1])
        where = where.strip('AND ')
        return (where, values)

    def __get_table_desc(self):
        """
        获取表结构
        :return:
        """
        sql = 'DESC `%s`' % self.__table
        res = self.mysql_db_obj.get_all(sql, [])
        self.table_schemas[self.__table] = {}
        self.table_schemas[self.__table]['fields'] = {}
        for column in res:
            self.table_schemas[self.__table]['fields'][column.get('Field')] = {
                'type': column.get('Type'),
                # 'default': column.get('Default'),
                # 'is_null': column.get('Null')
            }
            if column.get('Key') == 'PRI':
                self.table_schemas[self.__table]['primary_key'] = column.get('Field')
            if column.get('Extra') == 'auto_increment':
                self.table_schemas[self.__table]['auto_increment'] = column.get('Field')

        print(self.table_schemas)
