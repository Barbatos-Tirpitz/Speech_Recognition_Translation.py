import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import speech_recognition as sr
from googletrans import Translator

class SpeechRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Speech Recognition")

        # Choose Language
        self.language_label = tk.Label(master, text="Select Target Language:")
        self.language_label.pack()

        self.languages = ["English", "French", "German", "Spanish", "Filipino", "Japanese", "Russian"]  # Add more languages as needed
        self.selected_language = tk.StringVar()
        self.language_dropdown = ttk.Combobox(master, textvariable=self.selected_language, values=self.languages)
        self.language_dropdown.pack()

        # Choose Microphone
        self.microphone_label = tk.Label(master, text="Select Microphone:")
        self.microphone_label.pack()

        self.available_microphones = sr.Microphone().list_microphone_names()
        self.selected_microphone = tk.StringVar()
        self.microphone_dropdown = ttk.Combobox(master, textvariable=self.selected_microphone, values=self.available_microphones, width=50) # Adjust width as needed
        self.microphone_dropdown.pack()

        # Start and stop recording buttons
        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        # Text area for original speech
        self.text_area = scrolledtext.ScrolledText(master, width=40, height=10)
        self.text_area.pack()

        # Text area for translated text
        self.translated_text_area = scrolledtext.ScrolledText(master, width=40, height=10)
        self.translated_text_area.pack()

        self.is_recording = False

    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        threading.Thread(target=self.record_text).start()

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def record_text(self):
        r = sr.Recognizer()
        translator = Translator()
        with sr.Microphone(device_index=self.available_microphones.index(self.selected_microphone.get())) as source:
            while self.is_recording:
                try:   
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = r.listen(source)
                    recognized_text = r.recognize_google(audio)
                    self.text_area.insert(tk.END, recognized_text + '\n')

                    # Translate recognized text to the selected language
                    translated_text = translator.translate(recognized_text, dest=self.selected_language.get())
                    self.translated_text_area.insert(tk.END, translated_text.text + '\n')

                    self.output_text_to_file(recognized_text)
                except sr.RequestError as e:
                    self.text_area.insert(tk.END, "Could not request results; {0d}\n".format(e))
                    self.translated_text_area.insert(tk.END, "Could not request results; {0d}\n".format(e))
                    self.output_text_to_file("Could not request results; {0d}\n".format(e))
                except sr.UnknownValueError:
                    self.text_area.insert(tk.END, "Unknown Error Occurred\n")
                    self.translated_text_area.insert(tk.END, "Unknown Error Occurred\n")
                    self.output_text_to_file("Unknown Error Occurred\n")

    def output_text_to_file(self, text):
        with open("output.txt", "a") as f:
            f.write(text + "\n")

def main():
    root = tk.Tk()
    root.geometry("500x720")
    app = SpeechRecognizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
