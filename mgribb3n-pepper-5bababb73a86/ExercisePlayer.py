# -*- coding: utf-8 -*-

import pandas as pd
from os import listdir
import almath
import math
import time
import numpy as np
from os import path as osPath  # Import path
import random

from threading import Thread
from threading import Condition
from threading import Lock
"""
CSV Format for exercises:

Columns:
Number, HeadYaw, HeadPitch, LShoulderPitch, LShoulderRoll, LElbowYaw, LElbowRoll, LWristYaw,
                 HipRoll, HipPitch, KneePitch, RShoulderPitch, RShoulderRoll, RElbowYaw, RElbowRoll, RWristYaw,
                 Speed, LeftHand, RightHand, X-movement, Y-movement, Angle, sentence

Number: Just to have a reference on where in the exercise you are
Joints (until left and right hand): Angle in degrees
Speed: Speed to move joints (between 0.0 and 1.0)
Left and Right Hand: 0 Normal, 1 Open, 2 Close
X-movement: Meters to move
Y-movement: Meters to move
Angle: Angle to move
Sentence: Sentence to say

Might on a later occasion also put in delay (delay between movements), interpolation-interpolate joints to certain
 position (0,1), mood and body language for speaking.
"""

class ExercisePlayer(Thread):
    def __init__(self, folder, alMotion, tts, posture, file, language, ttsNOR, awareness, autonomousLifeController, fov, threadID=None, name="Temp. Exercise Thread"):
        # Thread args
        super(ExercisePlayer, self).__init__()
        self.threadID = threadID
        self.name = name
        self.paused = False
        self.running = True
        self.pause_cond = Condition(Lock())
        self.args = []
        self.kwargs = {}

        # Getting current filepath (used for relative path)...
        self.filepath = osPath.dirname(osPath.realpath(__file__))
        self.exercise_folder = self.filepath+"/"+folder
        self.file = file

        # Rotation variablesutslag
        self.fov = fov
        self.max_angle = round(fov/2)
        self.current_angle = 0
        self.previous_rotation = 0

        self.csv_cols = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw',
                 'HipRoll', 'HipPitch', 'KneePitch', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw',
                 'Speed','delay', 'LeftHand', 'RightHand', 'X-movement', 'Y-movement', 'Angle', 'sentence', 'rotate']

        # Executing on robot services:
        self.alMotion = alMotion
        self.posture = posture
        self.tts = tts
        self.ttsNOR = ttsNOR
        self.language = language
        self.awareness = awareness
        self.autonomousLifeController = autonomousLifeController

    def run(self):
        path = self.exercise_folder + "" + self.file
        tmp = pd.DataFrame.from_csv(path)

        print("Playing exercise")

        while self.stop:
            with self.pause_cond:
                for index, row in tmp.iterrows():
                    if not self.stop:
                        print("Stopping")
                        break;

                    #print(index)
                    joints = self.csv_cols[0:15]
                    joints_movement = row[0:15]
                    speed = row[15]
                    delay = row[16]
                    x = row[19]
                    y = row[20]
                    angle = row[21]
                    sentence = row[22]
                    rotate = row[23]

                    if np.isnan(x):
                        x = 0
                    if np.isnan(y):
                        y = 0
                    if np.isnan(angle):
                        angle = 0

                    if type(sentence) == str:
                        self.say(sentence)

                    print(self.alMotion.getStiffnesses("Body"))

                    self.move_joint(joints,joints_movement,speed)
                    time.sleep(delay)

                    stiffnesses = 1.0
                    self.alMotion.setStiffnesses("Body", stiffnesses)

                    #print(self.alMotion.getMoveArmsEnabled("Arms"))

                    self.alMotion.setMoveArmsEnabled(False, False)
                    if rotate == 1:
                        self.rotate()
                    self.alMotion.setMoveArmsEnabled(True, True)

                    while self.paused:
                        self.pause_cond.wait()  # Wait to not use resources
                self.stop = False

    def pause_exercise(self):
        """pauses the loop"""
        self.paused = True
        self.pause_cond.acquire()

    def stop_exercise(self):
        """stops the loop and stops the run function which kills the thread"""
        self.stop = False

    def resume_exercise(self):
        """resumes the loop"""
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()

    def give_feedback(self, feedback):
        self.pause_exercise()
        self.say(feedback)
        time.sleep(1)
        self.resume_exercise()

    def stop(self):
        """stops the loop and stops the run function which kills the thread"""
        self.stop = False
        self.pause_cond.notify()
        if self.paused:
            self.pause_cond.release()

        self.__control_awareness(True)
        self.__control_autonomous_abilities(True)

    def rotate(self):
        if self.fov == 0:
            theta = 0
        else:
            rotation = self.max_angle / 2 - 0.5
            rnd = random.random()
            if rnd <= 0.99:
                #self.alMotion.setIdlePostureEnabled("Body", False)
                if self.previous_rotation == 0:
                    to_rotate = rotation
                elif self.previous_rotation > 0:
                    if self.current_angle+self.previous_rotation >= self.max_angle:
                        to_rotate = -self.previous_rotation
                    else:
                        to_rotate = self.previous_rotation
                elif self.previous_rotation < 0:
                    if self.current_angle + self.previous_rotation <= -self.max_angle:
                        to_rotate = -self.previous_rotation
                    else:
                        to_rotate = self.previous_rotation


                self.previous_rotation = to_rotate
                self.current_angle += to_rotate
                theta = to_rotate * almath.TO_RAD

                self.alMotion.moveTo(0, 0, theta)
                #self.alMotion.setIdlePostureEnabled("Body", True)
                #print("Current angle: " + str(self.current_angle) + " Max angle: " + str(self.max_angle) + " To rotate: " + str(to_rotate))


    def move(self, x,y,angles):
        """

        :return:
        """


        moveToX = float(x)
        moveToY = float(y)
        moveDir = float(angles)
        print(moveDir)
        theta = moveDir * almath.TO_RAD

        self.alMotion.moveTo(moveToX, moveToY, theta)


    def move_joint(self, joints_to_move, to_angles, speed=0.1):
        """

        :param joints_to_move:
        :param to_angles:
        :param speed:
        :return:
        """
        for j in range(0, len(joints_to_move)):
            try:
                angles = to_angles[j] * almath.TO_RAD
            except:
                angles = math.radians(to_angles[j])

            self.alMotion.setAngles(joints_to_move[j], angles, speed)

    def say(self, to_say):
        if self.language == "English":
            to_say = self.translate_from_norwegian(to_say)
            self.tts.say(to_say)
        else:
            to_say = self.translate(to_say)
            self.ttsNOR.say(to_say)

    def translate_from_norwegian(self, nor_sentence):
        print(nor_sentence)
        translation_dict = {
            "Kom igjen! Alle sammen!": "Come on! Everybody!",
            "Kom igjen!": "Come on!",
            "Dere er flinke!": "You are doing great!",
            "Bra jobbet!": "Good job!"
        }

        if nor_sentence in translation_dict.keys():
            english_sentence = translation_dict.get(nor_sentence)
        else:
            english_sentence = nor_sentence

        print(english_sentence)
        return english_sentence


    def translate(self, english_sentence):
        english_sentence = english_sentence.strip()

        translation_dict = {
            "We will start by warming up!": "Nå skal vi varme opp!",
            "We will rotate our head to warm up our neck.":"Vi begynner med nakken. Prøv å gjøre det samme som meg.",
            "Are you starting to feel warm now?": "Begynner dere å føle dere varme nå?",
            "Move your left arm up.": "Løft venstre arm opp.",
            "and down again.": "og ned igjen!",
            "The other hand!": "Den andre hånden!",
            "And down!": "Og ned",
            "And Again!": "Og igjen!",
            "Let us do it a bit more advanced! Move your hand up. and bend to the side.": "Nå skal vi gjøre det litt mer avansert. Ta hånden opp. Og bøy til siden.",
            "Let us do the same. but with the other hand!": "Nå skal vi gjøre det samme. Men med andre hånden.",
            "Are you ready for the next one?": "Er dere klare for neste",
            "Thank you for today! I had so much fun! I hope all you cool people. want to work out. with me again!": "Tusen takk for i dag. Jeg har hatt det veldig gøy! Jeg håper dere vil trene med meg igjen.",
            "We will start by warming up our wrists!": "Nå skal vi begynne med å varme opp håndleddene.",
            "Hold your hands like this. Then we start to roll!": "Hold hendene deres slik. Så skal vi rulle.",
            "And relax!": "Så kan vi slappe av.",
            "Next. We will warm up our neck.": "Nå skal vi varme opp nakken.",
            "Look Up!": "Se opp.",
            "And Down!": "Se ned.",
            "Are you ready to workout now?": "Er dere klare for å trene nå?",
            "Next, we will stretch and bend!": "Nå er det på tide og strekke og bøye litt.",
            "Move to the left!": "Bøy dere til venstre.",
            "To the right!": "Så til høyre.",
            "Again!": "En gang til.",
            "Now, we will try bending forward!": "Nå skal vi bøye oss fremover.",
            "Let us work out our triceps.": "Det er også viktig å trene baksiden av armene.",
            "Now we will shake loose! You don't need to follow me. Just do something. shake loose!": "Da kan vi riste løs. Dere trenger ikke å følge meg. Bare rist litt på leddene.",
            "Now we will stretch, behind or head and down to our back. Try to follow me!": "Nå skal vi strekke litt. Vi skal ta hånden bak hode. Deretter bak korsryggen. Prøv å følg meg.",
            "Now we will do the other hand": "Så tar vi den andre hånden.",
            "Let us stretch!": "Da er det på tide å strekke.",
            "Right arm to the ceiling!": "",
            "Relax!": "Slapp av.",
            "Then the other arm!": "Så tar vi den andre armen.",
            "Since we often need to lift things, we will work out out arms.": "Vi trenger ofte å løfte ting. Derfor skal vi nå trene armene.",
            "Hold your hands like this, and follow me.": "Hold hendene slik som meg. Prøv å følg meg.",
            "And relax!": "Og slapp av.",
            "If you can, lean forward, and follow me!": "Visst dere kan. Bøy dere fremover. Og følg meg.",
            "Now we will shake loose! You don't need to follow me. Just do something!": "Da kan vi riste løs. Dere trenger ikke å følge meg. Bare ris litt på leddene.",
            "Next. we will stretch and bend!": "Nå skal vi strekke og bøye.",
            "Move to the left!": "Bøy dere til venstre.",
            "To the right!": "Så bøyer vi til høyre.",
            "Now. we will try bending forward!": "Nå skal vi prøve å bøye oss fremover igjen.",
            "Please. follow me!": "Prøv å følg meg.",
            "This one is a bit more challenging. Just do the parts you are comfortable with.": "Den neste er litt vanskligere. Men prøv å gjør det samme som meg.",
            "This is fun!": "Dette er gøy!",
            "The other hand!": "Den andre hånden!",
            "This is the last one. Before we shake it out.": "Dette er den siste øvelsen. Før vi skal riste løs.",
            }
        if english_sentence in translation_dict.keys():
            norwegian_sentence = translation_dict.get(english_sentence)
        else:
            norwegian_sentence = english_sentence

        return norwegian_sentence


    def __control_awareness(self, state):
        self.awareness.set_basic_awareness(state)

    def __control_autonomous_abilities(self, state):
        self.autonomousLifeController.set_all_autonomous_abilities(state, state, state, state)

