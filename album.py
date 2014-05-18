from peewee import *
from datetime import datetime


class Album(Model):
	# user who created the album
	user_id = IntegerField()
	# filename of the picture
	name = CharField()
	date_created = DateTimeField(default=datetime.now)
