class TextToSpeech(object):
    def __init__(self, session, language="English"):
        """
        init
        :param session: qi session
        :param language: synth language
        """
        self.animated_text_to_speech_service = session.service("ALAnimatedSpeech")
        self.text_to_speech_service = session.service("ALTextToSpeech")
        self.text_to_speech_service.setLanguage(language)
        self.speaking_flag = False

    # Public: The sentence you pass to this method will be spoken by the robot.
    def say(self, sentence):
        if sentence is not None:
            self.speaking_flag = True
            self.text_to_speech_service.say(sentence)
            self.speaking_flag = False

    # Public: The sentence you pass to this method will be spoken by the robot, async.
    def say_async(self, sentence):
        if sentence is not None:
            self.speaking_flag = True
            self.text_to_speech_service.say(sentence, _async=True)
            self.speaking_flag = False

    # Public: The sentence you pass to this method will be spoken by the robot.
    # Will also run animation while speaking.
    def say_animated(self, sentence):
        if sentence is not None:
            self.speaking_flag = True
            self.animated_text_to_speech_service.say(sentence)
            self.speaking_flag = False

    # Public: The sentence you pass to this method will be spoken by the robot, async.
    # Will also run animation while speaking.
    def say_animated_async(self, sentence):
        if sentence is not None:
            self.speaking_flag = True
            self.animated_text_to_speech_service.say(sentence, _async=True)
            self.speaking_flag = False


    # Public: The sentence you pass to this method will be spoken by the robot.
    # Will run animation if the word count of the sentence is above the threshold.
    def say_smart(self, sentence, smart_word_thresh=3):
        if sentence is not None:
            if len(sentence.split()) > smart_word_thresh:
                self.say_animated(sentence)
            else:
                self.say(sentence)

    # Public: Returns if the robot is speaking or not.
    def speaking(self):
        return self.speaking_flag
    # Setters

    # Public: Sets the volume of the text to speech.
    # Use a volume between 0.0 - 2.0
    # It is not recommended to use a volume over 1.0
    # Default volume 1.0
    def set_volume(self, volume):
        self.text_to_speech_service.setVolume(volume)

    # Public: Sets the speed of the text to speech.
    # Use a value between 50 - 400
    # Default value 100
    def set_voice_speed(self, value):
        self.text_to_speech_service.setParameter("speed", value)

    # Public: Sets the default voice speed of the text to speech.
    # Use a value 50 - 400
    # Default value 100
    def set_default_voice_speed(self, value):
        self.text_to_speech_service.setParameter("defaultVoiceSpeed", value)

    # Public: Sets the double voice level of the text to speech.
    # Use a value 0.0 - 4.0
    # Default value 100
    def set_double_voice_level(self, value):
        self.text_to_speech_service.setParameter("doubleVoiceLevel", value)

    # Public: Sets the double voice time shift of the text to speech.
    # Use a value 0.0 - 0.5
    def set_double_voice_time_shift(self, value):
        self.text_to_speech_service.setParameter("doubleVoiceTimeShift", value)

    # Public: Sets the double voice of the text to speech.
    # Use a value 1.0 - 4.0
    def set_double_voice(self, value):
        self.text_to_speech_service.setParameter("doubleVoice", value)

    # Public: Sets the pitch shift of the text to speech.
    # Use a value between 1.0 - 4.0
    def set_pitch_shift(self, value):
        self.text_to_speech_service.setParameter("pitchShift", value)

    # GETTERS

    # Public: Gets the volume of the text to speech.
    def get_volume(self):
        return self.text_to_speech_service.getVolume()

    # Public: Gets the speed of the text to speech.
    def get_voice_speed(self):
        return self.text_to_speech_service.getParameter("speed")

    # Public: Sets the default voice speed of the text to speech.
    def get_default_voice_speed(self):
        return self.text_to_speech_service.getParameter("defaultVoiceSpeed")

    # Public: Gets the double voice level of the text to speech.
    def get_double_voice_level(self):
        return self.text_to_speech_service.getParameter("doubleVoiceLevel")

    # Public: Gets the double voice time shift of the text to speech.
    def get_double_voice_time_shift(self):
        return self.text_to_speech_service.getParameter("doubleVoiceTimeShift")

    # Public: Gets the double voice of the text to speech.
    def get_double_voice(self):
        return self.text_to_speech_service.getParameter("doubleVoice")

    # Public: Gets the pitch shift of the text to speech.
    def get_pitch_shift(self):
        return self.text_to_speech_service.getParameter("pitchShift")