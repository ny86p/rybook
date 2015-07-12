from peewee import *
from datetime import datetime
from person import *

class Picture(Model):
	user = ForeignKeyField(User, null = True, related_name = "pictures")
	# filename of the picture
	filename = CharField()
	date_created = DateTimeField(default=datetime.now)