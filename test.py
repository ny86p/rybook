from person import *
from datetime import date
from peewee import *
from friend import *
from statuses import *
from messages import *
from likes import *
from comments import *
from picture import *

Friendship.create_table()
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
# db = SqliteDatabase('friendship.db')
# db.drop_table(Friendship)

# db = SqliteDatabase('people.db')
# for i in range(5):
#  	p = Person.create(birthday = date(2013,6,22), password = 'p' + str(i),f_Name = 'user' + str(i), l_Name = 'last' + str(i), email = 'e' + str(i), person_id = i)
#  	p.save()
# for person in Person.select():
# 	print person.email, person.password, person.id
# 	print person.id
	# person.delete_instance()


# current_user = Person.get(Person.email == 'e0', Person.password == 'p0')
# print current_user
