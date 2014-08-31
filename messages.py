from peewee import *
from datetime import datetime

class Message(Model):
	sender_id = IntegerField()
	recipient_id = IntegerField()
	message = CharField()
	date_sent = DateTimeField(default=datetime.now)
