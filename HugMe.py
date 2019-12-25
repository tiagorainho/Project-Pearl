import speech_recognition as sr
import sys, os
import time
from scripts import Sound
from scripts import Commands
from scripts import Time
from scripts import ExecuteCommands

print("Preparing...")

soundOutput = Sound.Sound()
voiceAnalyser = Commands.CommandsAnalyser('Config/commands.json')
ex = ExecuteCommands.CommandsExecuter(soundOutput)
os.system("clear")

print("Assistant ready")


def manageCommands(command, recognized):
    if len(command) == 0 and len(recognized) == 0:
        print("No match(empty command)")

    elif command == "play music":
        if not ex.playMusic(recognized):
            print("Playing music...")
            soundOutput.playMusic()

    elif command == "what time is it":
        soundOutput.speak("It's " + Time.getTimeToString())

    elif command == "get date":
        soundOutput.speak("today is " + Time.getDate())

    elif command == "how are you":
        soundOutput.speak("I'm fine thanks")
    
    elif command == "get my ip":
        print("IP: " + ex.getIp())

    elif command == "get my computer name":
        print("Computer Name: " + ex.getComputerName())

    elif command == "list commands":
        commandsList = voiceAnalyser.listCommands()
        print(commandsList)
        soundOutput.speak(commandsList)
    else:
        if "play" in recognized:
            ex.playMusic(recognized)
        else:
            print("No match")

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)
            print("Recognizing now...")
            try:
                recognized = r.recognize_google(audio)
                command = voiceAnalyser.getMostSimilar(recognized).lower()
                print("heard:" + recognized)

                try:
                    with open("Output/lastRecord.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                except Exception as e2:
                    print("Error saving recording: " + str(e2))

                ################################ commands begin #########################################
                
                manageCommands(command, recognized)

                ################################ commands end  #########################################

            except Exception as e:
                #r = sr.Recognizer() ###################################################################---------------------------
                print("Error recognizing voice :  " + str(e))

if __name__ == "__main__":

    main()