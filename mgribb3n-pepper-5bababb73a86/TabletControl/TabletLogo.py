# author = 'Eirik Gromholt Homlong'
import qi
from LEDController import LEDController

from RobotServices.AutonomousLifeController import AutonomousLifeControllerModule
from Tablet import Tablet
from httpserver import RootedHTTPServer, ServerThread

#  NaoQi / qi : init qi session and ALMemory service
session1 = qi.Session()
session1.connect("192.1.12.17:9559")



# Tablet : Sets up and connect the tablet.
tbl1 = Tablet(session1)
led1 = LEDController(session1)
aut1 = AutonomousLifeControllerModule(session1)


hsv = RootedHTTPServer()
svt = ServerThread(hsv)
svt.start()

tbl1.set_background_color()
tbl1.show_image(hsv.get_root_address() + "newtonlogo.jpg")

