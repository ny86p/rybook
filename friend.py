from peewee import *

db = SqliteDatabase('friendship.db')
class Friendship(Model):
	user_id = IntegerField()
	friend_user_id = IntegerField()
	# 0 = pending, 1 = accepted, -1 = declined 
	accepted = IntegerField(default = 0)
	# created = DateTimeField()