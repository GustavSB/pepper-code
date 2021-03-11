# -*- coding: utf-8 -*-

import time
import pandas as pd
from os import path as osPath  # Import path
import datetime

class DailyMessages(object):
    def __init__(self):
        self.folder_path = osPath.dirname(osPath.realpath(__file__))
        self.full_path = self.folder_path + "/dailyMessages.csv"
        self.messageBase = pd.DataFrame.from_csv(self.full_path, header=0)

    def get_message(self, delete=False):
        msgRow = self.messageBase.sort_values(by=["Date"], axis=0, ascending=True).iloc[0]
        message = msgRow.loc["Message"]
        type= msgRow.loc["Type"]
        msgIndex = int(msgRow.name)

        if delete == True:
            print("Delete message")
        return message



    def get_message_by_type(self, type, delete=False):
        message = self.messageBase.loc[self.messageBase["Type"] == type]

        if delete == True:
            print("Delete message")

        if len(message) == 0:
            returnMessage = None
        elif len(message) == 1:

            returnMessage = [(message.iloc[0]["Type"], message.iloc[0]["Message"])]
        else:
            returnMessage = []
            for i in range(0, len(message)):
                returnMessage.append((message.iloc[0]["Type"], message.iloc[0]["Message"]))

        return returnMessage

    def get_message_by_date(self, date=None):
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d")

        message = self.messageBase.loc[self.messageBase["Date"]==now]

        if len(message) == 0:
            returnMessage = None
        elif len(message) == 1:

            returnMessage = [(message.iloc[0]["Type"], message.iloc[0]["Message"])]
        else:
            returnMessage = []
            for i in range(0,len(message)):
                returnMessage.append((message.iloc[0]["Type"], message.iloc[0]["Message"]))

        return returnMessage

    def add_message(self, message, type, date=None):
        if date == None:
            date = datetime.datetime.now()
            date = date.strftime("%Y-%m-%d")

        message = message.replace(",",".")

        number_id = self.get_next_available_number()
        self.messageBase.loc[number_id] = [date, type, message, 0]
        self.messageBase.to_csv(self.full_path)

    def delete_message(self, messageID):
        if messageID in self.messageBase.index:
            self.messageBase = self.messageBase.drop([messageID])
            self.messageBase.to_csv(self.full_path)

    def get_next_available_number(self):
        return self.messageBase.index.max()+1

    def get_all_announcements(self):
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d")

        message = self.messageBase.loc[self.messageBase["Date"] == now]

        print(message)

        if len(message) == 0:
            returnMessage = None
        elif len(message) == 1:

            returnMessage = [(message.iloc[0].name, message.iloc[0]["Type"], message.iloc[0]["Message"])]
        else:
            returnMessage = []
            for i in range(0, len(message)):
                returnMessage.append((message.iloc[i].name,message.iloc[i]["Type"], message.iloc[i]["Message"]))

        return returnMessage