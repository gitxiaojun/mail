#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import json
import logging
import logging.handlers
import  sys
###import end
# configure log
LOG_FILE = "/var/log/gitlab-post.log"
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=20 * 1024 * 1024, backupCount=10)
fmt = "[%(asctime)s - %(message)s]"
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
# config_json
app = Flask(__name__)
@app.route('/', methods=['POST'])
def send_mails():
	data = json.loads(request.data)
	#if data['ref'] in ("refs/heads/develop","refs/heads/deploy","refs/heads/staging","refs/heads/master"):
	if data['ref'] in ("refs/heads/develop","refs/heads/deploy",'refs/heads/2016.4.21'):
		report_txt ='''<table align="center" border="1" cellspacing="0" bordercolor="#000000" width="800">
				<tr bgcolor="#3399CC" height="40">
	            <th><h2 style="color:#FFFF33">Type</h2></th>
	            <th><h2 style="color:#FFFF33">Project_Name</h2></th>
	            <th><h2 style="color:#FFFF33">User</h2></th>
	            <th><h2 style="color:#FFFF33">message</h2></th>
	            <th><h2 style="color:#FFFF33">Branch</h2></th>
	            <th><h2 style="color:#FFFF33">Commit_Id</h2></th>
	            <th><h2 style="color:#FFFF33">Modify_Files</h2></th>
	            <th><h2 style="color:#FFFF33">Removed_Files</h2></th>
	            <th><h2 style="color:#FFFF33">Added_Files</h2></th>
	            </tr>'''
		json.dump(data, open('/var/log/gitlab-post.log', 'w'))
		commits_count = len(data['commits'])
		movie_kind = data['object_kind']
		movie_project = data['project']['name']
		movie_branch = data['ref']
		if commits_count != 0 :
			for i in range(0,commits_count):
				movie_user_name = data['commits'][i]['author']['name']
				movie_commit_id = data['commits'][i]['id']
				movie_modify_file = data['commits'][i]['modified']
				movie_removed_file = data['commits'][i]['removed']
				movie_added_file = data['commits'][i]['added']
				movie_message = data['commits'][i]['message']
				report_txt += '''<tr height="40">
		            <th>%s</h2></th>
		            <th>%s</h2></th>
		            <th>%s</h2></th>
		            <th>%s</h2></th>
		            <th>%s</h2></th>
		            <th>%s</h2></th>
		            <th>%s</h2></th>
		            <th>%s</h2></th>
		            <th>%s</h2></th>
		             </tr>
		            ''' % (	movie_kind, movie_project,movie_user_name,movie_message,movie_branch,movie_commit_id, movie_modify_file,movie_removed_file,movie_added_file)
			report_txt += ''' </table>'''
			# sender_config
			msg = MIMEText('%s' % report_txt, 'html', 'utf-8')
			sender = 'test@bangwz.com'
			receiver = ['1@1.com','2@2.com']
			subject = '''NEW %s at %s ''' % (movie_kind, movie_project)
			smtpserver = 'smtp.ym.163.com'
			username = 'test@bangwz.com'
			password = 'test'
			# send_mail_config
			msg['Subject'] = subject
			msg['From'] = 'test@bangwz.com'
			smtp = smtplib.SMTP()
			smtp.connect('smtp.ym.163.com')
			smtp.login(username, password)
			smtp.sendmail(sender, receiver, msg.as_string())
			smtp.quit()
	return "ok"
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9527, debug=True)
