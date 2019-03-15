import smtplib
from xml.etree import ElementTree


class SmtpMessanger(object):
	mail_user = ""
	mail_password = ""
	gateway_address = ""
	gateway_port = ""

	def __init__(self, config_tree : ElementTree):
                self.configure(config_tree)

	def configure(self, config_tree : ElementTree):
                userinfo = config_tree.find('credentials')

                self.mail_user = userinfo.find('username').get('value')
                self.password = userinfo.find('password').get('value')

                gateway = config_tree.find('gateway')

                self.gateway_address = gateway.get('address')
                self.gateway_port = gateway.get('port')

	def send_mail(self):
                sent_from = self.mail_user
                to = self.mail_user
                subject = "Home alarm"
                body = "Your home alarm has detected an intrustion"
                
		message_text = """
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

		try:
                        server = smtplib.SMTP_SSL(self.gateway_address, self.gateway_port)
                        server.ehlo()
                        server.login(gmail_user, gmail_password)
                        server.sendmail(sent_from, to, email_text)
                        server.close()

                        print("Email sent!")
                except Exception as ex:
                        print("Something went wrong;",ex)
		
