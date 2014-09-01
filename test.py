from person import *
from datetime import date
from peewee import *
from friend import *
from statuses import *
from messages import *
from likes import *
from comments import *
from picture import *


Person.drop_table()
Person.create_table()
for i in range(7):
	p = Person.create(bday = date(2013,6,22), password = 'p' + str(i),f_Name = 'user' + str(i), l_Name = 'last' + str(i), email = 'e' + str(i),)
	p.save()

Message.drop_table()
Message.create_table()
for i in range(1,5):
	m = Message.create(sender_id = i, recipient_id = i+2, message = "Fake info")
	m.save()

Status.drop_table()
Status.create_table()
for i in range(1,5):
	s = Status.create(creater_id=i, status = "test")
	s.save()

Picture.drop_table()
Picture.create_table()
for i in range(5):
	pics = Picture.create(user_id = i+1,filename ="url.jpeg")
	pics.save()

Likes.drop_table()
Likes.create_table()
for i in range(5):
	l = Likes.create(user_id = i+1, item_id = i+2)
	l.save()

Comments.drop_table()
Comments.create_table()
for i in range(1,5):
	c = Comments.create(user_id = i+2,item_id = i,comment = 'comment here')
	c.save()

Friendship.drop_table()
Friendship.create_table()
for i in range(1,6):
	f = Friendship.create(user_id = i, friend_user_id = i+1, accepted = 1)
	f.save()
