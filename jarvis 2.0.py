import tkinter as tk
import math, random, threading
import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import time

# ------------------ TTS Setup ------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    update_text("Speaking...", "yellow")
    pulse_color["value"] = "yellow"
    speaking_state["value"] = True
    engine.say(text)
    engine.runAndWait()
    speaking_state["value"] = False
    update_text("JARVIS Online", "cyan")
    pulse_color["value"] = "cyan"

# ------------------ GUI Setup ------------------
root = tk.Tk()
root.title("JARVIS Circular Interface")
root.geometry("800x800")
root.configure(bg="black")

canvas = tk.Canvas(root, width=800, height=800, bg="black", highlightthickness=0)
canvas.pack()

label = tk.Label(root, text="JARVIS\nOnline", fg="cyan", bg="black", font=("Helvetica", 24, "bold"))
label.place(relx=0.5, rely=0.5, anchor="center")

def update_text(text, color="cyan"):
    label.config(text=text, fg=color)

# ------------------ Pulse Animation ------------------
pulse_size = 0
pulse_color = {"value": "cyan"}
speaking_state = {"value": False}

def pulse():
    global pulse_size
    canvas.delete("pulse")
    pulse_size = (pulse_size + 6) % 100
    canvas.create_oval(200 - pulse_size, 200 - pulse_size, 600 + pulse_size, 600 + pulse_size,
                       outline=pulse_color["value"], width=2, tags="pulse")
    canvas.create_oval(200, 200, 600, 600, outline=pulse_color["value"], width=3, tags="pulse")
    root.after(60, pulse)
pulse()

# ------------------ Rotating Arc ------------------
arc_angle = 0
def rotate_arc():
    global arc_angle
    canvas.delete("arc")
    arc_angle = (arc_angle + 5) % 360
    canvas.create_arc(240, 240, 560, 560, start=arc_angle, extent=120,
                      outline="cyan", width=2, style="arc", tags="arc")
    root.after(60, rotate_arc)
rotate_arc()

# ------------------ Orbiting Particles ------------------
particles = []
for _ in range(30):
    angle = random.randint(0, 360)
    radius = random.randint(250, 320)
    particles.append({"angle": angle, "radius": radius})

def animate_particles():
    canvas.delete("particle")
    for p in particles:
        p["angle"] = (p["angle"] + 2) % 360
        x = 400 + p["radius"] * math.cos(math.radians(p["angle"]))
        y = 400 + p["radius"] * math.sin(math.radians(p["angle"]))
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="cyan", outline="", tags="particle")
    root.after(60, animate_particles)
animate_particles()

# ------------------ Waveform Animation ------------------
wave_phase = 0
def animate_waveform():
    global wave_phase
    canvas.delete("waveform")
    if speaking_state["value"]:  # Only show waveform when speaking
        wave_phase += 0.3
        for x in range(220, 580, 15):
            y = 400 + 30 * math.sin((x/50) + wave_phase)
            canvas.create_line(x, y, x+15, y, fill=pulse_color["value"], width=2, tags="waveform")
    root.after(60, animate_waveform)
animate_waveform()

# ------------------ Command Execution ------------------
def execute_command(command):
    command = command.lower()
    if "play song" in command:
        song = command.replace("play song", "").strip()
        if song:
            speak(f"Playing {song}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
            update_text(f"Playing: {song}", "green")
        else:
            speak("Please say the song name.")
            update_text("No song name given.", "red")

    elif "time" in command:
        now = datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}")
        update_text(f"Time: {now}", "green")

    elif "open browser" in command:
        speak("Opening browser.")
        webbrowser.open("https://www.google.com")
        update_text("Browser opened.", "green")

    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            update_text(f"Searching: {query}", "green")
        else:
            speak("Please say what to search.")
            update_text("No search query.", "red")

    elif "shutdown" in command:
        speak("Shutting down. Goodbye Ambika.")
        update_text("Shutting down...", "red")
        time.sleep(2)
        root.destroy()

    elif "joke" in command:
        joke = "Why did the computer go to therapy? It had too many bytes of trauma."
        speak(joke)
        update_text("Telling a joke...", "green")

    elif "weather" in command:
        speak("Opening weather forecast.")
        webbrowser.open("https://www.google.com/search?q=weather+Pune")
        update_text("Weather opened.", "green")

    else:
        speak("Command not recognized.")
        update_text("Unknown command.", "red")

# ------------------ Continuous Listening ------------------
def continuous_listener():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                update_text("Listening...", "yellow")
                pulse_color["value"] = "yellow"
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = recognizer.recognize_google(audio, language="en-IN")
                update_text(f"You said: {command}", "cyan")
                pulse_color["value"] = "cyan"
                execute_command(command)
            except sr.UnknownValueError:
                update_text("Could not understand.", "red")
                pulse_color["value"] = "red"
            except sr.RequestError:
                update_text("Recognition service unavailable.", "red")
                pulse_color["value"] = "red"
            except:
                pass

threading.Thread(target=continuous_listener, daemon=True).start()

root.mainloop()
