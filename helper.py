from peewee import *
from person import *
from friend import *
from flask import *
from statuses import *
from datetime import datetime

def getPendingRequests(user_id):
	try:
		# find all pending request for current user
		pending_requests = Friendship.select().where((Friendship.user_id == user_id) & (Friendship.accepted == 0)).get()
		#for each request, get info of requester
		return [User.get(request.friend_user_id == User.id).f_Name for request in pending_requests.select()]
	except:
		return []


def getReqFriendships(user_id):
	friends = []
	try:
		for friendship in Friendship.select().where((Friendship.friend_user_id == user_id) & (Friendship.accepted == 1)):
			friend = User.get(User.id == friendship.user_id)
			friends.append(friend.f_Name)
		return friends
	except:
		return friends

def getAcceptedFrienships(user_id):
	friends = []
	try:
		for f in Friendship.select().where((Friendship.user_id == user_id) & (Friendship.accepted == 1)):
			friend = User.get(User.id == f.friend_user_id)
			friends.append(friend.f_Name)
		return friends
	except:
		return friends

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def getLikes(status):
	for s in status:
		try:
			likes = Likes.select().where(Likes.item_id == s.id)
			for like in likes:
				person = User.select().where(User.id == like.user_id).get()
				likers.append(person.f_Name)
				s.likers = likers
				s.likes = likes.count()
				return ':)'
		except:
			return ':('
