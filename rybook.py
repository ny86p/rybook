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

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in  app.config['ALLOWED_EXTENSIONS']

@app.route('/redesign/<user_id>')
def redesign(user_id):
	viewer = Person.select().where(Person.id == session['id']).get()
	# Grab current_users info
	# current_user = page owner, 
	current_user = Person.select().where(Person.id == user_id).get()
	# check if the person viewing page is the owner
	current_user.owner = str(user_id) == str(session['id'])

	status= getStatuses(user_id)
	for s in status:
		if s.date_created:
			s.date_created = datetime.strftime(s.date_created, '%m/%d/%Y %I:%M%p')

	request_names = getPendingRequests(user_id)
	print"Requests: ", request_names

	try:
		Message.select().order_by(Message.id.desc())
		message = [m for m in Message.select().where(Message.recipient_id == user_id)]

	except:
		message = []

	return render_template("profile2.html",current_user = current_user, request_names = request_names, viewer = viewer, message = message, status = status)

@app.route('/')
def index():
	return render_template("index2.html")

@app.route('/login', methods = ['POST'])
def login():

	current_user = Person.get(Person.email == request.form['email'], Person.password == request.form['password'])
		# return current_user.email
	session['id'] = current_user.id
	return redirect(url_for("redesign", user_id = current_user.id))
	# except:
	# 	return render_template("index.html")
		# current_user.active == True
	# current_user.save()
	# Try Except when checking information

@app.route('/register')
def register():
	return render_template("registration.html")

@app.route('/submit_registration', methods = ['POST'])
def submit_registration():
# check that no other user has same username/email
	person = Person()
	# person.email = request.form['email']
	# person.password = request.form['password']
	for key, value in request.form.items():
		# items.append(key)
		setattr(person, key, value)
	print "email:" , person.email
	# print "Person Email:" + person.email
	person.save()
	return redirect(url_for('index'))

@app.route('/home')
def home():
	return redirect(url_for('redesign', user_id = session['id']))

@app.route('/profile/<user_id>')
def profile(user_id):
	# print 'Pending Requests:', getPendingRequests(user_id)

	current_user = Person.select().where(Person.id == user_id).get()
	current_user.owner = str(user_id) == str(session['id'])
	likers = []
	commenters = []

	# get statuses for user
	status = getStatuses(user_id)
	for s in status:
		try:
			likes = Likes.select().where(Likes.item_id == s.id)
			for like in likes:
				person = Person.select().where(Person.id == like.user_id).get()
				likers.append(person.f_Name)
				s.likers = likers
				s.likes = likes.count()
				print 'in'

		except:
			print "No Likes"
		comments = Comments.select().where(Comments.item_id == s.id)
		for c in comments:
			person = Person.select().where(Person.id == c.user_id).get()
			commenters.append(person.f_Name)

		# Comments.select().where(Comments.item_id == s.id)
		# .aggregate(fn.Count(Likes.user_id))
		s.comments = ([c.comment for c in Comments.select().where(Comments.item_id == s.id)], commenters)

	# get pending requests for user, only shown is session id = user id
	request_names = getPendingRequests(user_id)

	# get Friends
	friends = getReqFriendships(user_id)
	friends.extend(getAcceptedFrienships(user_id))

	# message = []
	# for m in Message.select().where(Message.recipient_id == user_id):
	# 	message.append(m)
	try:
		Message.select().order_by(Message.id.desc())
		message = [m for m in Message.select().where(Message.recipient_id == user_id)]

	except:
		message = []



	return render_template('profile.html', current_user = current_user, request_names = request_names, friends = friends, logged_in = int(session['id']),status = status, message = message, likers = likers)

@app.route('/editProfile/<user_id>')
def editProfile(user_id):
	if str(user_id) != str(session['id']):
		return redirect(url_for('index'))
	person = Person.get(Person.id == user_id)
	print "Session Id:", session['id']
	return render_template('editProfile.html', current_user = person, edit = True)


@app.route('/fixedProfile/<user_id>', methods = ['POST'])
def fixedProfile(user_id):
	person = Person.get(Person.id == user_id)
	for key, value in request.form.items():
		setattr(person, key, value)
	person.save()
	return redirect(url_for('profile', user_id = person.id))
# Basically like registration


@app.route('/addFriend/<user_id>', methods = ['POST'])
def addFriend(user_id):
	Friendship.create(user_id = user_id, friend_user_id = session['id'])
	return redirect(request.referrer)

@app.route('/acceptRequest/<friend>', methods = ['POST'])
def acceptRequest(friend):
	friend_id = Person.get(Person.f_Name == friend)
	print 'Friend id:', friend_id, friend
	f  = Friendship.select().where((Friendship.user_id == session['id']) & (Friendship.friend_user_id == friend_id)).get()
	f.accepted = 1
	f.save()
	return redirect(request.referrer)

@app.route('/declineRequest/<friend>', methods = ['POST'])
def declineRequest(friend):
	friend_id = Person.get(Person.f_Name == friend)
	f  = Friendship.select().where((Friendship.user_id == session['id']) & (Friendship.friend_user_id == friend_id)).get()
	f.accepted = -1
	f.save()
	return redirect(request.referrer)

@app.route('/search',  methods = ['POST'])
def search():
	names = []
	for person in Person.select():
		names.append(person.f_Name)
	if request.form['Search'] in names:
		try:
			person = Person.get(Person.f_Name == request.form['Search'])
			return redirect(url_for('redesign', user_id = person.id))
		except:
			return redirect(request.referrer)
	else:
		return 'fails'

@app.route('/writeStatus', methods = ['POST'])
def writeStatus():
	s = Status.create(creater_id = session['id'], status = request.form['status'])
	s.save()
	return redirect(request.referrer)

@app.route('/likeStatus/<s_id>', methods = ['POST'])
def likeStatus(s_id):
	current_status = Status.get(Status.id == s_id)
	# current_status.likes.append(session['id'])
	try:
		like = Likes.select().where((Likes.user_id == session['id']) & (Likes.item_id == s_id)).get()
		like.delete_instance()
		like.save()
	except:
		like = Likes.create(user_id = session['id'], item_id = s_id)
		like.save()
	return redirect(request.referrer)

@app.route('/comment/<item_id>', methods = ['POST'])
def comment(item_id):
	print item_id, "ID", "Request", request.form
	etype = request.form['type']
	print etype, "Type id:"
	if etype == "status":
		type_id = 0
	elif etype == "picture":
		type_id = 1
	comment = Comments.create(user_id = session['id'], item_id = item_id, type_id = type_id, comment = request.form['comment'])
	comment.save()
	return redirect(request.referrer)


@app.route('/sendMessage/<user_id>', methods = ['POST'])
def sendMessage(user_id):
	m = Message.create(sender_id = session['id'], recipient_id = user_id, message = request.form['message'])
	print "Request Referrer", request.referrer
	m.save()
	# return redirect(url_for('profile', user_id = user_id))
	return redirect(request.referrer)

# @app.route('/deleteMessage')
# def deleteMessage():


# @app.route('/verify')
# def verify():
# 	return render_template('activate.html')
	# render the template- once this template is visited, activate user
	# and have type in activation code (**maybe) or just click button that says activate

# @app.route('/activate')
# def activate:
# 	for person in Person.select():
# 			current_user = person


@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pic = Picture.create(user_id = session['id'], filename = filename)
        pic.save()
        print "Request.form", request.form
        if int(request.form['isProfilePhoto']) == 1:
        	print "It Works"
	    	p = Person.select().where(Person.id == session['id']).get()
	    	p.profile_photo = filename
	    	p.save()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect(request.referrer)

@app.route('/getPictures/<user_id>')
def getPictures(user_id):
	# pictures = Picture.get(Picture.user_id == user_id)
	currentUserPics = [pic.filename for pic in Picture.select().where(Picture.user_id == user_id)]
	# if type(pictures) != list:
		# pictures = [pictures]
	# currentUserPics = [pic.filename for pic in pictures]
	# import os
	# # getting all filenames in the images directory
	# filenames = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
	# # getting all files that belong to the user
	# currentUserPics = [f for f in filenames if f.split('_')[0] == str(user_id)]
	print "Current Pics", currentUserPics
	return render_template('pictures.html', pics = currentUserPics)

@app.route('/goToPicture/<image_name>')
def goToPicture(image_name):
	pic_info = Picture.get(Picture.filename == image_name)
	comments = [c for c in Comments.select().where((pic_info.id == Comments.item_id) & (Comments.type_id == 1))]
	print(comments, "Comments Not Working:")

	return render_template('picturePage.html', pic_info = pic_info, comments = comments)

# @app.route('/pictures/view')
# def viewPictures():


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