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
import os
from comments import *
from werkzeug.utils import secure_filename
import constants
import sys

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


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

	status= getStatuses(user_id)
	commenters = []
	for s in status:
		s.type_id = constants.types['status']
		if s.date_created:
			s.date_created = datetime.strftime(s.date_created, '%m/%d/%Y %I:%M%p')
		try:
			likes = Likes.select().where((Likes.item_id == s.id) & (Likes.type_id == s.type_id))
			print s.id, "Status id"
			# print len(likes), "Number of Likes"
			# likes =  User.likes.select().where(Likes)
			likers= []
			for like in likes:
				person = User.select().where(User.id == like.user.id).get()
				likers.append(person.f_Name)
				print " IN loop"
			s.likes = len(likers)
			s.likers = likers
			print s.likes, "Likes on status", likers
		except:
		 	print "No Likes", sys.exc_info()[0]
		Comments.select().order_by(Comments.date_created.desc)
		s.comments = Comments.select().where(Comments.item_id == s.id)
		for c in s.comments:
			c.type_id = constants.types['comment']


	request_names = getPendingRequests(user_id)
	print"Requests: ", request_names

	friends = getAcceptedFrienships(user_id)
	friends.extend(getReqFriendships(user_id))
	print friends, "friends"
	try:
		Message.select().order_by(Message.id.desc())
		message = [m for m in Message.select().where(Message.recipient_id == user_id)]

	except:
		message = []

	viewerFriends = getAcceptedFrienships(session['id'])
	viewerFriends.extend(getReqFriendships(session['id']))
	mutualFriends = [f for f in viewerFriends if f in friends]
	return render_template("profile2.html",current_user = current_user, request_names = request_names, viewer = viewer, message = message, status = status,friends=friends, mutualFriends = mutualFriends)

@app.route('/')
def index():
	return render_template("index2.html")

@app.route('/login', methods = ['POST'])
def login():
	try:
		current_user = User.get(User.email == request.form['email'], User.password == request.form['password'])
		session['id'] = current_user.id
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
	print request.form["itemId"], "Requst form"
	current_status = Status.get(Status.id == request.form["itemId"])
	try:
		status = 0
		like = Likes.select().where((Likes.user == session['id']) & (Likes.item_id == request.form["itemId"]) & (Likes.type_id == request.form["typeId"])).get()
		like.delete_instance()
		like.save()
	except:
		status = 1
		like = Likes.create(user = session['id'], item_id = request.form["itemId"], type_id = request.form["typeId"])
		like.save()
	return jsonify(like = status) #0 for unlike 1 for a like

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
	html = comment_macro(c)
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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
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