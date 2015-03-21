from peewee import *
from friend import *

class User(Model):
    email = CharField()
    password = CharField() #see if optional
    f_Name = CharField()
    l_Name = CharField()
    #  active = BooleanField()
    bday = CharField()
    profile_photo = CharField(default='nopro.jpg')
    # cityName = CharField()
    # state = CharField()
    # gender = CharField()
    # bio = CharField()
    # created = dateField( )

class UserHelper():
    def __init__(self, id):
        self.id = id

    def get_my_id(self):
        return self.id

    def get_friends(self):
        friends = []
        try:
            # get all friendships (both accepted and requested)
            for friendship in Friendship.select().where( ((Friendship.friend_user_id == self.id) | (Friendship.user_id == self.id)) & (Friendship.accepted == 1)):
                # we want the id of the friend, not of user_id
                if friendship.user_id == self.id:
                    friends.append(friendship.friend_user_id)
                else:
                    friends.append(friendship.user_id)

        except:
            friends = []

        return friends
