
import pyttsx3
import speech_recognition as sr
import webbrowser
import openai
import datetime
import platform
import subprocess

import os
from openai import OpenAI
# Initialize global variables
chatStr = ""
from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=apikey)

# Initialize OpenAI client



def chat(query):
    global chatStr
    chatStr += f"User: {query}\nAssistant: "
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": chatStr}
        ],
        temperature=0.7,
        max_tokens=256
    )
    reply = response.choices[0].message.content.strip()
    print(f"AI: {reply}")
    say(reply)
    chatStr += f"{reply}\n"
    return reply

def ai(prompt):
    openai.api_key = apikey
    response = openai.Completion.create(
        model="GPT-4o mini",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text = response.choices[0].text.strip()
    print(f"AI: {text}")
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    safe_prompt = ''.join(char for char in prompt if char.isalnum() or char in (' ', '_')).strip()
    with open(f"Openai/{safe_prompt}.txt", "w") as f:
        f.write(text)
    return text

def get_site_url(query):
    response = ai(f"Provide the URL for {query}")
    return response

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f'You said: {query}')
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return "I didn't catch that."
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return "Service unavailable."

# Function to get app name based on query
def get_app_name(query):
    prompt = f"Based on the user query '{query}', suggest a specific application name that would be most relevant. Only return the application name, nothing else."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that suggests relevant application names based on user queries."},
            {"role": "user", "content": prompt}
        ]
    )
    suggested_app = response.choices[0].message.content.strip()
    return suggested_app

# Function to open the app
def open_app(app_name):
    system = platform.system()

    if system == "Windows":
        try:
            os.startfile(app_name)
        except FileNotFoundError:
            print(f"Could not find the application: {app_name}")
    elif system == "Darwin":  # macOS
        try:
            subprocess.call(["open", "-a", app_name])
        except subprocess.CalledProcessError:
            print(f"Could not open the application: {app_name}")
    elif system == "Linux":
        try:
            subprocess.Popen([app_name])
        except FileNotFoundError:
            print(f"Could not find the application: {app_name}")
    else:
        print(f"Unsupported operating system: {system}")

# Function to get website URL based on query
def get_website_url(query):
    prompt = f"Based on the user query '{query}', suggest a specific website URL that would be most relevant and helpful. Only return the URL, nothing else."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that suggests relevant website URLs based on user queries."},
            {"role": "user", "content": prompt}
        ]
    )
    suggested_url = response.choices[0].message.content.strip()
    return suggested_url

def open_website(url):
    webbrowser.open(url)

if __name__ == '__main__':
    say("Hello, I am Aayush, a useful personal assistant.")
    while True:
        print("Listening...")
        query = take_command()

        # Check if the query is to open a website
        if "open" in query.lower():
            site_query = query.lower().replace("open", "").strip()
            url = get_site_url(site_query)
            if url:
                say(f"Opening {site_query} for you")
                open_website(url)
            else:
                say("Sorry, I could not find the URL for that site.")

        # Check if the query is to open an app
        elif "open app" in query.lower():
            app_query = query.lower().replace("open app", "").strip()
            app_name = get_app_name(app_query)
            if app_name:
                say(f"Opening {app_name} for you")
                open_app(app_name)
            else:
                say("Sorry, I could not find the application.")

        # Open music
        elif "open music" in query.lower():
            musicpath = ""  # Specify your music path here
            if os.name == 'nt':  # Windows
                os.system(f"start {musicpath}")
            else:  # macOS
                os.system(f"open {musicpath}")

        # Tell the time
        elif "time" in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M %S")
            say(f"Sir, the time is {strfTime}")

        # Use AI for specific prompts
        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        # Exit the assistant
        elif "Exit".lower() in query.lower():
            say("Goodbye!")
            exit()

        # Reset chat history
        elif "reset chat".lower() in query.lower():
            chatStr = ""
            say("Chat history has been reset.")

        # Handle other commands
        else:
            say("Processing your request...")
            chat(query)
