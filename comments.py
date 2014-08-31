from peewee import *
from datetime import datetime

class Comments(Model):
	user_id = IntegerField()
	# Status = 0
	# picture =1
	type_id = IntegerField(default = 0)
	# actual thing being commmented on
	item_id = IntegerField()
	# actual string comment
	comment = CharField()
	date_created = DateTimeField(default=datetime.now)

	# class Meta:
	# 	indexes = (
	# 	(('item_id', 'date_created', 'user_id'), True),)