from PepperController import PepperController
from GUI import GUI

import urllib2


class Connector(object):
    def __init__(self, session, language, ip):
        """
        init
        :param session: qi session
        :param language: synth language
        """
        self.session = session
        self.language = language
        self.internetStatus = self.check_internet_connection()
        self.ip = ip

        if self.internetStatus == False:
            self.language = "English"

        print("Network connection is " + str(self.internetStatus))
        print("Chosen language is " + self.language)

        # Start Pepper Controller
        self.controller = PepperController(self.session, self.language, self.ip)
        # Start GUI
        self.GUI = GUI(self.controller)


    def check_internet_connection(self):
        try:
            urllib2.urlopen('http://216.58.192.142', timeout=4)
            return True
        except urllib2.URLError as err:
            return False