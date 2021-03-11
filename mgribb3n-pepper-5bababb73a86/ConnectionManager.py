import qi

#from GUI import *
from Tkinter import * # Import GUI elements from Tkinter package
from functools import partial

from Connector import Connector


class ConnectionManager(object):
    def __init__(self):
        """
        init
        :param session: qi session
        :param language: synth language
        """
        self.language = "Norwegian"
        self.backgroundColor = "#a8e6ff"

        # Create connection window
        self.connection_window = Tk()
        self.connection_window.resizable(width=False, height=False)
        self.connection_window.geometry('{}x{}'.format(420, 300))
        self.connection_window.configure(background=self.backgroundColor)
        self.connection_window.title('Pepper Connetion - NTNU')

        self.ip_entry = Entry(self.connection_window)
        self.ip_entry.insert(END, "")
        self.port_entry = Entry(self.connection_window)
        self.port_entry.insert(END, "")
        self.ip_entry.insert(END, "192.168.0.101")
        self.port_entry.insert(END, "9559")

        connection_label = Label(self.connection_window, text="Checklist for connecting to Pepper: ", bg=self.backgroundColor)
        check1 = Label(self.connection_window, text=" - Check that computer is connected to correct network!", bg=self.backgroundColor)
        check2 = Label(self.connection_window, text=" - Check if IP-address is correct: ", bg=self.backgroundColor)

        connect_button = Button(self.connection_window, text='Connect', command=partial(self.connect))

        close_button = Button(self.connection_window, text='Close', command=self.close)

        self.connection_mode = StringVar()
        self.connection_mode.set("Simu")

        connection_label.grid(row=9, column=0, columnspan=3, sticky=W)
        check1.grid(row=10, column=0, columnspan=4, sticky=W)
        check2.grid(row=11, column=0, columnspan=4, sticky=W)


        Label(self.connection_window, text="  ", bg=self.backgroundColor).grid(row=0, column=0)
        Label(self.connection_window, text="  ", bg=self.backgroundColor).grid(row=1, column=0)
        Label(self.connection_window, text="  ",bg=self.backgroundColor).grid(row=1, column=1)
        Label(self.connection_window, text="  ",bg=self.backgroundColor).grid(row=5, column=1)
        Label(self.connection_window, text="  ",bg=self.backgroundColor).grid(row=8, column=0)
        Label(self.connection_window, text="  ",bg=self.backgroundColor).grid(row=12, column=0)

        Label(self.connection_window, text="IP Address: ", bg=self.backgroundColor).grid(row=2, column=1)
        Label(self.connection_window, text="Port: ", bg=self.backgroundColor).grid(row=2, column=3)
        self.ip_entry.grid(row=3, column=1)
        self.port_entry.grid(row=3, column=3)
        connect_button.grid(row=6, column=1)
        close_button.grid(row=6, column=3)

        self.languageLabel = Label(self.connection_window, text="Choose speech language: ",bg=self.backgroundColor)
        self.languageToggle = Button(self.connection_window, text="Norwegian", width=12, relief="raised",
                                       command=self.language_toggle)
        #self.languageToggle.grid(row=14, column=1, columnspan=3, sticky=W)
        #self.languageLabel.grid(row=13, column=1, columnspan=3, sticky=W)


        self.connection_window.protocol('WM_DELETE_WINDOW', self.connection_window.destroy)

        self.connection_window.mainloop()

    def close(self):
        """

        :return:
        """
        print("Close")

    def connect(self):
        """

        :return:
        """
        robot_IP = self.ip_entry.get()
        robot_port = self.port_entry.get()
        self.connect_to_robot(robot_IP, robot_port)

    def connect_to_robot(self, ip, port):
        """
        Connects to the real robot
        :param ip:
        :param port:
        :return:
        """
        print("Connect to robot")
        # Connect to real robot
        #  NaoQi / qi : init qi session and ALMemory service
        try:
            session = qi.Session()
            session.connect(ip + ":" + port)
            print("Connected")
        except RuntimeError:
            print("Connection Problem!")
            sys.exit(1)

        self.connection_window.withdraw()
        self.connector = Connector(session, self.language, self.ip_entry.get())

    def language_toggle(self):
        if self.languageToggle.config('relief')[-1] == 'sunken':
            self.languageToggle.config(relief="raised", text="Norwegian")
            self.language = "Norwegian"
        else:
            self.languageToggle.config(relief="sunken", text="English")
            self.language = "English"


        '''
        # Start sessions
        tts = session.service("ALMotion")
        postureProxy = session.service("ALRobotPosture")
        text_to_speech_service2 = TextToSpeech(session)  # session.service("ALTextToSpeech")

        # Create object of AutonomousLifeControllerModule
        autLife = AutonomousLifeControllerModule(session)

        # Create object of AwarenessControllModule
        awContr = AwarenessControllerModule(session)

        # Turn of all autonomous abilities and awareness. To hold positions.
        autLife.set_all_autonomous_abilities(False, False, False, False)
        awContr.set_basic_awareness(False)

        self.connection_window.withdraw()
        #self.connection_window.destroy()
        GUI(tts, postureProxy, text_to_speech_service2)
        '''

