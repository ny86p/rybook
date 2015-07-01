from person import *
from datetime import date
from peewee import *
from friend import *
from statuses import *
from messages import *
from likes import *
from comments import *
from picture import *
from users_albums import *
from album import *

User.drop_table(True)
User.create_table()
for i in range(1,7):
	p = User.create(bday = date(2013,6,22), password = 'p' + str(i),f_Name = 'user' + str(i), l_Name = 'last' + str(i), email = 'e' + str(i),)
	p.save()

Message.drop_table(True)
Message.create_table()
for i in range(1,5):
	m = Message.create(sender_id = i, recipient_id = i+2, message = "Fake info")
	m.save()

Status.drop_table(True)
Status.create_table()
for i in range(1,5):
	s = Status.create(creater_id=i, status = "test")
	s.save()

Likes.drop_table(True)
Likes.create_table()
for i in range(5):
	l = Likes.create(user = i+1, item_id = i+2)
	l.save()

Comments.drop_table(True)
Comments.create_table()
for i in range(1,5):
	c = Comments.create(user = i+2,item_id = i,comment = 'comment here')
	c.save()

Friendship.drop_table(True)
Friendship.create_table()
for i in range(1,6):
	f = Friendship.create(user_id = i, friend_user_id = i+1, accepted = 1)
	f.save()

Album.drop_table(True)
Users_Albums.drop_table(True)
Album.create_table()
Users_Albums.create_table()
for i in range(1,7):
	a = Album.create(user_id = i, name = "Profile Pictures")
	a.save()
	u = Users_Albums.create(user = i, album = i)
	u.save()



Picture.drop_table(True)
Albums_Pictures.drop_table(True)
Picture.create_table()
Albums_Pictures.create_table()
for i in range(5):
	pics = Picture.create(user = i+1,filename ="nopro.jpg")
	pics.save()
	
	print "album = ", i + 1
	print "picture = ", i + 1
	# a_pic = Albums_Pictures.create(album_id = i+1, picture_id = i + 1)
	a_pic = Albums_Pictures.create(album = i+1, picture = i + 1)

	a_pic.save()
