from peewee import *
from datetime import datetime

db = SqliteDatabase('status.db')
class Status(Model):
	creater_id = IntegerField()
	# likes = []
	status = CharField()
	date_created = DateTimeField(default=datetime.now)

	# date_created = CharField(default = datetime.now)
def getStatuses(user_id):
	status = []
	try:
		# sort by date created - descending
		for statuses in Status.select().where(Status.creater_id == user_id):
			status.append(statuses)
		status.reverse()
		return status
	except:
		return 'not'
