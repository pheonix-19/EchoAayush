import os
import pyttsx3
import speech_recognition as sr
import datetime
import subprocess
import webbrowser
import pyautogui
import time
import keyboard
import psutil
import ctypes
import platform
from pathlib import Path

# Initialize text-to-speech engine
engine = pyttsx3.init()

def say(text):
    """Convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print(text)

def take_command():
    """Listen for and recognize voice commands"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f'User said: {query}')
            return query.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "none"
        except sr.RequestError:
            print("Could not request results")
            return "none"

def voice_typing():
    """Voice typing function that works in any application"""
    say("Voice typing mode activated. Say 'stop typing' to end.")
    while True:
        text = take_command()
        
        if text == "none":
            continue
            
        if "stop typing" in text:
            say("Voice typing deactivated")
            break
            
        # Handle special commands
        if text == "new line":
            pyautogui.press('enter')
        elif text == "backspace":
            pyautogui.press('backspace')
        elif text == "delete":
            pyautogui.press('delete')
        elif text == "tab":
            pyautogui.press('tab')
        elif text == "space":
            pyautogui.press('space')
        elif text == "clear all":
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
        else:
            # Type the text
            pyautogui.write(text + ' ')

def typing_commands():
    """Handle keyboard shortcut commands"""
    say("Command mode. What would you like to do?")
    text = take_command()
    
    commands = {
        "select all": ["ctrl", "a"],
        "copy": ["ctrl", "c"],
        "paste": ["ctrl", "v"],
        "cut": ["ctrl", "x"],
        "undo": ["ctrl", "z"],
        "redo": ["ctrl", "y"],
        "save": ["ctrl", "s"],
        "find": ["ctrl", "f"],
        "close": ["alt", "f4"],
        "enter": ["enter"]
    }
    
    for command, keys in commands.items():
        if command in text:
            pyautogui.hotkey(*keys)
            say(f"Executed {command}")
            return
            
    say("Command not recognized")

def open_application(app_name):
    """Open applications"""
    apps = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'word': 'winword.exe',
        'excel': 'excel.exe',
        'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
        'explorer': 'explorer.exe'
    }
    
    try:
        if app_name in apps:
            subprocess.Popen(apps[app_name])
        else:
            subprocess.Popen(f'start {app_name}', shell=True)
        return True
    except Exception as e:
        print(f"Error opening application: {e}")
        return False

def control_volume(command):
    """Control system volume"""
    try:
        if 'up' in command:
            for _ in range(5):
                pyautogui.press('volumeup')
            say("Volume increased")
        elif 'down' in command:
            for _ in range(5):
                pyautogui.press('volumedown')
            say("Volume decreased")
        elif 'mute' in command:
            pyautogui.press('volumemute')
            say("Volume muted")
    except Exception as e:
        print(f"Volume control error: {e}")

def control_media(command):
    """Control media playback"""
    try:
        if 'play' in command or 'pause' in command:
            pyautogui.press('playpause')
        elif 'next' in command:
            pyautogui.press('nexttrack')
        elif 'previous' in command:
            pyautogui.press('prevtrack')
    except Exception as e:
        print(f"Media control error: {e}")

def system_control(command):
    """Control system operations"""
    if 'shutdown' in command:
        say("Shutting down the system in 60 seconds")
        if platform.system() == 'Windows':
            os.system('shutdown /s /t 60')
    elif 'restart' in command:
        say("Restarting the system in 60 seconds")
        if platform.system() == 'Windows':
            os.system('shutdown /r /t 60')
    elif 'cancel shutdown' in command:
        if platform.system() == 'Windows':
            os.system('shutdown /a')
        say("Shutdown cancelled")
    elif 'sleep' in command:
        say("Putting system to sleep")
        if platform.system() == 'Windows':
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

def take_screenshot():
    """Take and save a screenshot"""
    try:
        screenshot_dir = Path.home() / "Pictures" / "Screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = screenshot_dir / f"screenshot_{timestamp}.png"
        pyautogui.screenshot(str(filename))
        say("Screenshot taken")
    except Exception as e:
        print(f"Screenshot error: {e}")

def open_website(site_name):
    """Open websites"""
    common_sites = {
        'google': 'https://www.google.com',
        'youtube': 'https://www.youtube.com',
        'facebook': 'https://www.facebook.com',
        'twitter': 'https://www.twitter.com',
        'gmail': 'https://www.gmail.com',
        'amazon': 'https://www.amazon.com',
        'wikipedia': 'https://www.wikipedia.org'
    }
    
    try:
        site_name = site_name.replace('open', '').replace('go to', '').strip()
        
        if site_name in common_sites:
            webbrowser.open(common_sites[site_name])
            say(f"Opening {site_name}")
        else:
            if not site_name.startswith(('http://', 'https://', 'www.')):
                site_name = 'www.' + site_name
            if not site_name.endswith('.com'):
                site_name += '.com'
            webbrowser.open(f'https://{site_name}')
            say(f"Opening {site_name}")
    except Exception as e:
        print(f"Website error: {e}")

def main():
    say("Hello! I am your voice assistant. You can start voice typing by saying 'start typing'")
    
    while True:
        query = take_command()
        if query == "none":
            continue

        # Voice typing
        if "start typing" in query or "voice type" in query:
            voice_typing()
            
        # Keyboard commands
        elif "keyboard command" in query:
            typing_commands()
            
        # Volume control
        elif "volume" in query:
            control_volume(query)
            
        # Media control
        elif any(word in query for word in ["play", "pause", "next", "previous"]):
            control_media(query)
            
        # System control
        elif any(word in query for word in ["shutdown", "restart", "sleep"]):
            system_control(query)
            
        # Screenshot
        elif "screenshot" in query:
            take_screenshot()
            
        # Open website
        elif "open" in query and any(site in query for site in ["website", ".com", "google", "youtube"]):
            open_website(query)
            
        # Open application
        elif "open" in query:
            app_name = query.replace("open", "").strip()
            if open_application(app_name):
                say(f"Opening {app_name}")
            else:
                say(f"Sorry, couldn't open {app_name}")
                
        # Tell time
        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            say(f"The current time is {current_time}")
            
        # Exit
        elif "exit" in query or "quit" in query:
            say("Goodbye!")
            break

if __name__ == "__main__":
    main()