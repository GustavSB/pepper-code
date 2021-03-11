from os import path as osPath  # Import path
import pandas as pd
import datetime



class ExerciseStats():
    def __init__(self, folder="exercises/", file="exerciseStats.csv"):

        self.filepath = osPath.dirname(osPath.realpath(__file__))
        self.exercise_folder = self.filepath + "/" + folder
        self.folder = folder
        self.file = file


    def get_exercise_stats(self, exercise_number):
        path = self.exercise_folder + "" + self.file
        tmp = pd.DataFrame.from_csv(path, index_col=0)

        duration, last_played = list(tmp.loc[exercise_number])[1:]

        return duration, last_played


    def update_exercise_stats(self, exercise_number):
        path = self.exercise_folder + "" + self.file
        tmp = pd.DataFrame.from_csv(path)

        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d")

        tmp.set_value(exercise_number, "Last Played", now)

        tmp.to_csv(path)

