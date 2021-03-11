"""
Source: https://pypi.python.org/pypi/pynput
Code is based on examples found in the given link.
"""
from pynput import keyboard
from pynput.keyboard import Controller as KeyboardSimulator
from KeyList import KeyList
from threading import Thread
from RobotCommands import RobotCommands


class KeyboardController:
    def __init__(self, session, pepperController):
        self.key_pressed = 0
        self.stop_signal = False
        self.key_list = KeyList()
        self.commands = RobotCommands(session, pepperController)
        self.keyboard_sim = KeyboardSimulator()

        "Code was changed and re-written 15.12.2017 - changes: keyboard simulator and command thread."
        "TODO: Has to be tested to see whether it works with a GUI."

        "TODO: Introduce a flag so that only 1 key can be pressed at a time. So that the first key pressed has to be" \
            " released before another can be pressed - to reduce clunkiness"

        "Note: Threads should probably be paused and not stopped and re-started. Probably does not matter since it" \
            " won't be so frequently used"

    def start(self):
        """ Starts everything, listener and command_thread"""
        self.__reset_command_loop()
        self.__start_listener_thread()
        self.__start_command_thread()

    def stop(self):
        """
        Simulates an Key.esc button press to stop the listener.
        Stops the listener and command_thread.
        """
        self.keyboard_sim.press(keyboard.Key.esc)
        self.keyboard_sim.release(keyboard.Key.esc)

    def on_press(self, key):
        """
        Callback function - for a button press
        """
        try:
            # print('special key {0} pressed'.format(key))
            self.__check_key(key)
        except AttributeError:
            pass
            # print('alphanumeric key {0} pressed'.format(key.char))

    def on_release(self, key):
        """
        Callback function - for a button release
        """
        # print('{0} released'.format(key))
        self.__reset_key()
        if key == keyboard.Key.esc:
            self.__stop_listener()

    def __check_key(self, key):
        """
        Checks if the key pressed is a "registered" key in key_list.
        Return the value representing the key if it does.
        """
        self.key_pressed = self.key_list.dict.get(key)

    def __do_command(self):
        """ Work function for command_worker thread"""
        while not self.stop_signal:
            self.commands.do_command(self.key_pressed)

    def __stop_listener(self):
        """ Stops the keyboard listener (+ command_thread), has to be called within the listener instance (callbacks)"""
        self.__stop_command_loop()
        keyboard.Listener.stop

    def __start_listener_thread(self):
        """ Starts the keyboard listener """
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

    def __start_command_thread(self):
        """ Starts the command thread"""
        command_thread = Thread(target=self.__do_command)
        command_thread.start()

    def __reset_key(self):
        """ Reset the key value to 0 - which is stop command"""
        self.key_pressed = 0

    def __stop_command_loop(self):
        """ Stop signal for command thread loop"""
        self.stop_signal = True

    def __reset_command_loop(self):
        """ Reset signal for command thread loop"""
        self.stop_signal = False





