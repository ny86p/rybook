from peewee import *
from datetime import datetime
from picture import *


class Album(Model):
	# user who created the album
	user_id = IntegerField()
	# filename of the picture
	name = CharField()
	isProfilePhoto = BooleanField(default=False)
	date_created = DateTimeField(default=datetime.now)

class Albums_Pictures(Model):
	album = ForeignKeyField(Album)
	picture = ForeignKeyField(Picture)
	# album_id = IntegerField(index = True )
	# picture_id = IntegerField(index = True )
	
	# class Meta:
	# 	primary_key = CompositeKey('album', 'picture')

