from person import *
from datetime import date
from peewee import *
from friend import *
from statuses import *
from messages import *
from likes import *
from comments import *
from picture import *
# Picture.create_table()

# for r in Likes.select().join(Person).where(Likes.user_id == Person.id):
# 	print "Like " , r.id, r.item_id, r.date_created
# 	print "Person", r.email, r.f_Name, r.birthday

# db = SqliteDatabase('status.db')
# print db.execute_sql('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')



# for like in Likes.select():
# 	like.delete_instance()
# Person.create_table()
# Likes2.create_table()
# for s in Status.select():
# 	print s.likes
# Message.create_table()
 # for m in Message.select():
# 	print m.message, m.sender_id, m.recipient_id
# for friendship in Friendship.select():
# 	print friendship.user_id, friendship.friend_user_id, friendship.accepted
# 	print friendship.id
# for f in Friendship.select():
# 	f.delete_instance()
# db = SqliteDatabase('peewee.db')
# db.drop_table(Message)
# Message.create_table()

# db = SqliteDatabase('people.db')
# for i in range(7):
# 	p = Person.create(bday = date(2013,6,22), password = 'p' + str(i),f_Name = 'user' + str(i), l_Name = 'last' + str(i), email = 'e' + str(i),)
# p.save()
# for i in range(5):
# 	m = Message.create(sender_id = i, recipient_id = i+2, message = "Fake info")
# 	s = Status.create(creater_id=i, status = "test")
# 	pics = Picture.create(user_id = i+1,filename ="url.jpeg")
# m.save()
# s.save()
# pics.save()

# for i in range(5):
# 	c = Comments.create(user_id = i+2,item_id = i,comment = 'comment here')
# 	l = Likes.create(user_id = i+1, item_id = i+2)
# c.save()
# l.save()
for i in range(6):
	f = Friendship.create(user_id = i, friend_user_id = i+1, accepted = 1)
# for person in Person.select():
	# print person.email, person.password, person.id
	# print person.id
	# person.delete_instance()


# current_user = Person.get(Person.email == 'e0', Person.password == 'p0')
# print current_user
