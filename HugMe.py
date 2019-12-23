import speech_recognition as sr
import sys, os
import time
from scripts import Sound
from scripts import Commands


s = Sound.Sound()
os.system("clear")
voiceAnalyser = Commands.voiceAnalyser('Config/commands.json')

def test():
    print(voiceAnalyser.getMostSimilar("play"))
    print("Done")

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)
            print("Recognizing now...")
            try:
                print("You said: " + r.recognize_google(audio) + "\n")
                try:
                    with open("Output/recorded.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    #print("Audio Recorded Successfully \n ")
                except Exception as e2:
                    print("Error saving recording: " + str(e2))
            except Exception as e:
                print("Error recognizing voice :  " + str(e))

if __name__ == "__main__":
    
    #main()
    test()