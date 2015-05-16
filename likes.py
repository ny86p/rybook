from peewee import *
from datetime import datetime
from person import *

class Likes(Model):
	user = ForeignKeyField(User, null = True,related_name = "likes")
	# Status = 0
	type_id = IntegerField(default = 0)
	item_id = IntegerField()
	date_created = DateTimeField(default=datetime.now)


