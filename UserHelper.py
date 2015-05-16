from friend import *
from person import *
class UserHelper():
    def __init__(self, id):
        self.id = int(id)

    def get_my_id(self):
        return self.id

    def get_friends(self):
        friends = []
        try:
            # get all friendships (both accepted and requested)
            for friendship in Friendship.select().where( ((Friendship.friend_user_id == self.id) | (Friendship.user_id == self.id)) & (Friendship.accepted == 1)):
                # we want the id of the friend, not of user_id
                if friendship.user_id == self.id:
                    friend_id = friendship.friend_user_id
                else:
                    friend_id = friendship.user_id
                    
                friend = User.get(User.id == friend_id)
                friends.append(friend)

        except:
            friends = []

        return friends

