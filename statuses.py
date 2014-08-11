from peewee import *
from datetime import datetime

db = SqliteDatabase('status.db')
class Status(Model):
	creater_id = IntegerField()
	# likes = []
	status = CharField()
	date_created = DateTimeField(default=datetime.now)

	# date_created = CharField(default = datetime.now)