from peewee import *

class User(Model):
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
# class Users_Albums(Model):
#     user = ForeignKeyField(User)
#     album = ForeignKeyField(Album)