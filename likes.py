from peewee import *
from datetime import datetime
class Likes(Model):
	user_id = IntegerField()
	# Status = 0
	type_id = IntegerField(default = 0)
	item_id = IntegerField()
	date_created = DateTimeField(default=datetime.now)

