from mongoengine import *  
connect('Virtual-Library')

class MyDocument(Document):
    @classmethod
    def get_or_create(cls, **kwargs):
        if len(cls.objects.filter(**kwargs)) == 1:
            return cls.objects.get(**kwargs)
        else:
            return cls.objects.create(**kwargs)
    @classmethod
    def get_or_skip(cls, **kwargs):
        if len(cls.objects.filter(**kwargs)) == 1:
            return cls.objects.get(**kwargs)
        else:
            return None
    meta = {
        'allow_inheritance' : True,
        'abstract' : True
    }

class AdminStaff (MyDocument):
    member= IntField(required=True)

class Library(MyDocument):
    ISBN = IntField(required=True)
    bookcase = IntField(default=0)
    title = StringField(default='none')
    author = StringField(default='none')
    bookshelf = IntField(default=0)

class TakenBooks(MyDocument):
    ISBN = ReferenceField(Library)
    whotook = IntField()
    retrieved = BooleanField()
