```text
ORM: 对象关系映射
类 ----> 表
对象 ----> 一条记录
对象.属性 ----> 一条记录的字段

1.字段类:
    Field:
        字段名，字段类型，是否为主键，默认值
        varchar(Field)
            name, varchar(64), primary_key=False, default=None

        int(Field)
            name, int, primary_key=False, default=0

2.模型表类

# 继承字典类型，可接收任意个数的关键字参数
Models(dict, metaclass=OrmMetaClass):
    def __init__(self, **kwargs):
        super().__init__(**kwarg)

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

User(Models):
    table_name = 'user_info'

Movie(Models):

# 取值:
    dict.get(key)
    dict[key]

    dict.key

# 存值:
    dict[key] = value
    dict.name = 'tank'


3.元类控制类的创建:
    1.表名
    2.只能有一个主键
    3.把所有的字段，放入一个空的字典中，也就是定义的mappings

class OrmMetaClass(type):

    def __new__(cls, class_name, class_bases, class_attr):

        # 1.过滤Models类
        if class_name == 'Models':
            return type.__new__(cls, class_name, class_bases, class_attr)


        # 2.限制表类的创建
        # 表名
        table_name = class_attr.get('table_name', class_name)

        # 主键
        primary_key = None

        # 存放字段的字典，mappings
        mappings = {}

        # 两件事情: 把所有的字段都添加到mappings中，
        # 获取主键值，以及限制只能有一个主键

        # key---> 字段名   value---> 字段对象
        for key, value in class_attr.items():
            if isinstance(value, Field):
                mappings[key] = value
                if value(字段对象).primary_key:
                    if primary_key:
                        raise TypeError('只能有一个主键')
                    primary_key = value(字段对象).name
                    # primary_key = key

        if not primary_key:
            raise TypeError('必须要有一个主键')

        for key in mappings.keys():
            class_attr.pop(key)

        class_attr['table_name'] = table_name
        class_attr['primary_key'] = primary_key
        class_attr['mappings'] = mappings

        return type.__new__(cls, class_name, class_bases, class_attr)


4.获取数据库连接:
import pymysql
class Mysql:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls,  *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.conn = pymysql.connect(
            配置信息
        )

        # 获取游标
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    # 封装查询
    def select(self, sql, args=None):
        self.cursor.execute(sql, args)
        res = self.cursor.fetchall()  # [{}, {}...]
        return res

    # 封装提交(插入，更新)
    def execute(self, sql, args):
        try:
            self.cursor.execute(sql, args)

        except Exception as e:
            print(e)



6.给Models类封装 查询， 插入， 更新方法
from 昨日回顾 import Mysql
@classmethod
def my_select(cls, **kwargs):
    ms = Mysql()
    # 查所有
    if not kwargs:
        sql = 'select * from %s' % cls.table_name
        res = ms.select(sql)  # [{}, {}]

    # 根据查询条件查询
    else:
        key = list(kwargs.keys())[0]
        value = kwargs.get(key)
        sql = 'select * from %s where %s=?'  % (cls.table_name, key)
        sql = sql.replace('?', '%s')
        res = ms.select(sql, value)  # [{}, {}]

    if res:
        [cls(**{key:value}) for d in res]
        cls(key=value})
        return [cls(**d) for d in res]  # user_obj(dict)
        return res # dict
User.select()
User.select(name='tank')

# 插入
def save(self):
    ms = Mysql()
    fields = []
    values = []
    args = []
    for key, value in self.mappings.items():
        # 过滤主键
        if not value.primary_key:
            fields.append(
                value.name
                # key
            )
            values.append(
                getattr(self, value.name, value.default)
            )
            args.append('?')

    # sql = 'insert into %s(字段名,...) values(字段值,...,??)'
    sql = 'insert into %s(%s) values(%s)' % (
        self.table_name, ','.join(fields), ','.join(args)
    )

    sql = sql.replace('?', '%s')
    ms.execute(sql, values)


# 更新
def update(self):
ms = Mysql()
    fields = []
    values = []
    # 主键值
    primary_key = None
    for key, value in self.mappings.items():
        # 过滤主键
        if value.primary_key:
            primary_key = getattr(self, value.name, value.default)

        else:
            fields.append(
                value.name + '=?'
            )
            values.append(
                getattr(self, value.name, value.default)
            )

    sql = 'update %s set 字段名=字段值 where id=1'
    sql = 'update %s set %s=?, %s=? where %s=%s'

    sql = 'update %s set %s where %s=%s' % (
        self.table_name, ','.join(fields), self.primary_key,primary_key
    )
    sql = sql.replace('?', '%s')
    ms.execute(sql, values)
```
