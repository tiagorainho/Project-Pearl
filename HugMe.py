import speech_recognition as sr
import sys, os
import time
from scripts import Sound
from scripts import Commands
from scripts import Time

print("Preparing...")

soundOutput = Sound.Sound()
os.system("clear")
voiceAnalyser = Commands.CommandsAnalyser('Config/commands.json')

print("Assistant ready")


def playMusic(recognized):
    keyWord = "play"
    if keyWord.lower() in recognized.lower():
        artist = recognized.replace(keyWord, "").strip()
        for r, d, f in os.walk("Music"):
            for file in d:
                if file.lower() == artist.lower():
                    print("Playing music from " + artist + "...")
                    soundOutput.playMusic("Music/" + file)
                    print("Done")
                    return True
    return False

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
                    #print("Audio Recorded Successfully \n ")
                except Exception as e2:
                    print("Error saving recording: " + str(e2))

                ################################ commands begin #########################################
                

                if len(command) == 0 and len(recognized) == 0:
                    print("No match(empty string)")

                elif command == "play music":
                    if not playMusic(recognized):
                        print("Playing music...")
                        soundOutput.playMusic()

                elif command == "what time is it":
                    soundOutput.speak("It's " + Time.getTimeToString())

                elif command == "date":
                    soundOutput.speak("today is " + Time.getDate())

                elif command == "how are you":
                    soundOutput.speak("I'm fine thanks")
                else:
                    if "play" in recognized:
                        playMusic(recognized)
                    else:
                        print("No match")

                ################################ commands end  #########################################
            except Exception as e:
                #audio = r.listen(source)
                print("Error recognizing voice :  " + str(e))

if __name__ == "__main__":
    
    main()