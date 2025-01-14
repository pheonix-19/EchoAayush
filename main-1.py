import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import openai
import datetime
import subprocess
import pyautogui
import time

#code for ai
# Initialize global variables
chatStr = ""
apikey = os.getenv('OPENAI_API_KEY')

from openai import OpenAI

client = OpenAI(api_key=apikey)

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

def open_application(app_name):
    """Open local applications based on the system type"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(f'start {app_name}', shell=True)
        else:  # macOS and Linux
            subprocess.Popen(['open', '-a', app_name])
        return True
    except Exception as e:
        print(f"Error opening application: {e}")
        return False

def dictate_to_notepad():
    """Open Notepad and transcribe voice to text"""
    # Open Notepad
    if os.name == 'nt':  # Windows
        subprocess.Popen('notepad')
    else:  # macOS
        subprocess.Popen(['open', '-a', 'TextEdit'])
    
    # Give some time for the application to open
    time.sleep(2)
    
    say("Notepad is open. Start speaking to write. Say 'stop writing' to finish.")
    
    while True:
        text = take_command()
        
        if text.lower() == 'stop writing':
            say("Stopping dictation")
            break
        elif text != "I didn't catch that." and text != "Service unavailable.":
            # Type the text
            pyautogui.write(text + '\n')

if __name__ == '__main__':
    say("Hello I am Aayush A useful personal assistant")
    while True:
        print("Listening...")
        query = take_command()
        query_lower = query.lower()

        # Check if the query is to open a website
        if "open" in query_lower and ("www" in query_lower or "http" in query_lower or ".com" in query_lower):
            site_query = query_lower.replace("open", "").strip()
            url = get_site_url(site_query)
            if url:
                say(f"Opening {site_query} for you")
                webbrowser.open_new_tab(url)
            else:
                say("Sorry, I could not find the URL for that site.")

        # Open Notepad for dictation
        elif "open notepad" in query_lower and ("write" in query_lower or "type" in query_lower):
            say("Opening Notepad for dictation")
            dictate_to_notepad()

        # Open local applications
        elif "open" in query_lower:
            app_name = query_lower.replace("open", "").strip()
            if open_application(app_name):
                say(f"Opening {app_name}")
            else:
                say(f"Sorry, I couldn't open {app_name}")

        # Open music
        elif "open music" in query_lower:
            musicpath = ""  # Specify your music path here
            if os.name == 'nt':  # Windows
                os.system(f"start {musicpath}")
            else:  # macOS
                os.system(f"open {musicpath}")

        # Tell the time
        elif "time" in query_lower:
            strfTime = datetime.datetime.now().strftime("%H:%M %S")
            say(f"Sir, the time is {strfTime}")

        # Use AI for specific prompts
        elif "using artificial intelligence" in query_lower:
            ai(prompt=query)

        # Exit the assistant
        elif "exit" in query_lower:
            say("Goodbye!")
            exit()

        # Reset chat history
        elif "reset chat" in query_lower:
            chatStr = ""
            say("Chat history has been reset.")

        # Handle other commands
        else:
            say("Processing your request...")
            chat(query)