from peewee import *

db = SqliteDatabase('people.db')
class Person(Model):
    email = CharField()
    password = CharField() #see if optional
    f_Name = CharField()
    l_Name = CharField()
    #  active = BooleanField()
    bday = CharField()
    profile_photo = CharField(default='nopro.jpg')
    # cityName = CharField()
    # state = CharField()
    # gender = CharField()
    # bio = CharField()
    # created = dateField( )
    class Meta:
		database = db
