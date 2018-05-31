import RPi.GPIO as GPIO
from audio import TEDrecord
from speech import Speech
from threading import Thread
import thread
from tedmqtt import TEDMQTT
import datetime

#Buttons variables
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def fileLog(message):
    dt = datetime.datetime.now()
    file = open('interations.txt','a')
    file.write(message + ' ' + dt.strftime("%Y-%m-%d %H:%M") + '\n')
    file.close()

def buttonThread(ted, speech):
    print("You can talk to TEDiot while the music is playing!")
    while(ted.isPlaying):
        input_state = GPIO.input(18)
        if input_state == False:
            ted.startRecording()
            audioResult = speech.speechToText()
            if any(word in audioResult for word in speech.keyWordsStop):
                print('Stoping the music...')
                fileLog(audioResult)
                ted.stopMusic()
            else:
                 print('Command not found!!')
            
def main():
    ted = TEDrecord()
    speech = Speech()
    tedmqtt = TEDMQTT()
    print("TEDiot is starting...press the button to start talking...")
    while True:
        input_state = GPIO.input(18)
        if input_state == False:
            print("Now TEDiot is listening you...")
            ted.startRecording()
            audioResult = speech.speechToText()
            if not(ted.isPlaying):
                if any(word in audioResult for word in speech.keyWordsPlay):
                    ted.isPlaying = True
                    print("Starting button thread...")
                    fileLog(audioResult)
                    t1 = Thread(target=buttonThread, args=(ted, speech))
                    t1.start()
                    ted.playWAV(audioResult)
                    #t1 = Thread(target=ted.playWAV(audioResult))
                elif any(word in audioResult for word in speech.keyWordsUpdate):
                    print("Updating the cloud...")
                    tedmqtt.update()
                else:
                    print("Command not found!")

if __name__ == "__main__":
    main()
