"""
定义字段类
"""

from mysql_control import Mysql

class Field():
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

# varchar
class StringField(Field):
    def __init__(self, name, column_type='varchar(255)', primary_key=False, default=None):
        super().__init__(name,column_type,primary_key,default)

# int
class IntegerField(Field):
    def __init__(self, name, column_type='int', primary_key=False, default=0):
        super().__init__(name,column_type,primary_key,default)

