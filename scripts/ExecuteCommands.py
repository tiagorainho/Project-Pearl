import sys, os
from scripts import Network

class CommandsExecuter:
    def __init__(self, soundOutput):
        self.soundOutput = soundOutput

    def playMusic(self, recognized):
        keyWord = "play"
        if keyWord.lower() in recognized.lower():
            artist = recognized.replace(keyWord, "").strip()
            for r, d, f in os.walk("Music"):
                for file in d:
                    if file.lower() == artist.lower():
                        print("Playing music from " + artist + "...")
                        self.soundOutput.playMusic("Music/" + file)
                        return True
        return False

    def getIp(self):
        ip = Network.getIp()
        self.soundOutput.speak(ip)
        return ip


    def getComputerName(self):
        name = Network.getComputerName()
        self.soundOutput.speak(name)
        return name