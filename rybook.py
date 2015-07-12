from flask import *
from peewee import *
import sendemail
from person import *
from friend import *
from picture import *
from sendemail import *
from helper import *
from statuses import *
from messages import *
from likes import *
from UserHelper import *
from LikesHelper import *
from album import *
from users_albums import *
import os
from comments import *
from werkzeug.utils import secure_filename
import constants
import sys


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in  app.config['ALLOWED_EXTENSIONS']

@app.route('/profile/<user_id>')
def profile(user_id):
	viewer = User.select().where(User.id == session['id']).get()
	# Grab current_users info
	current_user = User.select().where(User.id == user_id).get()
	# check if the person viewing page is the owner
	current_user.owner = str(user_id) == str(session['id'])

	statuses= getStatuses(user_id)
	commenters = []
	for s in statuses:
		s.type_id = constants.types['status']
		s.like_message = LikesHelper.getMessage(session["id"], s.id, s.type_id)
		s.is_liked_by_you = LikesHelper.was_item_liked_by_user(session["id"], s.id, s.type_id)
		if s.date_created:
			s.date_created = datetime.strftime(s.date_created, '%m/%d/%Y %I:%M%p')

		s.comments = Comments.select().where(Comments.item_id == s.id)
		for c in s.comments:
			c.type_id = constants.types['comment']
			c.like_message = LikesHelper.getMessage(session["id"], c.id, c.type_id)
			# try:
			# 	likes = list(Likes.select().where((Likes.item_id == c.id) & (Likes.type_id == c.type_id)))
			# 	print likes, "list of likes"
			# 	c.likes = len(likes)
			# 	c.likers = likes
			# 	c.you_like = False
			# 	for like in likes:
			# 		if session['id'] == like.user.id:
			# 			c.you_like = True

			# 	print  c.likes, "Likes on Comments"
			# except:
			# 	print "No Likes on Comments", sys.exc_info()[0]
			c.is_liked_by_you = LikesHelper.was_item_liked_by_user(session["id"], c.id, c.type_id)



	request_names = getPendingRequests(user_id)
	print"Requests: ", request_names

	page_owner = UserHelper(user_id)
	page_owner_friends = page_owner.get_friends()

	try:
		Message.select().order_by(Message.id.desc())
		message = [m for m in Message.select().where(Message.recipient_id == user_id)]

	except:
		message = []

	session_user = UserHelper(session['id'])
	session_user_friends = session_user.get_friends()

	mutual_friends = []
	for session_friend in session_user_friends:
		for owner_friend in page_owner_friends:
			if session_friend.id == owner_friend.id:
				mutual_friends.append(session_friend)

	template_data = {
		"current_user": current_user,
		"request_names": request_names,
		"viewer": viewer,
		"message": message,
		"statuses": statuses,
		"page_owner_friends": page_owner_friends,
		"mutual_friends": mutual_friends,
		"friendsCount": len(page_owner_friends)
	}
	return render_template("profile2.html", **template_data)

@app.route('/')
def index():
	return render_template("index2.html")

@app.route('/login', methods = ['POST'])
def login():
	try:
		current_user = User.get(User.email == request.form['email'], User.password == request.form['password'])
		session['id'] = current_user.id
		# sesson['user'] = current_user
		session['name'] = str(current_user.f_Name + current_user.l_Name)
		return jsonify(url = '/profile/' + str(current_user.id))
	except:
		return 403


@app.route('/submit_registration', methods = ['POST'])
def submit_registration():
# check that no other user has same username/email
	try:
		person = User()
		for key, value in request.form.items():
			setattr(person, key, value)
		person.save()
		return jsonify(url = '/profile/' + str(person.id))
	except:
		return jsonify(error = "something went wrong with your registration")


@app.route('/home')
def home():
	return redirect(url_for('profile', user_id = session['id']))


@app.route('/editProfile/<user_id>')
def editProfile(user_id):
	if str(user_id) != str(session['id']):
		return redirect(url_for('index'))
	person = User.get(User.id == user_id)
	print "Session Id:", session['id']
	return render_template('editProfile.html', current_user = person, edit = True)

# TODO: using this??
@app.route('/fixedProfile/<user_id>', methods = ['POST'])
def fixedProfile(user_id):
	person = User.get(User.id == user_id)
	for key, value in request.form.items():
		setattr(person, key, value)
	person.save()
	return redirect(url_for('profile', user_id = person.id))


@app.route('/addFriend/<user_id>', methods = ['POST'])
def addFriend(user_id):
	Friendship.create(user_id = user_id, friend_user_id = session['id'])
	return redirect(request.referrer)

@app.route('/acceptRequest/<friend>', methods = ['POST'])
def acceptRequest(friend):
	friend_id = User.get(User.f_Name == friend)
	print 'Friend id:', friend_id, friend
	f  = Friendship.select().where((Friendship.user_id == session['id']) & (Friendship.friend_user_id == friend_id)).get()
	f.accepted = 1
	f.save()
	return redirect(request.referrer)

@app.route('/declineRequest/<friend>', methods = ['POST'])
def declineRequest(friend):
	friend_id = User.get(User.f_Name == friend)
	f  = Friendship.select().where((Friendship.user_id == session['id']) & (Friendship.friend_user_id == friend_id)).get()
	f.accepted = -1
	f.save()
	return redirect(request.referrer)

@app.route('/search',  methods = ['POST'])
def search():
	names = []
	for person in User.select():
		names.append(person.f_Name)
	if request.form['Search'] in names:
		try:
			person = User.get(User.f_Name == request.form['Search'])
			return redirect(url_for('profile', user_id = person.id))
		except:
			return redirect(request.referrer)
	else:
		return 'fails'

@app.route('/writeStatus', methods = ['POST'])
def writeStatus():
	s = Status.create(creater_id = session['id'], status = request.form['status'])
	s.save()
	return redirect(request.referrer)

@app.route('/like', methods = ['POST'])
def like():
	try:
		status = 0
		user_like = Likes.select().where((Likes.user == session['id']) & (Likes.item_id == request.form["itemId"]) & (Likes.type_id == request.form["typeId"])).get()
		user_like.delete_instance()
		user_like.save()

	except:
		status = 1
		like = Likes.create(user = session['id'], item_id = request.form["itemId"], type_id = request.form["typeId"])
		like.save()

	message = LikesHelper.getMessage(session["id"], request.form["itemId"], request.form["typeId"])

	return jsonify({'like': status, 'message': message}) #0 for unlike 1 for a like

@app.route('/comment', methods = ['POST'])
def comment():
	etype = request.form['type']
	if etype == "status":
		type_id = 0
	elif etype == "picture":
		type_id = 1
	c = Comments.create(user = session['id'], item_id = request.form['itemId'], type_id = type_id, comment = request.form['comment'])
	c.save()
	comment_macro = get_template_attribute('macros/comment.html', 'comment')
	html = comment_macro(c, session['id'])
	return jsonify(html = html)

@app.route('/sendMessage/<user_id>', methods = ['POST'])
def sendMessage(user_id):
	m = Message.create(sender_id = session['id'], recipient_id = user_id, message = request.form['message'])
	print "Request Referrer", request.referrer
	m.save()
	# return redirect(url_for('profile', user_id = user_id))
	return redirect(request.referrer)


@app.route('/upload_file', methods=['POST'])
def upload_file():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		pic = Picture.create(user = session['id'], filename = filename)
		pic.save()

		print "Request.form", request.form
		if int(request.form['isProfilePhoto']) == 1:
			print "It Works"
			p = User.select().where(User.id == session['id']).get()
			p.profile_photo = filename
			p.save()
			album = Album.get(Album.name == "Profile Pictures")
			row = Albums_Pictures.create(album = album.id, picture = pic.id)
			row.save()
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
	else:
		flash(u'Picture not allowed', 'error')
	return redirect(request.referrer)

@app.route('/getPictures/<user_id>')
def getPictures(user_id):
	pic_owner = User.get(User.id == user_id)
	current_user_pics = [pic.filename for pic in pic_owner.pictures]
	return render_template('pictures.html', pics = current_user_pics, p = pic_owner)

@app.route('/goToPicture/<image_name>')
def goToPicture(image_name):
	viewer = User.get(User.id == session['id'])
	pic_info = Picture.get(Picture.filename == image_name)
	pic_info.type_id = constants.types['picture'] 
	pic_info.comments = [c for c in Comments.select().where((pic_info.id == Comments.item_id) & (Comments.type_id == constants.types['picture'] ))]
	likers = []
	for like in Likes.select().where(Likes.item_id == pic_info.id & Likes.type_id == constants.types['picture']):
		person = User.select().where(User.id == like.user.id).get()
		likers.append(person.f_Name)
	pic_info.likers = likers
	print likers, "Pic Likers"
	pic_info.likes = len(likers)
	print(pic_info.comments, "Comments Not Working:")
	return render_template('picturePage2.html', pic_info = pic_info, viewer=viewer, current_user = pic_info.user)


@app.route('/createAlbum', methods=['POST'])
def createAlbum():
	a = Album.create(user_id = session['id'], name = request.form["name"])
	a.save()
	u = Users_Albums.create(user = session['id'], album = a.id)
	u.save()
	return redirect(request.referrer)

@app.route('/getAlbums/<user_id>')
def getAlbums(user_id):
	users_albums = [row.album for row in Users_Albums.select().where(Users_Albums.user == user_id)]

	return render_template("albumPage.html", albums = users_albums)

@app.route('/getPicturesFromAlbum/<album_id>')
def getPicturesFromAlbum(album_id):
	try:
		rows = list(Albums_Pictures.select().where(Albums_Pictures.album == album_id))
		album = rows[0].album
		print rows[0].picture.id, "first pic"
		albums_pictures = [row.picture for row in rows]
	except:
		albums_pictures = []
		# Still need the name of the album
		album = Album.get(Album.id == album_id)

	return render_template('albumsPictures.html', album_pics = albums_pictures, album = album)

@app.route('/updateAlbum/<album_id>', methods=['POST'])
def updateAlbum(album_id):
	print request.form['action'], "Test!"
	if request.form['action'] == "add":
		file = request.files["file"]
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			pic = Picture.create(user = session["id"], filename = filename)
			pic.save()
			row = Albums_Pictures.create(album = album_id, picture = pic.id)
			row.save()
			print "Adding pic number ", pic.id,  "to album ", album_id
		else:
			flash(u'Picture not allowed', 'error')
	elif request.form['action'] == "delete":
		print "Deleting image", request.form["picture_id"], "from Album ", album_id
		# Can't have duplicate picture id's so we don't need to specify the album id
		Albums_Pictures.delete().where(Albums_Pictures.picture == request.form["picture_id"]).execute()
		Picture.delete().where(Picture.id == request.form["picture_id"]).execute()

	return redirect(request.referrer)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('id', None)
    return redirect(url_for('index'))





app.secret_key = 'd;sifghas uifdsghf;usadluig f S@@#!@# 1235'

if __name__ == '__main__':
	# app is a Flask object that allows us to
	# start our web server with the above logic.

	# The debug=true setting allows any changes to this file
	# to force an automatic restart of the webserver.
    app.run(debug = True)