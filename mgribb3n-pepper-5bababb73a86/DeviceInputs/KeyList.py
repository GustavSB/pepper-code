from pynput import keyboard


class KeyList:
    def __init__(self):
        self.dict = dict()
        self.__create_dict()

    def __create_dict(self):
        """
        Creates a dict() of the used keyboard keys.
        Binds them to a value that represents each one.
        See: KeyConfig text file for overview.
        """
        self.dict.update({None: 0})
        self.dict.update({keyboard.Key.up: 1})
        self.dict.update({keyboard.Key.down: 2})
        self.dict.update({keyboard.Key.left: 3})
        self.dict.update({keyboard.Key.right: 4})
        self.dict.update({keyboard.Key.f1: 5})
        self.dict.update({keyboard.Key.f2: 6})
        self.dict.update({keyboard.Key.f3: 7})
        self.dict.update({keyboard.Key.f4: 8})
