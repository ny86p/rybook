from datetime import datetime
import os
import hashlib

class PictureHelper():

	@staticmethod
	def generate_unique_filename(user_id, filename):
		ext = os.path.splitext(filename)[1]
		time_stamp = datetime.now().strftime("%I:%M:%H:%M:%S%p on %B %d, %Y")
		unique_filename = hashlib.md5(str(user_id) + time_stamp).hexdigest()
		return unique_filename + ext