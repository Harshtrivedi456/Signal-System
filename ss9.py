import tkinter as tk
from googletrans import Translator
import speech_recognition as sr
import pyttsx3  # Text-to-Speech library
import threading

# Translator instance
translator = Translator()

# Non-translatable words
non_translatable_words = [
    "Signal", "System", "Fourier transform", "Laplace", "Frequency", "Amplitude", "Phase", "Sampling", "Bandwidth",
    "Filter", "Modulation", "Digital Signal Processing", "Impulse Response", "signal system", "z transform"
]

# Function to translate text while retaining non-translatable terms
def translate_text_quick(text, target_lang="hi"):
    words = text.split()
    translated_words = []

    for word in words:
        if word.lower() in non_translatable_words:
            translated_words.append(word)
        else:
            try:
                translated_word = translator.translate(word, src='en', dest=target_lang).text
                translated_words.append(translated_word)
            except Exception as e:
                print(f"Translation error for '{word}': {e}")
                translated_words.append(word)  # Fallback

    return ' '.join(translated_words)

# Speech-to-Text & Text-to-Speech functionality
def listen_and_translate_continuous():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    engine = pyttsx3.init()  # Text-to-Speech engine

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                recognized_text = recognizer.recognize_google(audio)
                print(f"Recognized: {recognized_text}")

                translated_text = translate_text_quick(recognized_text)
                print(f"Translated: {translated_text}")

                # Display translated text on GUI
                subtitle_label.config(text=translated_text)

                # Convert translated text to speech
                engine.say(translated_text)
                engine.runAndWait()

            except sr.UnknownValueError:
                print("Could not understand speech.")
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
            except Exception as e:
                print(f"Error: {e}")

# GUI setup
root = tk.Tk()
root.title("Real-Time Speech Translation")

root.attributes('-topmost', 1)  # Always on top
root.overrideredirect(1)
root.geometry("800x100+100+20")
root.attributes('-alpha', 0.8)

subtitle_label = tk.Label(root, text="", font=("Helvetica", 16), fg="white", bg="black", wraplength=780, justify="center")
subtitle_label.pack(fill=tk.BOTH, expand=True)

control_frame = tk.Frame(root, bg="black")
control_frame.pack(fill=tk.X)

quit_button = tk.Button(control_frame, text="Quit", command=root.destroy, bg="red", fg="white", font=("Helvetica", 12))
quit_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Start listening
threading.Thread(target=listen_and_translate_continuous, daemon=True).start()

root.mainloop()
