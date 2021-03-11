# -*- coding: utf-8 -*-

from ExercisePlayer import ExercisePlayer
from ExerciseStats import ExerciseStats
from Jokes.JokeGenerator import JokeGenerator
from RobotServices.AnimationPlayer import AnimationPlayer
from RobotServices.AutonomousLifeController import AutonomousLifeControllerModule
from RobotServices.Awareness import Awareness
from RobotServices.HeadTracking import HeadTracking
from RobotServices.Motion import Motion
from RobotServices.Notification import Notification
from RobotServices.TextToNorwegianSpeech import TextToNorwegianSpeech
from RobotServices.TextToSpeech import TextToSpeech
from TabletController import TabletController
from Weather.WeatherAnswers import WeatherAnswers
from Help.Help import Help

import webbrowser
import random

class PepperController(object):
    def __init__(self, session, language, ip):
        """
        init
        :param session: qi session
        :param language: synth language
        """
        self.session = session
        self.language = language
        self.location = "Tennfjord"
        self.ip = ip

        # Available services
        self.motion = Motion(session)
        self.tts = TextToSpeech(session)
        self.audioPlayer = session.service("ALAudioPlayer")
        self.ttsNOR = TextToNorwegianSpeech(self.audioPlayer)
        self.awareness = Awareness(session)
        self.notification = Notification(session)
        self.animation = AnimationPlayer(session)
        self.autonomousLifeController = AutonomousLifeControllerModule(session)
        self.headTracking = HeadTracking(session)
        self.alMotion = session.service("ALMotion")
        self.postures = session.service("ALRobotPosture")

        #self.exercisePlayer = ExercisePlayer("exercises/", self.alMotion, self.tts, self.postures)
        self.exercisePlayer = None
        self.exerciseStats = ExerciseStats()
        self.helper = Help()


        self.tabletController = TabletController(self.session)

        self.weatherAPI = WeatherAnswers(self.language)
        self.jokeGen = JokeGenerator(self.language, self.tts, self.ttsNOR)

        self.inExerciseMode = False
        self.inTransportMode = False
        self.inIdleMode = True
        self.inPause = False

        self.__control_awareness(True)
        self.__control_autonomous_abilities(True)

        if self.language == "Norwegian":
            self.ttsNOR.say("Jeg er klar!")
        else:
            self.tts.say("I am ready!!")

    def get_pause_status(self):
        return self.inPause

    def get_session(self):
        return self.session

    def changeMode(self, mode):
        if mode.lower() == "transport":
            self.inTransportMode = True
            self.inExerciseMode = False
            self.inIdleMode = False
        elif mode.lower() == "exercise":
            self.inTransportMode = False
            self.inExerciseMode = True
            self.inIdleMode = False
        elif mode.lower() == "idle":
            self.inTransportMode = False
            self.inExerciseMode = False
            self.inIdleMode = True
        else:
            self.inTransportMode = False
            self.inExerciseMode = False
            self.inIdleMode = True
    # -------- API for movement
    def go_to_normalized(self, x, y, angle):
        '''
        Drive robot
        :param x:
        :param y:
        :param angle:
        :return:
        '''
        self.motion.go_to_normalized(x=x, y=y, angle=angle)

    def stop_moving(self):
        self.go_to_normalized(x=0, y=0, angle=0)


    def play_animation(self, path):
        self.animation.play_animation(path)

    def get_animation_path(self, name):
        path = ""

        animationDict = {
            "WakeUp":  "animations/Stand/Waiting/WakeUp_1",
            "Wings":  "animations/Stand/Gestures/Wings_1",
            "Binoculars":  "animations/Stand/Waiting/Binoculars_1",
            "Sneeze":  "animations/Stand/Emotions/Neutral/Sneeze",
            "SpaceShuttle":  "animations/Stand/Waiting/SpaceShuttle_1",
            "HappyBirtday":  "animations/Stand/Waiting/HappyBirthday_1",
            "Drink":  "animations/Stand/Waiting/Drink_1",
            "Laugh":  "animations/Stand/Emotions/Positive/Laugh_3",
            "DriveCar":  "animations/Stand/Waiting/DriveCar_1",
            "TakePicture":  "animations/Stand/Waiting/TakePicture_1",
            "Fitness": "animations/Stand/Waiting/Fitness_1",
            "MysticalPower":"animations/Stand/Waiting/MysticalPower_1",
            "AirGuitar":"animations/Stand/Waiting/AirGuitar_1",
            "Knight":"animations/Stand/Waiting/Knight_1",
            "Bandmaster":"animations/Stand/Waiting/Bandmaster_1"}
        path = animationDict[name]

        return path

    # API for Speech
    def say(self, to_say):
        if self.language == "English":
            self.tts.say(to_say)
        elif self.language == "Norwegian":
            self.ttsNOR.say(to_say)

    def say_animated(self, to_say):
        self.tts.say_animated(to_say)

    # API for awareness and security
    def set_basic_awareness(self, state):
        self.awareness.set_basic_awareness(state)

    def set_collision_detection(self, state):
        self.motion.enable_collision_detection(state)

    def __passive(self, state):
        self.motion.enable_collision_detection(state)

    def __control_awareness(self, state):
        self.awareness.set_basic_awareness(state)


    def __control_autonomous_abilities(self, state):
        self.autonomousLifeController.set_all_autonomous_abilities(state, state, state, state)


    # --------- API TO Exercise Player --------- #
    def play_exercise(self, file, fov):
        self.__control_awareness(False)
        self.__control_autonomous_abilities(False)

        if self.inPause == True:
            self.resume_exercise()
        else:
            if self.exercisePlayer is None or self.exercisePlayer.stop == False:
                self.exercisePlayer = ExercisePlayer("exercises/", self.alMotion, self.tts, self.postures, file, self.language, self.ttsNOR, self.awareness, self.autonomousLifeController, fov)
                self.exercisePlayer.start()

        self.inPause = False

    def pause_exercise(self):
        if self.inPause == False:
            self.inPause = True
            self.exercisePlayer.pause_exercise()

    def resume_exercise(self):
        self.__control_awareness(False)
        self.__control_autonomous_abilities(False)

        self.exercisePlayer.resume_exercise()

    def stop_exercise(self):
        self.exercisePlayer.stop_exercise()

        self.__control_awareness(True)
        self.__control_autonomous_abilities(True)

    def give_feedback(self, feedback):
        try:
            self.exercisePlayer
            self.exercisePlayer.give_feedback(feedback)
        except NameError:
            self.say(feedback)
        except AttributeError:
            self.say(feedback)

    def get_exercise_stats(self, exercise_number):
        return self.exerciseStats.get_exercise_stats(exercise_number)

    def update_exercise_stats(self, exercise_number):
        self.exerciseStats.update_exercise_stats(exercise_number)

    # --------- API To Tablet --------- #
    def stop_server(self):
        self.tabletController.stop_server()

    # --------- API for Weather --------- #
    def get_todays_weather(self):
        forecast = self.weatherAPI.get_current_weather_sentence(self.language, self.location)
        self.say(forecast)

    def get_tomorrows_forecast(self):
        forecast = self.weatherAPI.get_forecast_weather_sentence(self.language, self.location)
        self.say(forecast)

    def get_weather_forecast(self, date):
        forecast = self.weatherAPI.get_forecast_weather_sentence(self.language, self.location, date=date)
        self.say(forecast)


    # --------- API To Jokes --------- #
    def get_joke(self):
        self.jokeGen.get_joke()
        laugh = random.randint(0, 2)
        if laugh == 0:
            self.play_animation(self.get_animation_path("Laugh"))
        elif laugh == 1:
            self.play_animation("animations/Stand/Emotions/Positive/Laugh_1")
        else:
            self.play_animation("animations/Stand/Emotions/Positive/Laugh_2")


    # -------- API for Poses ---------
    def go_to_standard_pose(self):
        self.postures.goToPosture("StandInit", 1.0)

    #
    def get_language(self):
        return self.language

    # ------- API for help ------
    def get_help(self):
        self.helper.open_manual()

    # ADJUST SOUND
    def adjust_sound(self):
        print(self.ip)
        webbrowser.open("http://"+str(self.ip)+"/#/menu/myrobot")

    def changeSpeechRate(self, speechRate):
        self.ttsNOR.changeRate(speechRate)

    def getPreviousSpeechRate(self):
        return self.ttsNOR.get_previous_speech_rate()