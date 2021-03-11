# -*- coding: utf-8 -*-

import random
import pandas as pd
import time

from os import path as osPath  # Import path

class JokeGenerator(object):
    """
    Weather services super class / interface
    """
    def __init__(self, language, tts, ttsNOR):
        self.language = language
        self.filepath = osPath.dirname(osPath.realpath(__file__))
        self.filename = self.get_filename()
        self.jokeBase = pd.DataFrame.from_csv(self.filename, header=0)
        self.tts = tts
        self.ttsNOR = ttsNOR

    def get_filename(self):
        if self.language == "English":
            filename = self.filepath+"/JokesENG.csv"
        else:
            filename = self.filepath+"/JokesNOR.csv"

        return filename



    def load_jokes(self):
        self.jokeBase = pd.DataFrame.from_csv(self.filename, header=0)

    def save_jokes(self):
        self.jokeBase.to_csv(self.filename)

    def get_joke(self):
        if self.language == "English":
            self.load_jokes()

            jokeRow = self.jokeBase.sort_values(by=["NumberOfTimesPlayed"], axis=0, ascending=True).iloc[0]
            joke = jokeRow.loc["Joke"]
            jokeIndex = int(jokeRow.name)

            self.update_play_count(jokeIndex)
            self.save_jokes()

            self.tts.say(joke)

        else:
            # Tell a joke:
            self.__norwegian_joke()




    def update_play_count(self, index):
        self.jokeBase.set_value(index, "NumberOfTimesPlayed", self.jokeBase.iloc[index]["NumberOfTimesPlayed"]+1)

    def __norwegian_joke(self):
        file = open(self.filepath + "/previousJoke.txt", "r")
        previousJoke = int(file.read().strip())
        print(previousJoke)
        newJoke = previousJoke + 1
        file.close()

        switcher = {
            0: self.__joke_1,
            1: self.__joke_2,
            2: self.__joke_3,
            3: self.__joke_4,
            4: self.__joke_5,
            5: self.__joke_6,
            6: self.__joke_7,
            7: self.__joke_8,
            8: self.__joke_9,
            9: self.__joke_10,
            10: self.__joke_11,
            11: self.__joke_12,
            12: self.__joke_13,
            13: self.__joke_14,
            14: self.__joke_15,
            15: self.__joke_16,
            16: self.__joke_17,
            17: self.__joke_18,
            18: self.__joke_19
        }

        if newJoke >= len(switcher):
            newJoke = 0

        with open(self.filepath + "/previousJoke.txt", 'w') as file:
            file.write(str(newJoke))

        # Get the function from switcher dictionary
        func = switcher.get(newJoke, lambda: "no valid input")
        # Execute the function
        return func()

    def __joke_1(self):
        self.ttsNOR.say("Lille Per kommer hjem fra svømming med kloremerker på hele ryggen. Mor utbryter:")
        self.ttsNOR.say("Men hvordan du ser ut gutten min!", pitch=0.4, rate=0.40, vol=1)
        self.ttsNOR.say("Hvordan har dette skjedd?", pitch=0.4, rate=0.40, vol=1)
        self.ttsNOR.say("Det var så mye klor i vannet!", pitch=0.6, rate=0.40, vol=1)

    def __joke_2(self):
        self.ttsNOR.say("Det var et møte mellom presidenten i USA og presidenten i same tinget.")
        time.sleep(1)
        self.ttsNOR.say("Presidenten i USA hilste på han og sa:")
        time.sleep(1)
        self.tts.say("I am the president of The United States?")
        time.sleep(1)
        self.ttsNOR.say("Da sa presidenten av same tinget.")
        time.sleep(1)
        self.tts.say("I am pleased to meet you! I am the president of the same thing.")

    def __joke_3(self):
        self.ttsNOR.say("Vet noen av dere hvorfor svenskene har et kkålhode i hanskerommet?")
        time.sleep(4)
        self.ttsNOR.say("Fordi de bruker det som legitimasjon!")

    def __joke_4(self):
        self.ttsNOR.say("Vet dere hva moren til Pinoccio var?")
        time.sleep(4)
        self.ttsNOR.say("Trebarnsmor!")

    def __joke_5(self):
        self.ttsNOR.say("Hva kalles en tannlege som er veldig forsiktig i arbeidet sitt?")
        time.sleep(4)
        self.ttsNOR.say("Tannpirker!")

    def __joke_6(self):
        self.ttsNOR.say("Hva står skrevet under alle flaskene i Sverige?")
        time.sleep(4)
        self.ttsNOR.say("Åpnes i andre enden!")

    def __joke_7(self):
        self.ttsNOR.say("Det var en gang en mann som skulle opptre men så voknet han 4.", rate=0.37)


    def __joke_8(self):
        self.ttsNOR.say("En nordmann, en svenske og en danske gikk inn på en bar. Da bryter det ut fra en bartender.")
        time.sleep(0.5)
        self.ttsNOR.say("Er dette en vits?", pitch=0.4)

    def __joke_9(self):
        self.ttsNOR.say("Jeg kjøpte meg en kortstokk i går, men jeg måtte levere den tilbake. Fordi da jeg kom hjem fant jeg ut at 4 av kortene var knekt.")


    def __joke_10(self):
        self.ttsNOR.say("En prest gikk tur i skogen for å beundre skaperverket. Han ble plutselig angrepet av en rasende, sulten bjørn.")
        time.sleep(0.5)
        self.ttsNOR.say("Presten kastet seg på kne, foldet hendene og bad.")
        self.ttsNOR.say("Kjære Gud. La denne bjørnen bli kristen!", pitch=0.54, rate=0.40, vol=1)
        self.ttsNOR.say("Plutselig hørte han en stemme over seg.")
        self.ttsNOR.say("O, du som metter liten fugl, velsign vår mat, O Gud.", pitch=0.4, rate=0.40, vol=1)

    def __joke_11(self):
        self.ttsNOR.say("Bestemor til barnebarnet:", pitch=0.5)
        self.ttsNOR.say("Når jeg hoster holder jeg en hånd for munnen. Det må du også lære deg!", pitch=0.47)
        self.ttsNOR.say("Det trenger jeg vel ikke. Mine tenner sitter jo fast.", pitch=0.6)

    def __joke_12(self):
        self.ttsNOR.say("På biltur over Hardangervidda fikk familiens yngste for første gang øye på et reinsdyr.", pitch=0.50)
        self.ttsNOR.say("Se! Ei ku med TV antenne.", pitch=0.58)

    def __joke_13(self):
        self.ttsNOR.say("Er det noen som vet hvorfor blomstrene til elektrikeren ikke vokser?")
        time.sleep(4)
        self.ttsNOR.say("Det er på grunn av jordfeil.")

    def __joke_14(self):
        self.ttsNOR.say("Vet dere hvilket sjøpatterdyr som er mest opptatt av HMS?")
        time.sleep(4)
        self.ttsNOR.say("Sikkerhetsseelen.")

    def __joke_15(self):
        self.ttsNOR.say("Hva er forskjellen mellom en snømann og en snødame?")
        time.sleep(4)
        self.ttsNOR.say("Snøballer.")

    def __joke_16(self):
        self.ttsNOR.say("Småskolen skulle avslutte før jul med et stort julespill som alle var svært opptatt av.")
        self.ttsNOR.say("Men en dag kom lille Anders hjem og var aldeles utrøstelig. Han sa:")
        self.ttsNOR.say("Nå blir det ikke noe av julespillet i det hele tatt. Josef har fått kusma. Og en av englene skal til bestemoren sin i Bergen.", pitch=0.6)

    def __joke_17(self):
        self.ttsNOR.say("Sjefen til de nyansatte:")
        self.ttsNOR.say("Det er to ting som er svært viktig her i firmaet. Punkt 1 er renslighet.", pitch=0.45)
        time.sleep(0.5)
        self.ttsNOR.say("Forresten. Tørket dere alle av dere skoene på mattten utenfor døren?", pitch=0.45)
        self.ttsNOR.say("Ja svarte alle.")
        self.ttsNOR.say("Bra!", pitch=0.45)
        self.ttsNOR.say("Punkt 2 er ærlighet. Det finnes ingen matte utenfor døren.", pitch=0.45)

    def __joke_18(self):
        self.ttsNOR.say("En nervøs fabrikkarbeider viser kongen rundt i majonesfabrikken:")
        self.ttsNOR.say("Og her lager vi majestet, deres majones.", pitch=0.55)
        time.sleep(0.5)

    def __joke_19(self):
        self.ttsNOR.say("En politimann tok fartskontroll. Han kjedet seg veldig fordi ingen kjørte for fort.")
        self.ttsNOR.say("Plutselig kom det en som kjørte for fort. Politimannen stoppet han og sa:")
        self.ttsNOR.say("Jeg har ventet lenge på deg!", pitch=0.40)
        self.ttsNOR.say("Mannen svarte kjapt:")
        self.ttsNOR.say("Jeg kom så fort jeg kunne!", pitch=0.45)
