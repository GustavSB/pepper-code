"""
Library of methods to utilize the build-in text to speech functionality.
"""


class Speech:
    def __init__(self, session):
        """Initialise service"""
        self.text_to_speech_service = session.service("ALTextToSpeech")

    def say(self, text):
        """Convert the text to speech"""
        self.text_to_speech_service.say(text)

    def say_async(self, text):
        """Convert the text to speech"""
        self.text_to_speech_service.say(text, _async=True)
