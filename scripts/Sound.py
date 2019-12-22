import speech_recognition as sr
from gtts import gTTS
import pyaudio
import wave
import sys, os
import playsound
import time
from pynput import keyboard
import pydub
import random

class Sound:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.fileTemp = "Output/auxWaveFile.wav"
        self.stream = None
        self.wf = None
        self.paused = False
        self.abort = False
        self.prev = False
        self.next = False
        self.continueKey = True
        self.startStopKey = 269025044
        self.abortKey = 269025045
        self.prevKey = 269025046
        self.nextKey = 269025047

    def play(self, fileName):
        #playsound.playsound(fileName)
        # audio here
        sound = pydub.AudioSegment.from_mp3(fileName)
        sound.export(self.fileTemp, format="wav")
        self.wf = wave.open(self.fileTemp, 'rb')

        # open stream using callback
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                    channels=self.wf.getnchannels(),
                    rate=self.wf.getframerate(),
                    output=True,
                    stream_callback=self.callback)
        
        # start the stream
        self.stream.start_stream()
        try:
            while self.stream.is_active() or self.paused == True:
                if self.abort == True:
                    self.continueKey = False
                    break
                if self.next == True or self.prev == True:
                    break
                try:
                    with keyboard.Listener(on_press = self.on_press) as listener:
                        listener.join()
                    time.sleep(0.1)
                except Exception:
                    print("Error with Keyboard Listener")
        except Exception:
            print("Error with audio stream")
        # stop stream
        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()
        self.restart()

    def on_press(self, key):
        if key == keyboard.KeyCode(self.startStopKey):
            if self.stream.is_stopped():     # play audio
                print ('Play pressed')
                self.stream.start_stream()
                self.paused = False
                return False
            elif self.stream.is_active():   # pause audio
                print ('Pause pressed')
                self.stream.stop_stream()
                self.paused = True
                return False
        elif key == keyboard.KeyCode(self.abortKey):
            print("Abort pressed")
            self.abort = True
            return False
        elif key == keyboard.KeyCode(self.nextKey):
            print("Next pressed")
            self.next = True
        elif key == keyboard.KeyCode(self.prevKey):
            print("Prev pressed")
            self.prev = True
        return False

    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def playMusic(self):
        self.playMusicFromFile("Music")

    def playMusicFromFile(self, path):
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if file.endswith("mp3"):
                    files.append(os.path.join(r, file))
        index = -1
        previousMusics = []
        pointer = 0
        if len(files)>1:
            while self.continueKey:
                if pointer < len(previousMusics):
                    index = previousMusics[pointer]
                    self.play(files[index])
                    pointer += 1
                else:
                    possibleNextIndex = random.randint(0, len(files)-1)
                    if possibleNextIndex != index:
                        index = possibleNextIndex
                        previousMusics.append(index)
                        self.play(files[index])
                        pointer += 1
                if self.prev == True:
                    if pointer > 1:
                        pointer -= 2
                    else:
                        pointer -= 1
                    self.prev = False
        else:
            self.play(files[0])

    def speak(self, text):
        fileName = "Output/lastResponse.mp3"
        tts = gTTS(text = text, lang = 'en')
        tts.save(fileName)
        self.play(fileName)
        #playsound.playsound(fileName)

    def restart(self):
        self.stream = None
        self.wf = None
        self.paused = False
        self.abort = False
        self.next = False

    def bruteForceShutDown(self):
        # close PyAudio
        self.p.terminate()