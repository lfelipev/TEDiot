import time
import pyaudio
import wave
import io
import os
import sys
from threading import Thread
import datetime
import msvcrt as main
from speech import Speech

class TEDrecord:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 48000
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "resources/file.wav"
        self.audio = pyaudio.PyAudio()
        self.isPlaying = False
        self.myThread = None

    def startRecording(self):
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)
        print("recording...")
        frames = []
        
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("finished recording")
        
        
        # stop Recording
        stream.stop_stream()
        stream.close()
        
        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    def playWAV(self):
        '''
        Play (on the attached system sound device) the WAV file
        named wav_filename.'''
        global isPlaying
        wav_filename = 'resources/test.wav' 

        '''
        if ('1' in music_name or 'um' in music_name):
            wav_filename = wav_filename + 'jingle.wav'
        elif ('2' in music_name or 'dois' in music_name):
            wav_filename = wav_filename + 'Coca-Cola.wav'
        elif ('3' in music_name or 'tres' in music_name):
            wav_filename = wav_filename + 'Kazoo.wav'
        elif ('4' in music_name or 'quatro' in music_name):
            wav_filename = wav_filename + 'Roll.wav
            '''
        
        try:
            print('Trying to play file' + wav_filename)
            wf = wave.open(wav_filename, 'rb')
        except IOError as ioe:
            sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
            str(ioe) + '. Skipping.\n')
            return
        except EOFError as eofe:
            sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
            str(eofe) + '. Skipping.\n')
            return

        # Open stream.
        stream = self.audio.open(format=self.audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(self.CHUNK)
        while len(data) > 0 and self.isPlaying:
            stream.write(data)
            data = wf.readframes(self.CHUNK)

        # Stop stream.
        stream.stop_stream()
        stream.close()

    def continueMusic(self):
        #Play
        if not(self.isPlaying):
            isPlaying = True
            myThread = threading.Thread(target=loopPlay)
    
    def stopMusic(self):
        if(self.isPlaying):
            isPlaying = False

    def loopPlay(self):
        while isPlaying:
            print("Playing audio file")
            playWAV()


def buttonThread(ted):
    print("You can talk to TEDiot while the music is playing!")
    while(ted.isPlaying):
        input_state = GPIO.input(18)
        if input_state == False:
            ted.startRecording()



def main():
    ted = TEDrecord()
    speech = Speech()
    print("TEDiot is starting.....")
    while True:
        input_state = GPIO.input(18)
        if input_state == False:
            print("Now TEDiot is listening you...")
            ted.startRecording()
            audioResult = speech.speechToText()
            if not(ted.isPlaying):
                if any(word in audioResult for word in speech.getKeyWordsPlay):
                    ted.isPlaying = True
                    print("Starting button thread...")
                    t = Thread(target=wait(ted))
                    ted.playWAV()
                else:
                    print("OK!")

if __name__ == "__main__":
    main()

ted = TEDrecord()
ted.startRecording()
ted.isPlaying = True
ted.playWAV()
ted.audio.terminate()