# -*- coding: utf-8 -*-


from Tkinter import * # Import GUI elements from Tkinter package
from os import path as osPath  # Import path
from functools import partial

## ADDONS
from DeviceInputs.KeyboardController import KeyboardController

import os
import datetime
import webbrowser

from ImprovisationPackage.ImprovisationManager import Improvisation
from Daily.DailyMessagesGUI import DailyMessagesGUI

'''
GUI is the graphical interface for interacting with Pepper (or the virtual Pepper through Choregraph).
The GUI consists of a scalebar for each joint, entry field for moving the robot, entry field for talking, scalebar
for speed, buttons for opening and closing hands and demo buttons.

The GUI is to be extended with the possibility to save all joints positions, movement and text in a csv.
'''
class GUI(object):
    def __init__(self, controller):
        self.pepperController = controller
        self.improvisation = Improvisation(self.pepperController)

        self.keyboardController = KeyboardController(self.pepperController.get_session(), self.pepperController)
        self.keyboardController.start()
        self.stop_listen()

        self.filepath = osPath.dirname(osPath.realpath(__file__))
        self.backgroundColor = "#a8e6ff"#"#a1dbcd"

        # Initalising the master frame.
        topLevel = Tk()
        topLevel.resizable(width=False, height=False)
        topLevel.minsize(width=1700, height=700) #self.root.resizable(width=False, height=False)
        # set the window background to hex code '#a1dbcd'
        topLevel.configure(background=self.backgroundColor)
        # set the window title
        topLevel.title("NTNU - Pepper for Health ")

        # ------------------------------------------------------------------------------------------------------------
        # ---------------- Exercise Control Pane ---------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------
        self.exercisePane = LabelFrame(topLevel, text="  Exercise Control:  ", padx=5, pady=5,
                                       bg=self.backgroundColor, width=800,
                                       height=350, font="Verdana 9 bold")  # Separator(topLevel, orient=HORIZONTAL)
        self.exercisePane.grid_propagate(False)
        self.exercisePane.grid(row=0, column=0, sticky=W, padx=20, pady=10)

        self.roomScenarioLabel = Label(self.exercisePane, text="Room scenario", bg=self.backgroundColor, padx=10,
                                       font="Verdana 9 bold")
        self.fovLabel = Label(self.exercisePane, text="Approach range (degrees):", bg=self.backgroundColor, padx=10)
        self.fovScale = Scale(self.exercisePane, from_=0, to=90, orient=HORIZONTAL, length=150, resolution=1, bg=self.backgroundColor)
        self.fovScale.set(0)

        self.roomScenarioLabel.grid(row=0, column=0, pady=8, sticky=W)
        self.fovLabel.grid(row=1, column=0, sticky=W)
        self.fovScale.grid(row=1, column=1, sticky=W)

        # self.files = self.exerciseHandler.get_available_exercises()
        # self.file_path = StringVar(self.exercisePane)
        # self.file_path.set("demo_exercise.csv")  # default value
        # self.file_options = OptionMenu(self.exercisePane, self.file_path, *self.files)

        self.spacingLabel1 = Label(self.exercisePane, text="   ", bg=self.backgroundColor, padx=10)
        self.spacingLabel1.grid(row=2, column=0)

        self.exerciseLabel = Label(self.exercisePane, text="Exercise", bg=self.backgroundColor, padx=10,
                                   font="Verdana 9 bold")
        self.chooseExerciseLabel = Label(self.exercisePane, text="Choose exercise: ", bg=self.backgroundColor, padx=10)
        self.files = ["Exercise 1", "Exercise 2", "Exercise 3", "Exercise 4"]
        self.file_path = StringVar(self.exercisePane)
        self.file_path.set("Exercise 1")  # default value
        self.file_options = OptionMenu(self.exercisePane, self.file_path, *self.files, command=self.OptionMenu_SelectionEvent)
        self.file_options.config(width=20)

        self.exerciseLabel.grid(row=3, column=0, sticky=W)
        self.chooseExerciseLabel.grid(row=4, column=0, sticky=W)
        self.file_options.grid(row=4, column=1, sticky=W)

        self.spacingLabel2 = Label(self.exercisePane, text="     ", bg=self.backgroundColor, padx=15)
        self.spacingLabel2.grid(row=4, column=2)

        self.statSep = Frame(self.exercisePane, bg=self.backgroundColor)
        self.statSep.grid(row=4, column=3, sticky=W, columnspan=2, rowspan=2)

        self.exerciseStatsLabel = Label(self.statSep, text="Exercise statistics ", bg=self.backgroundColor,
                                        font="Verdana 9 bold")
        self.durationLabel = Label(self.statSep, text="Duration: ", bg=self.backgroundColor)
        self.lastPlayedLabel = Label(self.statSep, text="Last played: ", bg=self.backgroundColor)

        self.durationValueLabel = Label(self.statSep, text="3:55", bg=self.backgroundColor)
        self.lastPlayedValueLabel = Label(self.statSep, text="10.01.2017", bg=self.backgroundColor)

        self.exerciseStatsLabel.grid(row=0, column=0, sticky=W)
        self.durationLabel.grid(row=1, column=0, sticky=W)
        self.lastPlayedLabel.grid(row=2, column=0, sticky=W)
        self.durationValueLabel.grid(row=1, column=1, sticky=W)
        self.lastPlayedValueLabel.grid(row=2, column=1, sticky=W)


        self.spacingLabel1 = Label(self.exercisePane, text="   ", bg=self.backgroundColor, padx=10)
        self.spacingLabel1.grid(row=6, column=0)

        self.buttonSep = Frame(self.exercisePane, bg=self.backgroundColor)
        self.buttonSep.grid(row=7, column=0, sticky=W, columnspan=2, padx=20)

        self.playButton = Button(self.buttonSep, text="Play", width=10, command=self.play_exercise)
        self.pauseButton = Button(self.buttonSep, text="Pause", width=10, command=self.pause_exercise)
        self.stopButton = Button(self.buttonSep, text="Stop", width=10, command=self.stop_exercise)

        self.playButton.grid(row=0, column=0, padx=10, sticky=W)
        self.pauseButton.grid(row=0, column=1, padx=10, sticky=W)
        self.stopButton.grid(row=0, column=2, padx=10, sticky=W)

        self.spacingLabel1 = Label(self.exercisePane, text="   ", bg=self.backgroundColor, padx=10)
        self.spacingLabel1.grid(row=8, column=0, pady=3)

        self.feedbackLabel = Label(self.exercisePane, text="Feedback: ", bg=self.backgroundColor, padx=10,
                                   font="Verdana 9 bold")
        self.feedbackLabel.grid(row=9, column=0, sticky=W, pady=4)

        self.feedBackButton = Button(self.exercisePane, text="Give feedback", width=20, command=self.give_feedback)
        self.feedBackOptions = ["Alle kan prøve!", "Kom igjen!", "Bra jobbet!", "Dere er flinke!", "Kjempebra!", "Er dere lei nå?"]
        self.currentFeedback = StringVar(self.exercisePane)
        self.currentFeedback.set("Bra jobbet!")  # default value
        self.feedBackOptionsMenu = OptionMenu(self.exercisePane, self.currentFeedback, *self.feedBackOptions)
        self.feedBackOptionsMenu.config(width=60)

        self.feedBackButton.grid(row=10, column=0)
        self.feedBackOptionsMenu.grid(row=10, column=1, columnspan=3)

        # ------------------------------------------------------------------------------------------------------------
        # ---------------- Transport Control Pane --------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------
        self.transportControlPane = LabelFrame(topLevel, text="  Transport Control:  ", padx=5, pady=5,
                                               bg=self.backgroundColor, width=800, height=300, font="Verdana 9 bold")
        self.transportControlPane.grid_propagate(False)
        self.transportControlPane.grid(row=1, column=0, sticky=W, padx=20, pady=10)

        self.transport_label = Label(self.transportControlPane, text="Turn on/off keyboard control:  ",
                                     bg=self.backgroundColor)
        self.transport_label.grid(row=0, column=0, columnspan=2, padx=10, sticky=W, pady=10)

        self.transport_toggle = Button(self.transportControlPane, text="Off", width=12, relief="raised",
                                       command=self.transport_toggle)
        self.transport_toggle.grid(row=0, column=3)

        self.spacingLabel1B = Label(self.transportControlPane, text="   ", bg=self.backgroundColor, padx=10)
        self.spacingLabel1B.grid(row=1, column=0, pady=20, padx=10, sticky=W)

        # How to use part of transport control
        self.howToUseLabel = Label(self.transportControlPane, text="How to use Transport Control with keyboard:",
                                   bg=self.backgroundColor, font="Verdana 9 bold")
        self.howToUseLabel.grid(row=1, column=0, columnspan=3, sticky=W, padx=10, pady=7)
        self.keyboardControlLabel = Label(self.transportControlPane, text=" - Arrows on keyboard for driving Pepper (only one at the time)", bg=self.backgroundColor)
        self.keyboardControlLabel.grid(row=2, column = 0)
        self.f1Label = Label(self.transportControlPane, text=" - F1 to Wave", bg=self.backgroundColor)
        self.f2Label = Label(self.transportControlPane, text=" - F2 to Say Hello", bg=self.backgroundColor)
        self.f1Label.grid(row=3, column=0)
        self.f2Label.grid(row=4, column=0)
        # How to add icons...

        self.spacingLabel1C = Label(self.transportControlPane, text="   ", bg=self.backgroundColor, padx=10)
        self.spacingLabel1C.grid(row=5, column=0)
        #self.soundLabel = Label(self.transportControlPane, text="Adjust sound: ", bg=self.backgroundColor, padx=10)
        #self.soundButton = Button(self.transportControlPane, text="Adjust Sound", command=self.adjustSound)
        #self.soundLabel.grid(row=6, column=0)
        #self.soundButton.grid(row=6, column=0, pady=20, sticky=W)

        ############### CHANGES - REVISION 1.0 #########################
        self.speechRatePane = LabelFrame(self.transportControlPane, bg=self.backgroundColor)
        self.speechRatePane.grid_propagate(True)
        self.speechRatePane.grid(row=6, column=0, sticky=W, padx=10, pady=1)

        self.soundLabel = Label(self.speechRatePane, text="Adjust sound: ", bg=self.backgroundColor, padx=10)
        self.soundButton = Button(self.speechRatePane, text="Adjust Sound", command=self.adjustSound)
        # self.soundLabel.grid(row=6, column=0)
        self.soundButton.grid(row=0, column=0, pady=3, sticky=W)

        #self.speechRateLabel = Button(self.speechRatePane, text="Set Speech Rate", padx=20, command=self.changeSpeechRate)
        self.speechRateScale = Scale(self.speechRatePane, from_=0.1, to=0.6, orient=HORIZONTAL, length=150,
                                     resolution=0.05,
                                     bg=self.backgroundColor, command=self.changeSpeechRate)
        self.speechRateScale.set(self.pepperController.getPreviousSpeechRate())

        #self.speechRateLabel.grid(row=1, column=1, sticky=W)
        self.speechRateScale.grid(row=1, column=0, sticky=W)

        # ------------------------------------------------------------------------------------------------------------
        # ---------------- Conversation Control Pane -----------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------
        self.conversationPane = LabelFrame(topLevel, text="  Manual Conversation Control:  ", padx=5, pady=5,
                                           bg=self.backgroundColor, width=800,
                                           height=350, font="Verdana 9 bold")

        self.conversationPane.grid_propagate(False)
        self.conversationPane.grid(row=0, column=1, sticky=W, padx=20, pady=10)

        self.manualSpeechLabel = Label(self.conversationPane, text="Manual Speech Control: ", font="Verdana 9 bold",
                                       bg=self.backgroundColor)
        self.manualSpeechLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.speechEntry = Entry(self.conversationPane, width=65)
        self.speechEntry.grid(row=1, column=0, columnspan=2, sticky=W, padx=10)

        self.manualSpeechButton = Button(self.conversationPane, text="Say", width=10, command=self.say_from_entry)
        self.manualSpeechButton.grid(row=1, column=2, padx=10, sticky=W)

        self.spacingLabel1C = Label(self.conversationPane, text="   ", bg=self.backgroundColor, padx=10)
        self.spacingLabel1C.grid(row=2, column=0, pady=1, padx=2, sticky=W)

        self.predefinedAnswersSep = Frame(self.conversationPane, bg=self.backgroundColor)
        self.predefinedAnswersSep.grid(row=3, column=0, sticky=W, columnspan=3, rowspan=5, padx=10)

        self.greetingsButton = Button(self.predefinedAnswersSep, text="Say", width=10, command=self.say_greeting)
        self.questionsButton = Button(self.predefinedAnswersSep, text="Say", width=10, command=self.say_question)
        self.answersButton = Button(self.predefinedAnswersSep, text="Say", width=10, command=self.say_answer)
        self.complementButton = Button(self.predefinedAnswersSep, text="Say", width=10, command=self.say_complement)

        self.greetingsButton.grid(row=1, column=2, padx=10, sticky=W)
        self.questionsButton.grid(row=3, column=2, padx=10, sticky=W)
        self.answersButton.grid(row=5, column=2, padx=10, sticky=W)
        self.complementButton.grid(row=7, column=2, padx=10, sticky=W)

        self.greetingsLabel = Label(self.predefinedAnswersSep, text="Greetings: ", font="Verdana 9 bold",
                                    bg=self.backgroundColor)
        self.questionsLabel = Label(self.predefinedAnswersSep, text="Questions: ", font="Verdana 9 bold",
                                    bg=self.backgroundColor)
        self.answersLabel = Label(self.predefinedAnswersSep, text="Answers: ", font="Verdana 9 bold",
                                  bg=self.backgroundColor)
        self.complementLabel = Label(self.predefinedAnswersSep, text="Complements: ", font="Verdana 9 bold",
                                     bg=self.backgroundColor)
        self.greetingsLabel.grid(row=0, column=1, padx=2, sticky=W, pady=3)
        self.questionsLabel.grid(row=2, column=1, padx=2, sticky=W, pady=3)
        self.answersLabel.grid(row=4, column=1, padx=2, sticky=W, pady=3)
        self.complementLabel.grid(row=6, column=1, padx=2, sticky=W, pady=3)

        self.greetingOptions = ["Hallo! Mitt navn er Pepper!", "God morgen! Jeg håper du får en fin dag!", "Ha en fin dag!",
                                "God dag!", "Hei! Hyggelig å treffe deg!", "God morgen alle sammen!"]
        self.currentGreeting = StringVar(self.predefinedAnswersSep)
        self.currentGreeting.set("Ha en fin dag!")  # default value
        self.greetingOptionsMenu = OptionMenu(self.predefinedAnswersSep, self.currentGreeting, *self.greetingOptions)
        self.greetingOptionsMenu.config(width=60)
        self.greetingOptionsMenu.grid(row=1, column=1, sticky=NW)

        self.questionsOptions = ["Hvordan har du det i dag?", "Hva heter du?", "Har du lyst til å trene?", "Hva liker du å snakke om?", "Hva liker du å holde på med?", "Hva synes du om meg?"]
        self.currentQuestions = StringVar(self.predefinedAnswersSep)
        self.currentQuestions.set("Hva heter du?")  # default value
        self.questionsOptionsMenu = OptionMenu(self.predefinedAnswersSep, self.currentQuestions, *self.questionsOptions)
        self.questionsOptionsMenu.config(width=60)
        self.questionsOptionsMenu.grid(row=3, column=1, sticky=NW)

        self.answersOptions = ["Mitt navn er Pepper!", "Jeg vet ikke hva som er til middag i dag.",
                               "Jeg vet ikke desverre!", "Jeg beklager.", "Jeg liker å snakke om mye forskjellig.", "Jeg liker å være med mennesker.", "Jeg husker ikke."]
        self.currentAnswers = StringVar(self.predefinedAnswersSep)
        self.currentAnswers.set("Jeg vet ikke desverre!")  # default value
        self.answersOptionsMenu = OptionMenu(self.predefinedAnswersSep, self.currentAnswers, *self.answersOptions)
        self.answersOptionsMenu.config(width=60)
        self.answersOptionsMenu.grid(row=5, column=1, sticky=NW)

        self.complementOptions = ["Du ser flott ut i dag!", "Det er en nydelig dag!", "Du er så hyggelig med meg!",
                                "Jeg blir så glad for å se deg!", "Du imponerer meg!", "Du er morsom!", "Det er så fantastisk å være her."]
        self.currentComplement = StringVar(self.predefinedAnswersSep)
        self.currentComplement.set("Du er så hyggelig med meg!")  # default value
        self.complementOptionsMenu = OptionMenu(self.predefinedAnswersSep, self.currentComplement, *self.complementOptions)
        self.complementOptionsMenu.config(width=60)
        self.complementOptionsMenu.grid(row=7, column=1, sticky=NW)

        # ------------------------------------------------------------------------------------------------------------
        # ---------------- Other Control Pane --------------------------------
        # ------------------------------------------------------------------------------------------------------------
        self.otherPane = LabelFrame(topLevel, text="  Other Functions:  ", padx=5, pady=5,
                                    bg=self.backgroundColor, width=800,
                                    height=300, font="Verdana 9 bold")

        self.otherPane.grid_propagate(False)
        self.otherPane.grid(row=1, column=1, sticky=W, padx=20, pady=10)

        self.improvisationSep = Frame(self.otherPane, width=250,bg=self.backgroundColor)
        self.improvisationSep.grid(row=0, column=0, sticky=W, columnspan=3, rowspan=5)

        self.spacingLabel4A = Label(self.otherPane, text=" ",bg=self.backgroundColor)
        self.spacingLabel4A.grid(row=0, column=4, padx=5)

        self.otherSep = Frame(self.otherPane, width=250,bg=self.backgroundColor)
        self.otherSep.grid(row=0, column=5, sticky=NW, columnspan=3, rowspan=5)


        self.improvisationLabel = Label(self.improvisationSep, text="Improvisation Session:", font="Verdana 9 bold",
                                    bg=self.backgroundColor)
        self.improvisationButton = Button(self.improvisationSep, text="Run Improvisation", width=20, command=self.run_improvisation)
        self.improvisationButton.grid(row=1, column=0, columnspan=2)
        self.improvisationLabel.grid(row=0, column=0, sticky=W)

        self.announcementButton = Button(self.improvisationSep, text="Add Announcement", width=18,
                                          command=self.add_announcement_pop_up)
        self.seeAnnouncementButton = Button(self.improvisationSep, text="See Announcements", width=18,
                                          command=self.see_announcements_pop_up)
        self.announcementButton.grid(row=3, column=0)
        self.seeAnnouncementButton.grid(row=3, column=1)


        self.spacingLabel4A = Label(self.improvisationSep, text=" ",bg=self.backgroundColor)
        self.spacingLabel4A.grid(row=2, column = 0)

        self.spacingLabel4B = Label(self.improvisationSep, text=" ",bg=self.backgroundColor)
        self.spacingLabel4B.grid(row=4, column=0)


        self.whatIsImLabel = Label(self.improvisationSep, text="What is Improvisation Session:",bg=self.backgroundColor, font="Verdana 8 bold")
        self.whatIsImLabel.grid(row=5, column=0, columnspan=2)

        self.whatIsImLabel2 = Label(self.improvisationSep, text="- It is a session where Pepper talks, "
                                                                "he tells a story, the \n weather for today "
                                                                "and potential announcements. \n See "
                                                                + "'" + "Help" + "'" + " for more information!",bg=self.backgroundColor)
        self.whatIsImLabel2.grid(row=6, column=0, sticky=W, columnspan=2)

        self.whatIsAnnoucementLabel = Label(self.improvisationSep, text="What is Announcement?",bg=self.backgroundColor, font="Verdana 8 bold")
        self.whatIsAnnoucementLabel.grid(row=7, column=0, columnspan=2)

        self.whatIsAnnoucementLabel2 = Label(self.improvisationSep, text="- It is a message (or several) that will be "
                                                                         "presented \n during the improvisation session."
                                                                         " \n It can be news or todays dinner and so on. \n See "
                                                                + "'" + "Help" + "'" + " for more information!",bg=self.backgroundColor)
        self.whatIsAnnoucementLabel2.grid(row=8, column=0, sticky=W, columnspan=2)

        # OTHER PANE - INCLUDES BUTTONS FOR JOKE, WEATHER, etc...
        self.animationLabel = Label(self.otherSep, text="Animations:", font="Verdana 9 bold",bg=self.backgroundColor)
        self.animationLabel.grid(row=4, column=0, sticky=NW)
        self.playAnimationButton = Button(self.otherSep, text="Play Animation", width=12, command=self.play_animation)
        self.playAnimationButton.grid(row=5, column=2, columnspan=1, sticky=NW)
        self.playAnimationButton.config(width=15)
        self.animationOptions = ["WakeUp", "Wings",
                                 "Binoculars", "Sneeze", "SpaceShuttle", "HappyBirtday", "Drink", "Laugh", "DriveCar",
                                 "TakePicture", "Fitness", "MysticalPower", "AirGuitar", "Knight", "Bandmaster"]
        self.currentAnimation = StringVar(self.otherSep)
        self.currentAnimation.set("WakeUp")  # default value
        self.animationOptionsMenu = OptionMenu(self.otherSep, self.currentAnimation, *self.animationOptions)
        self.animationOptionsMenu.config(width=12)
        self.animationOptionsMenu.grid(row=5, column=0, sticky=W)


        self.resetJointsLabel = Label(self.otherSep, text="Reset all Joints:", font="Verdana 9 bold",bg=self.backgroundColor)
        self.resetJointsLabel.grid(row=7, column=2, sticky=W)
        self.goToStdPoseButton = Button(self.otherSep, text="Reset Joints", command=self.go_to_std_pose)
        self.goToStdPoseButton.grid(row=8, column=2, sticky=W)
        self.goToStdPoseButton.config(width=15)

        self.spacingLabel4C = Label(self.otherSep, text=" ",bg=self.backgroundColor)
        self.spacingLabel4C.grid(row=3, column=0)
        self.spacingLabel4D = Label(self.otherSep, text=" ",bg=self.backgroundColor)
        self.spacingLabel4D.grid(row=6, column=0)
        self.spacingLabel4E = Label(self.otherSep, text=" ",bg=self.backgroundColor)
        self.spacingLabel4E.grid(row=0, column=1)
        self.spacingLabel4F = Label(self.otherSep, text=" ",bg=self.backgroundColor)
        self.spacingLabel4F.grid(row=9, column=0)


        self.jokeLabel = Label(self.otherSep, text="Jokes:", font="Verdana 9 bold",bg=self.backgroundColor)
        self.jokeLabel.grid(row=7, column=0, sticky=W)
        self.jokeButton = Button(self.otherSep, text="Play Joke", command=self.get_joke)
        self.jokeButton.grid(row=8, column=0, sticky=W)
        self.jokeButton.config(width=15)

        self.weatherLabel = Label(self.otherSep, text="Weather Forecast:", font="Verdana 9 bold",bg=self.backgroundColor)
        self.weatherLabel.grid(row=0, column=0, sticky=W)
        self.weatherButton = Button(self.otherSep, text="Get Forecast", command=self.get_weather_forecast)
        self.weatherButton.grid(row=1, column=2, sticky=W)
        self.weatherButton.config(width=15)

        self.weatherOptions = ["Today", "+1 Day", "+2 Days",
                                  "+3 Days", "+4 Days", "+5 Days"]
        self.currentWeatherOption = StringVar(self.otherSep)
        self.currentWeatherOption.set("Today")  # default value
        self.weatherOptionsMenu = OptionMenu(self.otherSep, self.currentWeatherOption, *self.weatherOptions)
        self.weatherOptionsMenu.config(width=12)
        self.weatherOptionsMenu.grid(row=1, column=0, sticky=W)

        self.helpLabel = Label(self.otherSep, text="Help:", font="Verdana 9 bold",bg=self.backgroundColor)
        self.helpLabel.grid(row=10, column=0, sticky=W)
        self.helpButton = Button(self.otherSep, text="Help", command=self.help)
        self.helpButton.grid(row=11, column=0, sticky=W)
        self.helpButton.config(width=15)

        self.aboutLabel = Label(self.otherSep, text="About:", font="Verdana 9 bold",bg=self.backgroundColor)
        self.aboutLabel.grid(row=10, column=2, sticky=W)
        self.aboutButton = Button(self.otherSep, text="About", command=self.about)
        self.aboutButton.grid(row=11, column=2, sticky=W)
        self.aboutButton.config(width=15)

        # ------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------

        # draw the window, and start the 'application'
        topLevel.protocol('WM_DELETE_WINDOW', self.onCloseHandler)
        topLevel.mainloop()


        # GUI example code:
        '''
            # create a label for the instructions
        lblInst = Label(topLevel, text="Please login to continue:", fg="#383a39", bg="#a1dbcd",
                                font=("Helvetica", 16))
        # and pack it into the window
        lblInst.pack()

        # create the widgets for entering a username
        lblUsername = Label(topLevel, text="Username:", fg="#383a39", bg="#a1dbcd")
        entUsername = Entry(topLevel)
        # and pack them into the window
        lblUsername.pack()
        entUsername.pack()

        # create the widgets for entering a username
        lblPassword = Label(topLevel, text="Password:", fg="#383a39", bg="#a1dbcd")
        entPassword = Entry(topLevel)
        # and pack them into to the window
        lblPassword.pack()
        entPassword.pack()

        # create a button widget called btn
        btn = Button(topLevel, text="Login", fg="#a1dbcd", bg="#383a39")
        # pack the widget into the window
        btn.pack()
        '''

    def onCloseHandler(self):
        self.keyboardController.stop()
        self.pepperController.stop_server()
        os._exit(0)

    # Transport
    def transport_toggle(self):
        if self.transport_toggle.config('relief')[-1] == 'sunken':
            self.transport_toggle.config(relief="raised", text="Off")
            self.stop_listen()
        else:
            self.transport_toggle.config(relief="sunken", text="On")
            self.start_listen()

    # Key listener thread
    def stop_listen(self):
        self.keyboardController.stop()
        self.pepperController.stop_moving()
        print("Keyboard listener off")

    def start_listen(self):
        self.keyboardController.start()
        print("Keyboard listener on")

    # Exercise functions


    def play_exercise(self):
        exercise_number = int(filter(str.isdigit, self.file_path.get()))
        self.pepperController.update_exercise_stats(exercise_number)

        if self.pepperController.get_pause_status():
            self.playButton.config(text="Play")
            self.pauseButton.config(text="Pause")

        fov = self.fovScale.get()
        exercisePath = self.file_path.get().replace(" ", "") + ".csv"
        self.pepperController.play_exercise(exercisePath, fov)

    def pause_exercise(self):
        self.playButton.config(text="Continue")
        self.pauseButton.config(text="In Pause")
        self.pepperController.pause_exercise()

    def stop_exercise(self):
        self.pepperController.stop_exercise()
        self.go_to_std_pose()

    def give_feedback(self):
        feedback = self.currentFeedback.get()
        self.pepperController.give_feedback(feedback)

    # Exercise stats
    def OptionMenu_SelectionEvent(self, event):  # I'm not sure on the arguments here, it works though
        exercise_number = int(filter(str.isdigit, self.file_path.get()))
        print(exercise_number)
        duration, last_played = self.pepperController.get_exercise_stats(exercise_number)
        self.update_exercise_stats_in_gui(duration,last_played)

    def update_exercise_stats_in_gui(self, duration, last_played):
        self.durationValueLabel.config(text=duration)
        self.lastPlayedValueLabel.config(text=last_played)


        # Manual conversation functions
    def say_from_entry(self):
        to_say = self.speechEntry.get()
        self.say(to_say)

    def say_greeting(self):
        to_say = self.currentGreeting.get()
        self.say(to_say)

    def say_answer(self):
        to_say = self.currentAnswers.get()
        self.say(to_say)

    def say_question(self):
        to_say = self.currentQuestions.get()
        self.say(to_say)

    def say_complement(self):
        to_say = self.currentComplement.get()
        self.say(to_say)

    def say(self, to_say):
        if self.pepperController.get_language() == "Norwegian":
            self.pepperController.say(to_say)
        else:
            to_say = self.temp_translation(to_say)
            self.pepperController.say(to_say)


    # Other functions
    def get_weather_today(self):
        self.pepperController.get_todays_weather()

    def get_weather_tomorrow(self):
        self.pepperController.get_tomorrows_forecast()

    def get_weather_forecast(self):
        when = self.currentWeatherOption.get()
        if when == "Today":
            self.pepperController.get_todays_weather()
        elif when == "+1 Day":
            self.pepperController.get_tomorrows_forecast()
        else:
            days = int(filter(str.isdigit, when))
            now = datetime.datetime.now()
            now += datetime.timedelta(days=days)
            #now = now.strftime("%Y-%m-%d")
            self.pepperController.get_weather_forecast(date=now)


    def get_joke(self):
        self.pepperController.get_joke()

    def run_improvisation(self):
        self.improvisation.get_improvisation()

    def add_announcement(self):
        msg = self.message_entry.get()
        type = self.currentType.get()
        self.improvisation.add_announcement(msg, type)
        self.msgGUI.destroy()

    def tell_story(self):
        self.improvisation.story()

    # Animation
    def play_animation(self):
        animation_name = self.currentAnimation.get()
        path = self.pepperController.get_animation_path(animation_name)
        self.pepperController.play_animation(path)

    # Posture
    def go_to_std_pose(self):
        self.pepperController.go_to_standard_pose()

    # TEMP - Because of stress...
    def temp_translation(self, norwegian_sentence):
        norwegian_sentence = norwegian_sentence.replace('å', 'aa')

        translation_dict = {
            "Ha en fin dag!": "Have a nice day!",
            "Hallo! Mitt navn er Pepper!": "Hello! My name is Pepper!",
            "God morgen!": "Good morning!",
            "God dag! Jeg haaper du faar en fin dag!": "Hello! I hope you will get a nice day.",
            "Hei! Hyggelig aa treffe deg!": "Very nice to meet you.",
            "Hvordan har du det i dag?": "How are you?",
            "Hva heter du?": "What is your name?",
            "Har du lyst til aa trene?": "Do you want to workout?",
            "Mitt navn er Pepper!": "My name is Pepper!",
            "Jeg vet ikke hva som er til middag i dag.": "I do not know what we will have for dinner today.",
            "Jeg vet ikke desverre!": "I do not know. I am sorry.",
            "Jeg beklager.": "I am sorry.",
            "Du ser flott ut i dag!": "You look beautiful today.",
            "Det er en nydelig dag!": "It is a lovely day.",
            "Du er saa hyggelig med meg!": "You are so nice to me!",
            "Jeg blir saa glad for aa se deg!":"I am so happy to see you."}

        if norwegian_sentence in translation_dict.keys():
            english_sentence = translation_dict[norwegian_sentence]
        else:
            english_sentence = norwegian_sentence

        return english_sentence

    def help(self):
        self.pepperController.get_help()

    def adjustSound(self):
        self.pepperController.adjust_sound()

    def changeSpeechRate(self, value):
        #self.pepperController.changeSpeechRate(self.speechRateScale.get())
        self.pepperController.changeSpeechRate(value)

    # -----------------------------------------------------------------------------
    # ------------------------- GUI for ABOUT -------------------------------------
    # -----------------------------------------------------------------------------
    def about(self):
        self.aboutGUI = Toplevel()
        self.aboutGUI.configure(background=self.backgroundColor)
        self.aboutGUI.resizable(width=False, height=False)
        self.aboutGUI.geometry('{}x{}'.format(450, 450))
        self.aboutGUI.title('About')

        self.aboutTitleLabel = Label(self.aboutGUI, text="About Pepper for Health Software:",
                                     bg=self.backgroundColor, font="Verdana 9 bold")
        self.developmentLabel = Label(self.aboutGUI, text="The software is developed at NTNU Ålesund at \n the Department "
                                                          "of ICT and Natural Sciences. \n The developers are "
                                                          "Magnus Gribbestad, Karl-Eirik Aasen \n and Eirik Homlong.")
        self.licenceAndTerms = Label(self.aboutGUI, text="Licence and Terms of Use:",
                                     bg=self.backgroundColor, font="Verdana 9 bold")
        self.licenceLabel = Label(self.aboutGUI, text="Software licences is revocable, non-exclusive, \n non-transfarable, "
                                                      "limited right to install and \n use the program on a single computer. "
                                                      " The program \n can under no circumstance be used without a "
                                                      "predefined \n agreement with the development team or the \n Department "
                                                    "of ICT and Natural Sciences. \n The code can not be copied or "
                                                      "reused \n without an agreement. All rights resereved. \n "
                                                      "The software is experimental, NTNU cannot \n be held responsible"
                                                      "for any damages that might occur. \n Usage at own responsibility.")

        self.apiLabel = Label(self.aboutGUI, text="API's:",
                                     bg=self.backgroundColor, font="Verdana 9 bold")
        self.apiWeatherLabel = Label(self.aboutGUI, text="Weather data is acquired through an API from: \n"
                                                         "http://openweathermap.org/appid.")
        self.apiSpeechLabel = Label(self.aboutGUI, text="Norwegian speech is acquired from: \n https://responsivevoice.org/.")
        self.spacerLabel = Label(self.aboutGUI, text="   ", bg=self.backgroundColor)

        self.contactLabel = Label(self.aboutGUI, text="Contact:",
                              bg=self.backgroundColor, font="Verdana 9 bold")
        self.contact2Label = Label(self.aboutGUI, text="- NTNU Ålesund")

        self.aboutTitleLabel.pack()
        self.developmentLabel.pack()
        self.licenceAndTerms.pack()
        self.licenceLabel.pack()
        self.apiLabel.pack()
        self.apiWeatherLabel.pack()
        self.spacerLabel.pack()
        self.apiSpeechLabel.pack()
        self.contactLabel.pack()
        self.contact2Label.pack()

        self.aboutGUI.protocol('WM_DELETE_WINDOW', self.aboutGUI.destroy)

    '''
    WARNING: Should be extracted and put as classes later
    '''
    # -----------------------------------------------------------------------------
    # ------------------ GUI for ADDING ANNOUNCEMENT ------------------------------
    # -----------------------------------------------------------------------------
    def add_announcement_pop_up(self):
        self.msgGUI = Toplevel()
        self.msgGUI.configure(background=self.backgroundColor)
        self.msgGUI.resizable(width=False, height=False)
        self.msgGUI.geometry('{}x{}'.format(450, 270))
        self.msgGUI.title('Add Announcement')

        self.msgExplanation = Label(self.msgGUI, text="This messages will be told during \n the improvisation session today!",
                                    bg=self.backgroundColor)
        self.message_entry = Entry(self.msgGUI)
        self.message_entry.insert(END, "I dag er det kjøttkaker i brunsaus til middag!")
        self.message_entry.config(width=55)
        self.message_label = Label(self.msgGUI, text="Message: ",
                                   bg=self.backgroundColor)
        self.add_button = Button(self.msgGUI, text='Add', width=20, command=self.add_announcement)
        #self.see_button = Button(self.msgGUI, text='See Messages')

        self.type_label = Label(self.msgGUI, text="Select Message Type:", bg=self.backgroundColor)
        self.typeOptions = ["News", "Lunch", "Other"]

        self.currentType = StringVar(self.msgGUI)
        self.currentType.set("Other")  # default value
        self.TypeOptionsMenu = OptionMenu(self.msgGUI, self.currentType, *self.typeOptions)
        self.TypeOptionsMenu.config(width=10)

        #self.TypeOptionsMenu.grid(row=5, column=1, sticky=NW)

        self.msgExplanation.pack(pady=15)
        self.type_label.pack()
        self.TypeOptionsMenu.pack()
        Label(self.msgGUI, text=" ", bg=self.backgroundColor).pack()
        self.message_label.pack()
        self.message_entry.pack()
        self.add_button.pack(pady=5)

        self.msgGUI.protocol('WM_DELETE_WINDOW', self.msgGUI.destroy)

    # -----------------------------------------------------------------------------
    # ------------------ GUI for SEEING TODAYS ANNOUNCEMENT -----------------------
    # -----------------------------------------------------------------------------
    def see_announcements_pop_up(self):
        self.seeMsgGUI = Toplevel()
        self.seeMsgGUI.configure(background=self.backgroundColor)
        self.seeMsgGUI.resizable(width=True, height=True)
        self.seeMsgGUI.geometry('{}x{}'.format(1200, 500))
        self.seeMsgGUI.title('See Announcements')

        self.seeMsgExplanation = Label(self.seeMsgGUI,
                                    text="Todays announcements:",
                                    bg=self.backgroundColor, font="Verdana 9 bold")
        self.seeMsgExplanation.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        self.seeTypeLabel = Label(self.seeMsgGUI, text="Type:", bg=self.backgroundColor, font="Verdana 9 bold")
        self.seeMsgLabel = Label(self.seeMsgGUI, text="Message:", bg=self.backgroundColor, font="Verdana 9 bold")
        self.seeDeleteLabel = Label(self.seeMsgGUI, text="Delete:", bg=self.backgroundColor, font="Verdana 9 bold")
        self.seeTestLabel = Label(self.seeMsgGUI, text="Test:", bg=self.backgroundColor, font="Verdana 9 bold")
        self.seperatorLabel = Label(self.seeMsgGUI, text="-"*210,
                                    bg=self.backgroundColor, font="Verdana 9 bold")

        self.seeTypeLabel.grid(row=1, column=0, pady=5, padx=10)
        self.seeMsgLabel.grid(row=1, column=1, pady=5, padx=10)
        self.seeDeleteLabel.grid(row=1, column=2, pady=5, padx=10)
        self.seeTestLabel.grid(row=1, column=3, pady=5, padx=10)
        self.seperatorLabel.grid(row=2, column=0, columnspan=4, pady=3, padx=10, sticky=W)

        self.spacerExample = Label(self.seeMsgGUI, text="Example", bg=self.backgroundColor)
        self.spacerExample.grid(row=40, column=0, sticky=W, padx=20)
        self.spacerExample2 = Label(self.seeMsgGUI, text="|        " + "Here you see today's planned annoncements. "
                                                                       "You can listen to them by pressing the test button, or "
                                                                       "delete it by pressing delete.", bg=self.backgroundColor)
        self.spacerExample2.grid(row=40, column=1, sticky=W, padx=10)

        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d")

        self.todays_announcements = self.improvisation.get_all_announcements()

        self.tmpIDLabels = []
        self.tmpMessageLabels = []
        self.tmpTypeLabels = []
        self.tmpDeleteButtons = []
        self.tmpTestButtons = []

        if self.todays_announcements is not None:
            print("Is not none!")
            i = 0
            for row in self.todays_announcements:
                message = row[2]
                type = row[1]
                id = row[0]

                tmpTypeLabel = Label(self.seeMsgGUI, text=type, bg=self.backgroundColor)
                tmpMessageLabel = Label(self.seeMsgGUI, text="|        " + message, bg=self.backgroundColor)
                tmpIDLabel = Label(self.seeMsgGUI, text=id, bg=self.backgroundColor)

                tmpDeleteButton = Button(self.seeMsgGUI, text="Delete", command=partial(self.improvisation.delete_announcement, id))
                tmpTestButton = Button(self.seeMsgGUI, text="Test", command=partial(self.say, message))
                tmpDeleteButton.grid(row=i+3, column=2)
                tmpTestButton.grid(row=i+3, column=3)

                self.tmpDeleteButtons.append(tmpDeleteButton)
                self.tmpTestButtons.append(tmpTestButton)

                tmpTypeLabel.grid(row=i+3,column=0, sticky=W, padx=20)
                tmpMessageLabel.grid(row=i+3,column=1, sticky=W, padx=10)
                #tmpIDLabel.grid(row=i+2,column=,)

                self.tmpIDLabels.append(tmpTypeLabel)
                self.tmpMessageLabels.append(tmpMessageLabel)
                self.tmpTypeLabels.append(tmpIDLabel)

                i += 1
                self.tmpSeperatorLabel = Label(self.seeMsgGUI,
                                            text="-"*248,
                                               bg=self.backgroundColor)
                self.tmpSeperatorLabel.grid(row=i+3, column=0, columnspan=4, sticky=W, padx=10)
                i += 1
        else:
            self.spacerExampleA = Label(self.seeMsgGUI, text="Message", bg=self.backgroundColor)
            self.spacerExampleA.grid(row=3, column=0, sticky=W, padx=20)
            self.spacerExampleB = Label(self.seeMsgGUI,
                                        text="|        " + "No announcements are added for today.", bg=self.backgroundColor)
            self.spacerExampleB.grid(row=3, column=1, sticky=W, padx=10)
            self.tmpSeperatorLabel = Label(self.seeMsgGUI,
                                           text="-"*248,
                                           bg=self.backgroundColor)
            self.tmpSeperatorLabel.grid(row=4, column=0, columnspan=4, sticky=W, padx=10)

