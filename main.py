import os
import time
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import psutil
import pygame
import smtplib
import ssl
from email.message import EmailMessage
import google.generativeai as genai
import re

# --- CONFIGURATION ---
# Please fill in these details for the advanced features to work.
EMAIL_ADDRESS = "ateebahmed456@gmail.com"  # Your email address
# If using Gmail, you need an App Password. See instructions in the comments below.``
EMAIL_PASSWORD = "scrq fjma rbfy lteh" 
GEMINI_API_KEY = "AIzaSyA067knepcRkkI48XhCEI2nv64lzWzqceo" # Your Google Gemini API key

# --- SETUP AND INITIALIZATION ---

# Initialize the speech recognizer
r = sr.Recognizer()

# Initialize pygame mixer for music playback
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Pygame mixer initialization failed: {e}")

# Initialize the Gemini API
try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Gemini API key not configured: {e}")

# Set the microphone device index after you find it
# Run this code to find your index:
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Microphone with name '{name}' found for device_index {index}")
MIC_DEVICE_INDEX = 2 # Replace with your microphone's device index, e.g., 2
if MIC_DEVICE_INDEX is None:
    print("Please find your microphone device index and set the MIC_DEVICE_INDEX variable.")
    print("Then restart the program.")
    exit()

# Global flag to control speaking interruption
is_interrupting = False

def speak(text, interruptible=False):
    """
    Converts text to speech using a fresh pyttsx3 engine instance.
    This method is more reliable for consistent speech output.
    """
    global is_interrupting
    
    # Split text into sentences if it's an interruptible response
    if interruptible:
        sentences = re.split(r'(?<=[.!?]) +', text)
    else:
        sentences = [text]

    for sentence in sentences:
        if is_interrupting:
            is_interrupting = False
            return
            
        print(f"J.A.R.V.I.S.: {sentence}")
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')

            # Find and select a masculine voice for J.A.R.V.I.S.
            male_voice_found = False
            for voice in voices:
                if "male" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    male_voice_found = True
                    break
            if not male_voice_found:
                engine.setProperty('voice', voices[0].id)

            # Adjust speech speed and volume
            engine.setProperty('rate', 125) 
            engine.setProperty('volume', 0.8)
            
            engine.say(sentence)
            engine.runAndWait()
        except Exception as e:
            print(f"Error speaking text: {e}")
            break


def listen_for_command():
    """
    Listens for a voice command from the user and converts it to text.
    Handles timeouts and recognition errors.
    """
    global is_interrupting
    with sr.Microphone(device_index=MIC_DEVICE_INDEX) as source:
        print("Listening for a command...")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            # Increased timeout to 8 seconds and phrase_time_limit to 5 seconds
            audio = r.listen(source, timeout=8, phrase_time_limit=5)
            command = r.recognize_google(audio).lower()
            print(f"You said: {command}")
            if "stop talking" in command:
                is_interrupting = True
                print("Interrupt command received.")
                return ""
            return command
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from the Google Speech Recognition service; {e}")
            return ""


def get_llm_response(prompt):
    """
    Sends a prompt to the Gemini API and returns the text response.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I am unable to connect to the AI service. Error: {e}"


def handle_command(command):
    """
    Processes the user's command and performs a corresponding action.
    """
    # The wake word is "jarvis"
    if "jarvis" in command:
        # Remove the wake word to simplify command matching
        command = command.replace("jarvis", "").strip()

        # Check for commands using keywords
        if "hello" in command:
            speak("Hello, sir. How may I help you?")
        
        elif "time" in command:
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M %p")
            speak(f"The time is {current_time}.")

        elif "day" in command or "date" in command:
            today = datetime.date.today()
            speak(f"Today is {today.strftime('%A, %B %d, %Y')}.")

        elif "search for" in command:
            search_query = command.replace("search for", "").strip()
            speak(f"Searching for {search_query} on Google.")
            webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query}")
            time.sleep(2)

        elif "open website" in command:
            website_url = command.replace("open website", "").strip()
            if "." not in website_url:
                speak("Sorry, that does not appear to be a valid website. Please try again.")
            else:
                speak(f"Opening {website_url}.")
                webbrowser.open_new_tab(f"https://www.{website_url}")
                time.sleep(2)

        elif "open youtube" in command or "play video" in command:
            speak("What would you like to watch on YouTube?")
            video_query = listen_for_command()
            if video_query:
                speak(f"Playing {video_query} on YouTube.")
                webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={video_query}")
                time.sleep(2)
            else:
                speak("Sorry, I didn't catch that. Please try again.")

        elif "open application" in command:
            app_name = command.replace("open application", "").strip()
            speak(f"Attempting to open {app_name}.")
            try:
                subprocess.Popen([app_name])
            except FileNotFoundError:
                speak(f"Sorry, I could not find the application {app_name}. Please check the spelling.")

        # --- ADVANCED COMMANDS ---

        elif "send email" in command:
            speak("Who is the recipient?")
            recipient = listen_for_command()
            if recipient:
                speak("What is the subject?")
                subject = listen_for_command()
                speak("What is the message?")
                body = listen_for_command()
                send_email(recipient, subject, body)

        elif "check system status" in command:
            report_system_status()

        elif "play music" in command:
            play_music()

        elif "pause music" in command:
            pause_music()
        
        elif "resume music" in command:
            resume_music()

        elif "stop music" in command:
            stop_music()

        elif "add to-do item" in command:
            speak("What would you like to add to your to-do list?")
            item = listen_for_command()
            if item:
                add_todo_item(item)
                speak(f"Added '{item}' to your to-do list.")
        
        elif "read to-do list" in command:
            read_todo_list()

        elif "stop talking" in command:
            speak("Yes, sir.")

        elif command: # This block is for general chat questions for the LLM
            response = get_llm_response(command)
            speak(response, interruptible=True)

    elif "exit" in command or "goodbye" in command:
        speak("Goodbye, sir. I will be here if you need me.")
        exit()
    else:
        # This will be printed but not spoken to avoid speaking an error repeatedly
        print("Sorry, I did not understand that command. Please try again.")


# --- NEW FUNCTIONALITY IMPLEMENTATIONS ---

def send_email(recipient, subject, body):
    """
    Sends an email using the configured SMTP server.
    Note: For Gmail, you must use an App Password, not your regular password.
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        speak("Email configuration is not complete. Please check the code.")
        return

    recipients = {"test": "test@example.com"} # Example mapping, add your own recipients here

    if recipient in recipients:
        recipient_email = recipients[recipient]
    else:
        speak("I could not find that recipient. Please specify a valid email address.")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            speak("Email sent successfully.")
    except Exception as e:
        speak(f"Sorry, I could not send the email. Error: {e}")

def report_system_status():
    """
    Reports on system metrics like CPU and battery status.
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        speak(f"The current CPU usage is {cpu_percent} percent.")
    except Exception as e:
        speak(f"Error getting CPU status: {e}")

    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            power_plugged = battery.power_plugged
            if power_plugged:
                speak(f"The battery is at {percent} percent and is currently charging.")
            else:
                speak(f"The battery is at {percent} percent.")
        else:
            speak("No battery information available.")
    except Exception as e:
        speak(f"Error getting battery status: {e}")

def play_music():
    """
    Plays a music file using pygame.
    """
    music_file = 'music.mp3'
    if os.path.exists(music_file):
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            speak("Now playing music.")
        except pygame.error as e:
            speak(f"Sorry, there was an error playing the music: {e}")
    else:
        speak("Sorry, I could not find the music.mp3 file.")

def pause_music():
    """
    Pauses the currently playing music.
    """
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        speak("Music paused.")
    else:
        speak("No music is currently playing.")

def resume_music():
    """
    Resumes the paused music.
    """
    if pygame.mixer.music.get_pos() > 0:
        pygame.mixer.music.unpause()
        speak("Resuming music.")
    else:
        speak("No music has been paused to resume.")

def stop_music():
    """
    Stops the music playback entirely.
    """
    pygame.mixer.music.stop()
    speak("Music stopped.")

def add_todo_item(item):
    """
    Appends a new task to the to-do list file.
    """
    try:
        with open("todo.txt", "a") as f:
            f.write(f"- {item}\n")
    except Exception as e:
        speak(f"Error adding to-do item: {e}")

def read_todo_list():
    """
    Reads the to-do list and speaks each item.
    """
    if os.path.exists("todo.txt"):
        try:
            with open("todo.txt", "r") as f:
                tasks = f.read().strip()
                if tasks:
                    speak("Your to-do list is as follows:")
                    speak(tasks.replace('-', '...')) # Add a pause for each item
                else:
                    speak("Your to-do list is empty.")
        except Exception as e:
            speak(f"Error reading to-do list: {e}")
    else:
        speak("You do not have a to-do list yet.")

def main_loop():
    """
    The main loop of the voice assistant.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    speak("jarvis is ready, sir.")

    while True:
        command = listen_for_command()
        if command:
            handle_command(command)

# Start the assistant
if __name__ == "__main__":
    main_loop()
