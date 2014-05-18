from peewee import *

db = SqliteDatabase('status.db')
class Status(Model):
	creater_id = IntegerField()
	# likes = []
	status = CharField()
	
	# dateCreated = CharField()