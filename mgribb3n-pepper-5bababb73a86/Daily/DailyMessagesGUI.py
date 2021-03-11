import qi

#from GUI import *
from Tkinter import * # Import GUI elements from Tkinter package
from functools import partial
import time
import datetime


class DailyMessagesGUI(object):
    def __init__(self):
        """
        init
        :param session: qi session
        """

        self.backgroundColor = "#a8e6ff"

        # Create connection window
        self.msgGUI = Tk()
        self.msgGUI.resizable(width=False, height=False)
        self.msgGUI.geometry('{}x{}'.format(350, 300))
        self.msgGUI.configure(background=self.backgroundColor)
        self.msgGUI.title('Pepper Daily Messages')

        self.msgExplanation = Label(self.msgGUI, text="This messages will be told during the improvisation session!", bg=self.backgroundColor)
        self.message_entry = Entry(self.msgGUI)
        self.message_entry.insert(END, "Her kan du skrive en melding... Som for eksempel hva som er til lunsj i dag.")
        self.message_label = Label(self.msgGUI, text="Melding som skal sies under improvisasjon: ", bg=self.backgroundColor)
        self.add_button = Button(self.msgGUI, text='Add', command=partial(self.add_message))
        self.see_button = Button(self.msgGUI, text='See Messages', command=self.see_messages)

        self.type_label = Label(self.msgGUI, text="Select Message Type:", bg=self.backgroundColor)
        self.typeOptions = ["News", "Lunch","Other"]

        self.currentType = StringVar(self.msgGUI)
        self.currentType.set("Other")  # default value
        self.TypeOptionsMenu = OptionMenu(self.msgGUI, self.currentType, *self.typeOptions)
        self.TypeOptionsMenu.config(width=60)
        self.TypeOptionsMenu.grid(row=5, column=1, sticky=NW)

        self.msgExplanation.grid(row=0, column=0, pady=10)
        self.type_label.grid(row=1, column=0)
        self.message_entry.grid(row=3, column=0)
        self.message_label.grid(row=2, column=0)
        self.add_button.grid(row=4, column=0)
        self.see_button.grid(row=4, column=1)
        self.TypeOptionsMenu.grid(row=2, column=0)

        self.msgGUI.protocol('WM_DELETE_WINDOW', self.msgGUI.destroy)

        #self.msgGUI.mainloop()


    def add_message(self):
        print("")

    def see_messages(self):
        print("")

    def hide(self):
        self.msgGUI.withdraw()

    def show(self):
        self.msgGUI.update()
        self.msgGUI.deiconify()