#!python 3.6.5
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sys ,os
# reload(sys)
# sys.setdefaultencoding('utf-8')

class SendMail():
    def __init__(self, userid, userpw, smtp_server = 'gmail'):
        assert isinstance(userid, str)
        assert isinstance(userpw, str)
        assert isinstance(smtp_server, (list,str))

        default_smpt_server = {}
        default_smpt_server['gmail']     = ['smtp.gmail.com',587]
        default_smpt_server['yahoo']     = ['smtp.mail.yahoo.com',25]
        default_smpt_server['microsoft'] = ['smtp.live.com',587]

        self.mail_user = userid
        self.mail_pw = userpw
        self.smtp_server_conf = default_smpt_server[smtp_server]
        self.login()
        
    def login(self):
        self.mailServer = smtplib.SMTP(*self.smtp_server_conf) #Mail Server
        self.mailServer.ehlo()
        self.mailServer.starttls()
        self.mailServer.ehlo()
        self.mailServer.login(self.mail_user, self.mail_pw)
        print('login successfully')

    def sendEmail(self, subject, msg, mail_target, cc_id=[], attached = [], mail_from = 'Auto Mail'):
        assert isinstance(subject, str)
        assert isinstance(msg, str)
        assert isinstance(attached, list)
        assert isinstance(mail_from, str)
        assert isinstance(mail_target, list)
        assert isinstance(cc_id, list)

        isAuth = True

        ### Mail configration
        mail_Message = MIMEMultipart()
        mail_Message['From'] = mail_from
        mail_Message['Subject'] = subject

        print ("Preparing mail configaration...")
        
        mail_Message['cc'] = ", ".join(cc_id)
        mail_Message['To'] = ", ".join(mail_target)

        print ("Preparing mail content...")
        # content is read HTML language
        mail_Message.attach(MIMEText(msg, 'html', 'utf-8'))
        for filepath in attached:
            filename, file_extension = os.path.splitext(filepath)
            with open(filepath, 'rb') as fp:
                if file_extension in ['.png']:
                    mailFile = MIMEImage(fp.read())
                    mailFile["Content-Disposition"] = 'attachment; filename="%s"' %(os.path.basename(filepath))
                    mailFile.add_header('Content-ID', '<image1>')
                elif file_extension in ['.csv', '.xlsx', '.txt']:
                    mailFile = MIMEText(fp.read(), 'base64', 'utf-8')
                    mailFile["Content-Type"] = 'application/octet-stream'
                    mailFile["Content-Disposition"] = 'attachment; filename="%s"' %(os.path.basename(filepath))
                else:
                    mailFile = MIMEText(fp.read(), 'base64', 'utf-8')
                    mailFile["Content-Type"] = 'application/octet-stream'
                    mailFile["Content-Disposition"] = 'attachment; filename="%s"' %(os.path.basename(filepath))
            mail_Message.attach(mailFile)

        print ("Loging into AUTH Mail server...")
        
        print ("Sending mail...")

        self.mailServer.sendmail(self.mail_user, cc_id+mail_target, mail_Message.as_string())
        return True

    def close(self):
        self.mailServer.close()
        print ("logout")
