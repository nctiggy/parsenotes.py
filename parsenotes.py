import sys
import smtplib
from email.mime.text import MIMEText
import webbrowser
import urllib
import re
 
maildrop = ''
arrNotes = []
arrTasks = []
arrMeetings = []
actual_tasks = []
emailUser = ''
emailPassword = ''
 
def emailTask(subject):
	msg = MIMEText('')
	msg['Subject'] = subject
	msg['From'] = emailUser
	msg['To'] = maildrop
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.ehlo()
	server.login(emailUser,emailPassword)
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	server.quit()
 
text = sys.argv[1]
arrText = text.split('\n')
#subject = re.sub('[\[\]]','',arrText[0])
full_note = arrText[0].split(' ')[0] + '\n'
full_note += '## ' + arrText[0] + '\n'
# group all like items together
for line in arrText:
	matchNote = re.escape("[note_item]")
	matchTask = re.escape("[task_item]")
	matchMeeting = re.escape("[meeting_item]")
	if re.match(matchNote,line):
		arrNotes.append(line.split(']')[1].strip() + '\n')
	elif re.match(matchTask,line):
		arrTasks.append('-' + line.split(']')[1] + '\n')
		emailTask(line.split(']')[1].strip())
	elif re.match(matchMeeting,line):
		arrMeetings.append('-' + line.split(']')[1] + '\n')
		emailTask(line.split(']')[1].strip())
 
full_note += ' '.join(arrNotes)
full_note += ' '.join(arrTasks)
full_note += ' '.join(arrMeetings)
 
webbrowser.open("drafts://x-callback-url/create?text=" + urllib.quote(full_note) + "&action=notes_to_ever&afterSuccess=Delete&x-success=launch://")