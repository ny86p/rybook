from UserHelper import *
from likes import *

class LikesHelper():

	@staticmethod
	def getMessage(session_id, item_id, type_id):
		print session_id, "session_id"
		session_user_friends = UserHelper(session_id).get_friends()
		print session_user_friends, "friends"
		friend_likers = []

		try:
			item_likes = Likes.select().where((Likes.item_id == item_id) & (Likes.type_id == type_id))
			try:
				item_likes = list(item_likes)
			except:
				item_likes = [item_likes]
		except:
			item_likes = []

		print item_likes
		num_likes_on_item = len(list(item_likes))
		you_liked = False
		non_friend_message = ""
		# TODO: Get all user_ids from item_likes 
		# if friend.id in item_user_ids then append

		# Checking if a friend of the current  user likes this particular item
		for like in item_likes:
			for friend in session_user_friends:
				if like.user.id == friend.id:
					friend_likers.append(friend)
				if int(like.user.id) == int(session_id):
					you_liked = True

		non_friend_likes = num_likes_on_item - len(friend_likers) - int(you_liked)
		if non_friend_likes == 1: 
			non_friend_message = "1 other likes this"
		elif non_friend_likes > 1:
			non_friend_message = str(non_friend_likes) + " others like this"

		if num_likes_on_item == 0:
			message = "No likes"
		elif num_likes_on_item == 1 and you_liked:
			message = "You like this"
		else:
			message = non_friend_message

		if( friend_likers ):
			first_friend_first_name = friend_likers[0].f_Name
			if( len(friend_likers) > 1):
				second_friend_first_name = friend_likers[1].f_Name
				if non_friend_likes > 0:
					message = first_friend_first_name + "," + second_friend_first_name + " and " + non_friend_message
				else:
					message = first_friend_first_name + "," + second_friend_first_name + " like this"
				if you_liked:
					message = "You, " + message
			else:
				if non_friend_likes > 0:
					message = first_friend_first_name + " and " + non_friend_message
					if you_liked:
						message = "You, " + message 
				else:
					message = first_friend_first_name + " likes this"
					if you_liked:
						message = "You and " + first_friend_first_name + " like this"
		return message
	
	@staticmethod
	def was_item_liked_by_user(user_id, item_id, type_id):
		likes = Likes.select().where((Likes.item_id == item_id) & (Likes.type_id == type_id))
		for like in likes:
			if user_id == int(like.user.id):
				return True
		return False

