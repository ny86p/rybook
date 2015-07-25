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