import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import openai
import datetime
from config import api
#code for ai
# Initialize global variables
chatStr = ""
apikey = api   # Replace with your OpenAI API key

from openai import OpenAI

client = OpenAI(api_key=apikey)

def chat(query):
    global chatStr
    chatStr += f"User: {query}\nAssistant: "
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or another suitable model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": chatStr}
        ],
        temperature=0.7,
        max_tokens=256
    )
    reply = response.choices[0].message.content.strip()
    print(f"AI: {reply}")  # Print the AI response
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
    print(f"AI: {text}")  # Print the AI response
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    # Use a more reliable naming strategy for files
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

if __name__ == '__main__':
    say("Hello I am  Aayush A usefull personal assistant")
    while True:
        print("Listening...")
        query = take_command()

        # Check if the query is to open a website
        if "open" in query.lower():
            site_query = query.lower().replace("open", "").strip()
            url = get_site_url(site_query)
            if url:
                say(f"Opening {site_query} for you")
                webbrowser.open_new_tab(url)
            else:
                say("Sorry, I could not find the URL for that site.")

        # Open music (Note: `os.system("open ...")` is for macOS; for Windows use `start`)
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
