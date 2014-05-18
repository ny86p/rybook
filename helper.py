from peewee import *
from person import *
from friend import *
from flask import *
from statuses import *
from datetime import datetime

def getPendingRequests(user_id):
	request_names =  []
	try:
		pending_requests = Friendship.select().where((Friendship.user_id == user_id) & (Friendship.accepted == 0)).get()
		person = Person.get(Person.id == pending_requests.friend_user_id)
		for request in pending_requests.select():
			if person.f_Name not in request_names:
				if request.accepted != 0:
					request_names.append(person.f_Name)
		return request_names
	except:
		return request_names

def getStatuses(user_id):
	status = []
	try:
		for statuses in Status.select().where(Status.creater_id == user_id):
			status.append(statuses)
		return status
	except:
		return 'not'

def getReqFriendships(user_id):
	friends = []
	try:
		for friendship in Friendship.select().where((Friendship.friend_user_id == user_id) & (Friendship.accepted == 1)):
			friend = Person.get(Person.id == friendship.user_id)
			friends.append(friend.f_Name)
		return friends
	except:
		return friends

def getAcceptedFrienships(user_id):
	friends = []
	try:
		for f in Friendship.select().where((Friendship.user_id == user_id) & (Friendship.accepted == 1)):
			friend = Person.get(Person.id == f.friend_user_id)
			friends.append(friend.f_Name)
		return friends
	except:
		return friends

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
