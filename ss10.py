import tkinter as tk
from googletrans import Translator
import speech_recognition as sr
import threading

# Translator instance
translator = Translator()

# Non-translatable words
non_translatable_words = [
    "Signal", "System", "Fourier transform", "Laplace", "Frequency", "Amplitude", "Phase", "Sampling", "Bandwidth",
    "Filter", "Modulation", "Digital Signal Processing", "Impulse Response", "signal system", "z transform"
]

# File to save subtitles
output_file = "optimized_subtitles.txt"

# Real-time translation function
def translate_text_quick(text, target_lang="gu"):
    """Translates while retaining non-translatable technical terms."""
    words = text.split()  # Split text into words
    translated_words = []
    
    for word in words:
        # Check if the word matches any non-translatable term (case-insensitive)
        if word.lower() in [term.lower() for term in non_translatable_words]:
            translated_words.append(word)  # Keep the word as-is
        else:
            try:
                # Translate only if it's not in the non-translatable list
                translated_word = translator.translate(word, src='en', dest=target_lang).text
                translated_words.append(translated_word)
            except Exception as e:
                print(f"Translation error for '{word}': {e}")
                translated_words.append(word)  # Fallback to original word on error

    return ' '.join(translated_words)  # Join words back into a sentence


def listen_and_translate_continuous():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                print("Recognizing...")
                recognized_text = recognizer.recognize_google(audio)
                print(f"Recognized: {recognized_text}")

                # Translate quickly
                translated_text = translate_text_quick(recognized_text)
                print(f"Translated: {translated_text}")

                # Update GUI and save to file
                subtitle_label.config(text=translated_text)
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"{translated_text}\n")

            except sr.UnknownValueError:
                print("Could not understand speech.")
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
            except Exception as e:
                print(f"Error: {e}")


def start_listening():
    threading.Thread(target=listen_and_translate_continuous, daemon=True).start()

# Tkinter GUI setup
root = tk.Tk()
root.title("Real-Time Speech Translation")

# Always on top and transparent
root.attributes('-topmost', 1)  # Always on top
root.overrideredirect(1)        # Remove window decorations
root.geometry("800x100+100+20") # Position and size (width x height + x + y)
root.attributes('-alpha', 0.8)  # Transparency (0.0 to 1.0)

# Subtitle display
subtitle_label = tk.Label(root, text="", font=("Helvetica", 16), fg="white", bg="black", wraplength=780, justify="center")
subtitle_label.pack(fill=tk.BOTH, expand=True)

# Buttons (to quit if needed)
control_frame = tk.Frame(root, bg="black")
control_frame.pack(fill=tk.X)

quit_button = tk.Button(control_frame, text="Quit", command=root.destroy, bg="red", fg="white", font=("Helvetica", 12))
quit_button.pack(side=tk.RIGHT, padx=10, pady=5)

# Start listening when launched
start_listening()

# Main loop
root.mainloop()
