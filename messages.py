from peewee import *
from datetime import datetime

db = SqliteDatabase('messages.db')
class Message(Model):
	sender_id = IntegerField()
	recipient_id = IntegerField()
	message = CharField()
	# date_created = DateTimeField(default=datetime.now)
