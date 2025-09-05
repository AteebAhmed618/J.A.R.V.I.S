J.A.R.V.I.S. - A Python Voice Assistant
J.A.R.V.I.S. is a personal voice assistant built in Python. This project demonstrates how to integrate various Python libraries to create a conversational, multi-functional application that can interact with you using both voice commands and a conversational AI backend.

✨ Features
Voice Interaction: Uses a masculine, robotic voice and listens for a wake word.

Dynamic Commands: Recognizes and executes commands to perform tasks like searching, browsing, and playing music.

Conversational AI: Integrates with the Google Gemini API to handle general questions and engage in natural conversation.

System Utilities: Reports on CPU usage and battery status.

Email Management: Sends emails via voice commands (requires a Gmail App Password).

Music Player: Plays, pauses, resumes, and stops a local music file (music.mp3).

To-Do List: Manages a simple to-do list stored in a file (todo.txt).

Interruptible Speech: A "stop talking" command allows you to interrupt J.A.R.V.I.S. mid-sentence.

⚙️ Prerequisites
To run this assistant, you need to have Python 3.6 or higher installed. You also need to install the following libraries. Open your terminal or command prompt and run:

pip install playsound SpeechRecognition gTTS pyttsx3 psutil pygame google-generativeai

You may also need to install PyAudio for microphone support:

pip install pyaudio

🚀 Getting Started
1. Configuration
Before running the program, you must update the jarvis.py file with your specific configuration details. Open the file and modify the following variables in the --- CONFIGURATION --- section:

EMAIL_ADDRESS: Your Gmail address.

EMAIL_PASSWORD: An App Password for your Gmail account. You can generate one from your Google Account security settings.

GEMINI_API_KEY: Your API key from Google AI Studio.

MIC_DEVICE_INDEX: The index of your microphone. You can find this by running a simple Python script provided in the main file's comments.

2. Required Files
music.mp3: Place an MP3 file named music.mp3 in the same directory as the jarvis.py script for the music commands to work.

todo.txt: The program will automatically create this file when you add your first to-do item.

3. Running the Assistant
Once you have configured the file and installed the prerequisites, you can run the program from your terminal:

python jarvis.py

🗣️ How to Use
J.A.R.V.I.S. is designed to be conversational. Remember to start every command with the wake word "jarvis" to get its attention.

Command

Example Phrase

Description

Greeting

"Jarvis, hello"

Responds with a greeting.

Time/Date

"Jarvis, what time is it?"

Reports the current time.

Web Search

"Jarvis, search for the latest news"

Opens a Google search in your browser.

YouTube

"Jarvis, open YouTube and play [video title]"

Opens a YouTube search for the video.

Music Control

"Jarvis, play music"

Plays the local music.mp3 file.

To-Do List

"Jarvis, add to-do item call the doctor"

Adds a new task to your to-do list.

System Status

"Jarvis, check system status"

Reports on CPU and battery usage.

Stop Talking

"Jarvis, stop talking"

Immediately interrupts J.A.R.V.I.S. while it's speaking.

Conversational AI

"Jarvis, what is the capital of France?"

Responds to general questions using a conversational AI.

📄 License
This project is open-source. Feel free to modify and adapt it for your own use.
