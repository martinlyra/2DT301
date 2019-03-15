import smtplib
import logging
import time
from xml.etree import ElementTree
from MoreThreading import Threaded


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
        self.mail_password = userinfo.find('password').get('value')

        gateway = config_tree.find('gateway')

        self.gateway_address = gateway.get('address')
        self.gateway_port = gateway.get('port')

    @Threaded
    def send_mail(self):
        sent_from = self.mail_user
        to = [self.mail_user]
        subject = "Home alarm"
        body = "Your home alarm has detected an intrustion"
                
        message_text = """
                From: %s
                To: %s
                Subject: %s

                %s
                """
        message_text = message_text % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL(self.gateway_address, self.gateway_port)
            logging.debug("Logging in...")
            server.login(self.mail_user, self.mail_password)
            logging.debug("Sending mail...")
            server.sendmail(sent_from, to, message_text)
            server.quit()

            logging.debug("Email sent!")
        except Exception as ex:
            logging.debug("Something went wrong;",ex)

