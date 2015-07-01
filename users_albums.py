from person import *
from album import *

class Users_Albums(Model):
    user = ForeignKeyField(User)
    album = ForeignKeyField(Album)