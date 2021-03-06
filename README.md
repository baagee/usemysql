# usemysql
python简单的方式使用mysql数据库，分为Dao类和MySQLDB类

### install

- cd usmysql
- tar zxvf usemysql-1.0.tar.gz
- cd usemysql-1.0
- python3 setup.py install


### 简单实例：

>dao_test.py

```python
from usemysql.Dao import Dao
import time

# 数据库配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'xxxxx',
    'database': 'spider',
    'port': 3306,
    'charset': 'utf8'
}
# 参数：连接数据库配置和操作的表名
dao = Dao(config=db_config).set_table(table='plant')
print(dao.get_table())
#切换数据库
dao.set_table('table_test')
res = dao.sum('aaa', {'id': ['>', 2]})
print(res)

res = dao.count('aaa', {'id': ['>', 2]})
print(res)

res = dao.avg('aaa', {'id': ['>', 2]})
print(res)

res = dao.min('aaa', {'id': ['>', 2]})
print(res)

res = dao.max('aaa', {'id': ['>', 2]})
print(res)
# 批量插入数据
res = dao.batch_create([
    {
        'name': 'name4',
        'price': 11.34,
        'aaa': 8976543345678,
        'text': 'textsdfhfd'
    },
    {
        'name': 'name4',
        'price': 11.34,
        'aaa': 8976543345678,
        'text': 'textsdfhfd'
    },
    {
        'name': 'name4',
        'price': 11.34,
        'aaa': 8976543345678,
        'text': 'textsdfhfd'
    },
])
print('批量插入:%s' % res)

#切换操作的数据库 
dao.set_table('plant')
# 插入数据
data = {
    'zhongming': 'zongming',
    'xueming': 'xueming',
    'bieming': '.bieming',
    'ke': 'kie',
    'shu': 'shu',
    'xingtai': 'xingtai',
    'candi': 'candi',
    'xixing': 'xixing',
    'fanzhi': 'fanzhi',
    'yongtu': 'yongtu',
    'insert_time': int(time.time())
}
# 插入，返回插入ID
insert_id = dao.create(data)
print('插入ID：%s' % insert_id)

# 更改数据记录
res = dao.save({'id': ['=', insert_id], 'candi': ['=', 'candi']}, {'candi': '哈哈', 'yongtu': '用途'})
print('保存：%s' % res)

# 删除条件
con = {
    'id': ['=', insert_id,'and'],
    'candi': ['like', '%candi%','or'],
    'ke': ['in', ['ke', 'ddd'],'and'],
    'insert_time': ['between', [0, int(time.time())]]
}
# 删除
res = dao.delete(con)
print('删除:%s' % res)

# 获取一条记录，返回字典
res = dao.get_one({'id': ['>', insert_id - 10]})
print('查找%s' % res)

# 获取多条记录，返回列表，eg:[{},{}....]
res = dao.get_all({
    'id': ['>', insert_id - 10],
    'insert_time': ['between', [0, int(time.time())]]
}, ['id', 'ke', 'shu', 'candi'], 'candi', {'ke': ['=', 'kie']}, order_by={'id': 'desc', 'insert_time': 'desc'},
    limit=[0, 20])
print('查找%s' % res)

# 执行sql语句
print(dao.mysql_db_obj.get_one('select * from plant where id=%s', [1200]))
```

关于条件，需满足这种形式，默认and连接
```
{
	'filed1':['>|<|=|like','value1','and],
	'field2':['not in'|'in',[1,2,3,4,5],'or']
	'field3':['not between'|'between',[min,max]]
}
```
---
>mysqldb_test.py

```python
from usemysql.MySQLDB import MySQLDB

# 连接数据库配置文件
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'xxxxxx',
    'database': 'spider',
    'port': 3306,
    'charset': 'utf8'
}
# 获取一个数据库实例
mysql_db = MySQLDB(db_config)

# 批量插入数据
sql = 'insert into table_test(name, price, aaa, text) VALUES (%s,%s,%s,%s)'
data = [
    ['name1', 11.11, 11111, 'text1'],
    ['name2', 11.12, 22222, 'text2'],
    ['name3', 11.13, 33333, 'text3'],
]
print(mysql_db.batch_insert(sql, data))

# 查询多条数据，返回列表，eg:[{},{}....]
data = mysql_db.get_all('select * from plant where id<%s', [10])
print(data)

# 插入数据
sql = 'insert into plant (zhongming, xueming, bieming, ke, shu, xingtai, candi, xixing, fanzhi, yongtu, insert_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
datas = ['事实上', 'ssss', 'dsfgsd', 'dsgfsd', 'dd', 'fdd', 'dsf', 'eee', 'dfsd', 'fgds', 1243423488]
insert_id = mysql_db.insert(sql, datas)
print(insert_id)

# 删除数据
sql = 'DELETE FROM plant WHERE id=%s'
res = mysql_db.delete(sql, [insert_id])
print(res)

# 更新数据
sql = 'update plant set ke=%s where id=%s'
res = mysql_db.update(sql, ['hello world', insert_id])
print(res)

# 查询一条记录 返回字典
sql = 'select * from plant where id=%s'
res = mysql_db.get_one(sql, [insert_id])
print(res)
```