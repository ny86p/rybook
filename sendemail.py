import smtplib
 
def send(recipient):
	gmail_user = 'mkyong2002@gmail.com'
	gmail_pwd = 'yourpassword'
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + recipient + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
	print header
	msg = header + '\n this is test msg from mkyong.com \n\n'
	smtpserver.sendmail(gmail_user, recipient, msg)
	print 'done!'
	smtpserver.close()
