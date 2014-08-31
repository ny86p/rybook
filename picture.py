from peewee import *
from datetime import datetime

class Picture(Model):
	# user who uploaded the picture
	user_id = IntegerField()
	# filename of the picture
	filename = CharField()
	date_created = DateTimeField(default=datetime.now)