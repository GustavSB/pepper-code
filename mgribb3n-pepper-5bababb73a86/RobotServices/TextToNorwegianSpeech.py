# -*- coding: utf-8 -*-
from os import path as osPath  # Import path

class TextToNorwegianSpeech(object):
    def __init__(self, audioPlayer):
        self.audioPlayer = audioPlayer
        self.base_link_part1 = "http://code.responsivevoice.org/getvoice.php?t="
        self.base_link_part2v = "&tl=no&sv=g1&vn=&pitch=0.5&rate=0.42&vol=1"
        self.rate = 0.3
        self.filepath = osPath.dirname(osPath.realpath(__file__))

    def say(self, text, pitch=0.5, rate=0.41, vol=1):
        sentences = self.speech_control(text)
        for sentence in sentences:
            if sentence != '':
                self.audioPlayer.playWebStream(self.__get_audio_link(sentence, pitch, rate, vol), 1.0, 1.0)

    def __get_audio_link(self, text, pitch=0.5, rate=0.42, vol=1):
        return "http://code.responsivevoice.org/getvoice.php?t="\
               + text + "&tl=no&sv=g1&vn=&pitch="+ str(pitch) \
               +"&rate=" + str(self.rate) +"&vol=" + str(vol) + ""

    def speech_control(self, text):
        #print("TEXT:     " + text)

        # Seperate by dot
        text = text.replace(':','.').replace('!','.').replace('?','.')
        sentences = text.split(".")
        print(sentences)

        return sentences

    def changeRate(self, new_rate):
        self.rate = new_rate
        self.save_speech_rate()

    def get_previous_speech_rate(self):
        file = open(self.filepath + "/previousSpeechRate.txt", "r")
        tmp = float(file.read().strip())
        file.close()
        return tmp

    def save_speech_rate(self):
        with open(self.filepath + "/previousSpeechRate.txt", 'w') as file:
            file.write(str(self.rate))