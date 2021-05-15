import speech_recognition as sr
from gtts import gTTS
import uuid
from playsound import playsound
import os
from time import ctime
import random

from utils.word_in_command import word_in_command


class VoiceBot:
    def __init__(self, username):
        self.r = sr.Recognizer()
        self.username = username

    def record_audio(self):
        print(f"Welcome {self.username}, how can i help you")

        with sr.Microphone() as source:
            audio = self.r.listen(source)
            command = ""

            try:
                command = self.r.recognize_google(audio)
                print(f"{self.username} issued the {command} command")
            except sr.UnknownValueError:
                print("Unknown value Error")
                self.speak("Sorry I did not get that ...")
            except sr.RequestError:
                print("Request Error")
                self.speak("Sorry my speech service is down ...")

            return command

    def speak(self, audio_string):
        text_to_speech = gTTS(text=audio_string, lang="en")
        audio_file = f"audio{uuid.uuid4()}.mp3"
        text_to_speech.save(audio_file)
        playsound(audio_file)
        print(audio_string)
        os.remove(audio_file)

    def respond(self, command):
        command = command.lower()

        if "time" in command:
            self.speak(ctime())

        if word_in_command(["hi", "yo"], command):
            greetings = [
                "Welcome, how can i help you",
                "hello",
                "What is your command",
                "hey, what's up",
            ]
            self.speak(f"{greetings[random.randint(0,len(greetings)-1)]} {username}")

        if "flip a coin" in command:
            options = ["heads", "tails"]
            choice = random.choice(options)
            self.speak(f"I got {choice}")

        if "exit" in command:
            self.speak("bye")
            exit()


username = "adam"
bot = VoiceBot(username=username)
bot.speak(f"Welcome master {username}. How can i help you today?")

while True:
    command = bot.record_audio()
    bot.respond(command)