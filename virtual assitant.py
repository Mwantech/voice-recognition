import speech_recognition as sr
import pyttsx3 as p
import datetime
import os
import time
import subprocess
import wikipedia
import webbrowser
import ecapture as ec
import json
import requests

# Initialize text to speech
engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user based on the time of day
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello joshua, Good Morning")
        print("Hello joshua, Good Morning")
    elif 12 <= hour < 18:
        speak("Hello joshua, Good Afternoon")
        print("Hello joshua, Good Afternoon")
    else:
        speak("Hello joshua, Good Evening")
        print("Hello joshua, Good Evening")

# Function to capture user's voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        print("listening...")
        audio = r.listen(source, timeout=3)
        text = r.recognize_google(audio)
        print(text)
        return text

# Logical question to OpenAI
def send_question_openai(api_key, question):
    openai_url = "https://api.openai.com/v1/ask"  # Corrected URL
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}  # Added space in Authorization
    data = {'question': question}
    response = requests.post(openai_url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('answer', 'No response from Openai')
    else:
        return f'Error {response.status_code}: unable to get response from openAI'

# Greeting and initialization
print("Am your AI personal assistant MWANTECH")
speak("Am your AI personal assistant MWANTECH")
wishMe()

# Main loop for handling user commands
if __name__ == '__main__':
    while True:
        speak("How can I help you now?")
        text = takeCommand()

        if text == 0:
            continue

        # Shutdown command
        if "good bye" in text or "ok bye" in text or "stop" in text:
            speak('Your personal assistant MWANTECH is shutting down,Have a nice time, Goodbye')
            print('Your personal assistant MWANTECH is shutting down,Have a nice time, Goodbye')
            break

        # Open commands
        elif 'play on Youtube' in text:
            video_query = text.replace('play on Youtube', '').strip()
            youtube_url = f"https://www.youtube.com/results?search_query={video_query.replace(' ', '+')}"
            webbrowser.open_new_tab(youtube_url)
            speak(f"playing {video_query} on Youtube now")
            time.sleep(5)

        elif 'ask OpenAI' in text:
            api_key = "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"
            question = text.replace('ask OpenAI', '').strip()
            response = send_question_openai(api_key, question)
            speak("Here is the response from openAI: " + response)
            time.sleep(5)

        elif 'open gmail' in text:
            webbrowser.open_new_tab("https://www.gmail.com")
            speak("Google Mail is open now")
            time.sleep(5)

        # Wikipedia search
        elif 'wikipedia' in text:
            speak('Searching Wikipedia...')
            text = text.replace("wikipedia", "")
            results = wikipedia.summary(text, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Time command
        elif 'time' in text:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        # Camera command
        elif "camera" in text or "take a photo" in text:
            ec.capture(0, "robo camera", "img.jpg")

        # News command
        elif 'news' in text:
            webbrowser.open_new_tab("https://www.kenyans.co.ke/news")
            speak('Here are some headlines from kenya today')
            time.sleep(6)

        # Search command
        elif 'search' in text:
            statement = text.replace("search", "")
            webbrowser.open_new_tab("https://www.google.com/search?q=" + statement)
            time.sleep(5)

        # Weather commands
        elif "weather" in text:
            api_key = "Apply your unique ID"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What is the city name?")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f"Temperature in Kelvin unit is {current_temperature}, "
                      f"Humidity in percentage is {current_humidity}, "
                      f"Description: {weather_description}")
                print(f"Temperature in Kelvin unit = {current_temperature}, "
                      f"Humidity (in percentage) = {current_humidity}, "
                      f"Description = {weather_description}")

        # Introduction command
        elif 'who are you' in text or 'what can you do' in text:
            speak('I am MWANTECH version 1.0, your personal assistant. I am programmed to perform tasks like '
                  'opening YouTube, Google Chrome, Gmail, and Stack Overflow, predicting time, taking a photo, '
                  'searching Wikipedia, predicting weather in different cities, and providing top headlines from Times of India. '
                  'You can also ask me computational or geographical questions!')

        # Creator information command
        elif "who made you" in text or "who created you" in text or "who discovered you" in text:
            speak("I was built by JOSHUA")
            print("I was built by JOSHUA")

        # Log off command
        elif "log off" in text or "sign out" in text:
            speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
            subprocess.call(["shutdown", "/l"])

        time.sleep(5)