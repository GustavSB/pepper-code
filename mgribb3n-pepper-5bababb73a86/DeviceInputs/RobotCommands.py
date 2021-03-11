"""
The responsibility of this class is to communicate commands and such to the Robot.

Establish connections to the different services on the robot, and perform commands that will be performed
according to the argument (input from user).
"""

from RobotServices.Motion import Motion
from RobotServices.Speech import Speech
from RobotServices.AnimationPlayer import AnimationPlayer
from RobotServices.Notification import Notification
from RobotServices.Awareness import Awareness


class RobotCommands:
    def __init__(self, session, pepperController):
        #self.motion = Motion(session)
        #self.speech = Speech(session)
        self.awareness = Awareness(session)
        self.notification = Notification(session)
        #self.animation = AnimationPlayer(session)
        self.speed_limit = 0.6
        self.pepperController = pepperController

    # Motion commands
    def __forward(self):
        self.pepperController.go_to_normalized(x=self.speed_limit, y=0, angle=0)
        #print("Forward")

    def __backward(self):
        self.pepperController.go_to_normalized(x=-self.speed_limit, y=0, angle=0)
        #print("Backward")

    def __left(self):
        self.pepperController.go_to_normalized(x=0, y=0, angle=self.speed_limit)
        #print("Left")

    def __right(self):
        self.pepperController.go_to_normalized(x=0, y=0, angle=-self.speed_limit)
        #print("Right")

    def __stop(self):
        self.pepperController.go_to_normalized(x=0, y=0, angle=0)

    def stop(self):
        print("Trying to stop!")
        self.__stop()

    # Animation commands
    def __greet(self):
        self.pepperController.play_animation("animations/Stand/Gestures/Hey_1")

    # Voice commands
    def __say_hello(self):
        self.pepperController.say("Hallo. Her kommer jeg!")

    # General commands
    def __status(self):
        pass

    def __static(self):
        self.pepperController.set_basic_awareness(False)

    def __dynamic(self):
        self.pepperController.set_basic_awareness(True)

    def __killer(self):
        self.pepperController.enable_collision_detection(False)

    def __passive(self):
        self.pepperController.enable_collision_detection(True)

    def do_command(self, argument):
        switcher = {
            0:  self.__stop,
            1:  self.__forward,
            2:  self.__backward,
            3:  self.__left,
            4:  self.__right,
            5:  self.__greet,
            6:  self.__say_hello,
            7:  self.__static,
            8:  self.__dynamic,
            9:  None,
            10: None,
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument, lambda: "no valid input")
        # Execute the function
        return func()




























