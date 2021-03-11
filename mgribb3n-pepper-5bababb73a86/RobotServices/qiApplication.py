"""
Class to establish a Qi (Robot) application.
From this application, sessions can be created to proxy services in the NAOqi API.
"""

import qi
import sys


class QiApplication:
    def __init__(self, application_name, ip_address, port):
        """ Initialise variables for connection """
        self.ip_address = ip_address
        self.port = port
        self.application_name = application_name

    def connect(self):
        """ Establish a Qi-application and connect to robot """
        try:
            connection_url = "tcp://" + self.ip_address + ":" + str(self.port)
            app = qi.Application([self.application_name, "--qi-url=" + connection_url])
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + self.ip_address + "\" on port " + str(self.port) + ".\n"
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)
        return app




