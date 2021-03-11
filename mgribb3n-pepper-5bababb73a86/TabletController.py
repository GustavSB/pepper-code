import qi
from TabletControl.LEDController import LEDController

from RobotServices.AutonomousLifeController import AutonomousLifeControllerModule
from TabletControl.Tablet import Tablet
from TabletControl.httpserver import RootedHTTPServer, ServerThread

class TabletController(object):
    def __init__(self, session):
        self.session = session
        self.tablet = Tablet(self.session)
        self.hsv = RootedHTTPServer()
        self.svt = ServerThread(self.hsv)
        self.svt.start()
        self.LEDController = LEDController(self.session)

        self.set_initial_background_image()

    def set_initial_background_image(self):
        self.tablet.set_background_color()
        self.tablet.show_image(self.hsv.get_root_address() + "NTNUlogobred.png")
        #self.set_color("EyesGreen")
        #self.set_color("ChestGreen")

    def set_background_image(self, image_path):
        self.tablet.set_background_color()
        self.tablet.show_image(self.hsv.get_root_address() + image_path)

    def set_color(self, color):
        self.LEDController.set_group_on(color)

    def stop_server(self):
        self.svt.stop()
