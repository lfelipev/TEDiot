import os
import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class Speech():
    def __init__(self):
        self.client = speech.SpeechClient()
        self.fileName = os.path.join(
            os.path.dirname(__file__),
            'resources',
            'file.wav'
        )
        self.keyWordsPlay = ['toque', 'play', 'teste', 'tocar']
        self.keyWordsUpdate = ['atualize', 'update']
        self.keyWordsStop = ['pare', 'para', 'stop']
    
    def speechToText(self):
        with io.open(self.fileName, 'rb') as audioFile:
            print("Loading audio file...")
            content = audioFile.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=48000,
            language_code='pt-BR')

        print("Detecting speech...")
        response = self.client.recognize(config, audio)

        for result in response.results:
            return result.alternatives[0].transcript
