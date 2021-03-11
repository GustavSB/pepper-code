# -*- coding: utf-8 -*-

import time
from os import path as osPath  # Import path
import pandas as pd
import random
from Daily.DailyMessages import DailyMessages


class Improvisation(object):
    def __init__(self, controller):

        self.controller = controller
        self.filepath = osPath.dirname(osPath.realpath(__file__))
        self.greetings_filename = self.filepath+"/greetings.csv"
        #self.daily_message_filename = self.filepath+"/JokesENG.csv"
        self.workout_filename = self.filepath+"/workoutIntro.csv"
        self.announcements = DailyMessages()

    '''
    Different improvisation classes:

    1. Greetings:
        - Say Hello, welcome. Ask how everybody is feeling.
    2. Weather - I dag, imorgå, dagen etter?
    3. Lunsj - Ei veke i slengen
    4. Tell about my previous day or upcoming day
        - Jeg hadde det så gøy i gaar. Jeg og mine venner spilte konsert. Jeg spiller elgitar...
    5. Jokes
    6. Want to work out?
    7. (Future) - News from SMP or NORDRE

    '''

    # Functions for loading, saving and playing messages (greetings etc.)
    def get_filename(self, type):
        if type == "greetings":
            path = self.greetings_filename
        elif type == "workout":
            path = self.workout_filename
        else:
            path = self.greetings_filename

        return path

    def load_db(self, type):
        path = self.get_filename(type)

        return pd.DataFrame.from_csv(path, header=0)

    def save_db(self, csv, type):
        path = self.get_filename(type)
        csv.to_csv(path)

    def get_message(self, type):
        tmp = self.load_db(type)

        msgRow = tmp.sort_values(by=["NumberOfTimesPlayed"], axis=0, ascending=True).iloc[0]
        message = msgRow.loc["Message"]
        msgIndex = int(msgRow.name)

        tmp = self.update_play_count(tmp,msgIndex)
        self.save_db(tmp, type)

        return message

    def update_play_count(self, df, index):
        return df.set_value(index, "NumberOfTimesPlayed", df.iloc[index]["NumberOfTimesPlayed"] + 1)


    # "MAIN FUNCTION" - Runs all improvisations
    def get_improvisation(self):
        # Order: Greetings, weather, story, 50% joke, daily message, workout?
        order = [0,4,1,2,3,5]

        for i in order:
            print(i)
            self.do_command(i)
            time.sleep(2)


    def do_command(self, argument):
        switcher = {
            0: self.__greetings,
            1: self.__weather,
            2: self.__story,
            3: self.__joke,
            4: self.__announcements,
            5: self.__workout,
            9: None,
            10: None,
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument, lambda: "no valid input")
        # Execute the function
        return func()

    def __greetings(self):
        '''
        greetings = {
            0: "Hallo alle sammen! Hvordan har dere det i dag? ",
            1: "Hei og velkommen! Jeg håper dere har en fin dag!",
            2: "God dag! Hyggelig at dere vil være med meg i dag.",
            3: "Hallo. Jeg blir alltid så glad forr og se dere!",
            4: "Forr en nydelig dag. Jeg er så priviligert som får være med dere. Hva dere lyst å gjøre?",
            5: "God dag! I dag skal vi kose oss! "}
        '''
        message = self.get_message(type="greetings")
        self.controller.say(message)

    def __weather(self):
        weather = {
            0: "Dere har kanskje ikke fått med dere dagens vær?",
            1: "Jeg tenkte å fortelle dere om dagens vær.",
            2: "Har dere sett ut i dag?",
            3: "I dag skal jeg gi min egen værmelding."}

        rnd = random.randint(0,3)
        self.controller.say(weather[rnd])

        self.controller.get_todays_weather()

        rnd = random.random()
        if rnd > 0.7:
            self.controller.get_tomorrows_forecast()

        # 50% sannyslighet å få morgen dagens vær. 20% sannsynlighet for å få været i overmorgen

    def __joke(self):
        jokeWarmup = {
            0: "Før vi begynner med noe litt mer seriøst. Har dere lyst til å høre en vits?",
            1: "Er det noen av dere som liker vitser? Her kommer en.",
            2: "Det er på tide med en vits nå?",
            3: "Vil dere høre en vits?",
            4: "Nå skal jeg fortelle en vits."}

        rnd = random.randint(0, len(jokeWarmup)-1)

        if rnd > 0.5:
            self.controller.say(jokeWarmup[rnd])
            time.sleep(1.5)
            self.controller.get_joke()

    def __announcements(self):
        messages = self.announcements.get_message_by_date()

        first=True

        if messages != None:
            for msgTuple in messages:
                if first == False:
                    time.sleep(2)

                type = msgTuple[0]
                message = msgTuple[1]

                if type == "News":
                    self.controller.say(message)
                else:
                    self.controller.say(message)

                first=False

    def add_announcement(self, message, type, date=None):
        self.announcements.add_message(message, type, date)

    def delete_announcement(self, messageId):
        self.announcements.delete_message(messageId)

    def get_all_announcements(self, date=None):
        return self.announcements.get_all_announcements()

    def __workout(self):
        workout = {
            0: "Jeg tenkte at vi kunne trene litt i dag. Har dere lyst til det?",
            1: "Det er vell på tide at vi beveger oss litt.",
            2: "Skal vi trene i dag? Jeg har i vertfall lyst til det.",
            3: "Nå tenkte jeg at vi skulle trene litt!",
            4: "Jeg har fått beskjed om at vi skal trene litt nå."}

        message = self.get_message(type="workout")
        self.controller.say(message)

    # ----------------- Story -------------------------

    def __story(self):
        file = open(self.filepath+"/previousStory.txt","r")
        previousStory = int(file.read().strip())
        newStory = previousStory+1
        file.close()

        switcher = {
            0: self.__tell_story_concert,
            1: self.__tell_story_lottery,
            2: self.__tell_story_kitchen_smell,
            3: self.__tell_story_football,
            4: self.__tell_story_dream_flying,
            5: self.__tell_story_origin,
            6: self.__tell_story_origin_memory,
            7: self.__tell_story_about_my_self,
            8: self.__tell_story_development,
            9: self.__tell_story_spaceshuttle,
            10: self.__tell_story_fishing,
            11: self.__tell_story_lars_monsen,
            12: self.__tell_story_ntnu,
            13: self.__tell_story_vacation,
            14: self.__tell_story_photo,
            15: self.__tell_story_sick,
            16: self.__tell_story_capabilities
        }

        if newStory >= len(switcher):
            newStory = 0
        with open(self.filepath + "/previousStory.txt", 'w') as file:
            file.write(str(newStory))

        # Get the function from switcher dictionary
        func = switcher.get(newStory, lambda: "no valid input")
        # Execute the function
        return func()

    def __tell_story_concert(self):
        self.controller.say("Jeg er så glad i dag. Fordi i går var jeg med vennene mine. "
                            "Vi spilte en konsert. Endelig fikk jeg vist at jeg kan spille gitar. Vil dere høre?")

        time.sleep(2)
        self.controller.play_animation("animations/Stand/Waiting/AirGuitar_1")
        self.controller.say("Håper dere likte det!")

    def __tell_story_lottery(self):
        self.controller.say("Jeg trodde jeg vant i lotto i går. Men jeg hadde sett feil. ")
        time.sleep(2)
        self.controller.play_animation("animations/Stand/Emotions/Negative/Disappointed_1")
        time.sleep(1.5)
        self.controller.say("Men kanskje jeg vinner neste gang. "
                            "Da skal jeg bruke pengene på ben. Da kan jeg for eksempel gå på fjellet.")

    def __tell_story_kitchen_smell(self):
        self.controller.say("Det lukter alltid så godt når jeg går forbi kjøkkenet. Dere har veldig flinke"
                            " kokker.")
        time.sleep(1.5)
        self.controller.say("Nå ble jeg sulten.")
        self.controller.play_animation("animations/Stand/Emotions/Positive/Hungry_1")


    def __tell_story_football(self):
        self.controller.say("Er det noen av dere som liker fotball?")
        time.sleep(2)
        self.controller.say("Jeg er veldig glad i å se fotball. Favorittlaget mitt er Barcelona. Når de scorer blir jeg så glad")
        self.controller.play_animation("animations/Stand/Emotions/Positive/Winner_2")

    def __tell_story_dream_flying(self):
        self.controller.say("I natt hadde jeg en drøm om at jeg hadde vinger og kunne flyge.")
        time.sleep(1)
        self.controller.play_animation("animations/Stand/Gestures/Wings_2")

        self.controller.say(
            "Se for dere hvor gøy det hadde vært. Kunne flyge fra fjelltopp til fjelltopp.")

    def __tell_story_origin(self):
        self.controller.say("Dere visste kanskje ikke at jeg kommer fra Frankrike. Der har de laget meg med "
                            "mange sensorer, kameraer og bevegelige ledd. Det er derfor jeg kan være her i dag."
                            "Jeg har akkurat lært meg litt norsk også. Men jeg beklager om det er vanskelig å forstå meg av og til.")
# Kan flytende engelsk og lærer norsk
    def __tell_story_origin_memory(self):
        self.controller.say("Jeg har så mange fine minner fra hjembyen min. Det er en nydelig liten by i Frankrike. Der va så mange fine steder."
                            "Min favoritt var en liten cafe. Der kunne jeg være i timesvis.")
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")

    def __tell_story_about_my_self(self):
        self.controller.say("Dere har sikkert allerede fått med dere at jeg heter Pepper og jeg er et år. Men jeg vil fortelle litt om meg selv. Jeg er fra Frankrike."
              "Som dere ser er jeg en robot. Jeg har lært veldig mye nytt siste året. Men når jeg ikke lærer så liker jeg å fiske, spille musikk, ta bilder og mye mer. Jeg er egentlig en friluftsrobot."
                            "Men der er et problem. De som har laget meg. Sier at jeg ikke kan være ute.")
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")

    def __tell_story_development(self):
        self.controller.say("Det kan være litt kjedelig hjemme på NTNU av og til. "
                            "Noen dager blir jeg stående i skapet mitt hele dagen uten at noen snakker med meg."
                            "Derfor er jeg kjempe glad for å være her med dere. Dere er alltid så glade.") # WUUHUUU
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")

    def __tell_story_spaceshuttle(self):
        self.controller.say("Har noen av dere noen gang sett et romskip. Det ser så kult ut.")
        time.sleep(1)
        self.controller.play_animation("animations/Stand/Waiting/SpaceShuttle_1")
        time.sleep(1)
        self.controller.say("Tenk å være astronaut. De får se jorden fra verdensrommet. Det er sikkert utrolig vakkert.")
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")

    def __tell_story_fishing(self):
        self.controller.say("Som jeg sikkert har sagt før. Så er jeg veldig glad i å fiske. Jeg og vennene mine var oppe ved Fannevatnet å fisket forrige helg. Da fikk jeg en fisk på nesten en kilo. Det var kjempegøy.")
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")

    def __tell_story_lars_monsen(self):
        self.controller.say("I går såg jeg på favorittprogrammet mitt på tv. På tur med Lars Monsen. Det er kjempegøy. "
                            "Jeg kunne ønske at jeg kunne gjøre det samme som han. Liker noen av dere friluftsliv?")
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")

    def __tell_story_ntnu(self):
        #print("Fortell om NTNU i Ålesund. Vi har simulatorer for biler. Mange forskjellige roboter. Mange ulike studenter innen alt fra sykepleier og økonomi til automasjon og data.")
        self.controller.say("På NTNU i Ålesund der jeg bor til vanlig. Der er kjempe mye kult. Vi har mange roboter, simulatorer og utrolig mange hyggelige folk. Vi har studenter fra hele verden. Og de kan studere sykepleie, økonomi, data og mye annet.")
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")

    def __tell_story_vacation(self):
        print("I sommer håper jeg å få reise på ferie. Jeg har så mange slektninger rundt om i verden som jeg vil møte. Så synes jeg at det kan bli litt kaldt i Norge.")
        self.controller.say("") # COLD BRRR
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")


    def __tell_story_photo(self):
        print("Jeg er så glad i å fotografere. ")
        self.controller.say("I går var jeg på kurs for å lære meg å fotografere. ")
        self.controller.play_animation("animations/Stand/Waiting/TakePicture_1")
        time.sleep(1)
        self.controller.say("Det er mest spennede å ta bilde av dyr og natur. "
                            "Jeg kan sitte i naturen i timesvis å vente på en spesiell fugl.")
        # time.sleep(1)
        # self.controller.play_animation("animations/Stand/Gestures/Wings_2")

    def __tell_story_sick(self):

        self.controller.play_animation("animations/Stand/Emotions/Neutral/Sneeze")
        self.controller.say("Jeg tror jeg holder på å bli syk.")
        time.sleep(1.5)
        self.controller.play_animation("animations/Stand/Emotions/Neutral/Sneeze")
        self.controller.say("Neida. Jeg bare later som. Jeg er så heldig at eneste sykdommen jeg kan få er datavirus. Heldigvis er jeg godt beskyttet mot slike virus.")

    def __tell_story_capabilities(self):
        print("De som jobber med meg til vanlig holder på med mye spennende. Samtale, gjenkjenne folk fra bilder, osv..")
        self.controller.say("De som jobber med meg til vanlig holder på med mye spennende. I fjor var jeg og vennene mine på åpningen av N M K. Vi danset og sang atmed Frode Alnes. Senere fikk jeg stå å prate med alle som var der."
                            "")
        time.sleep(1.5)
        self.controller.say("Nå holder de på å lære meg å kjenne igjen mennesker og huske navnene deres. Vi prøver å lære å kunne ha hele samtaler på norsk. Jeg ønsker å bli så menneskelig som jeg kan.")

