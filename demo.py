
class User(dict):
    class_name = 'User'

    def __init__(self,name,age,hight,**kwargs):
        super().__init__(**kwargs)
        print(kwargs)
        self.name = name
        self.age = age
        self.hight = hight

    def say_hi(self):
        print('my name is %s.'%self.name)

    @classmethod
    def play(cls):
        print(cls.class_name)


    def __getattr__(self, item):
        print(item)
        print('触发getattr')

user = User('gong','23',168, namse='gg',agef='4')
