from peewee import *
from datetime import datetime

db = SqliteDatabase('status.db')
class Likes2(Model):
	user_id = IntegerField(primary_key = True)
	# Status = 0
	type_id = IntegerField(default = 0)
	item_id = IntegerField(primary_key = True)
	date_created = DateTimeField(default=datetime.now)
