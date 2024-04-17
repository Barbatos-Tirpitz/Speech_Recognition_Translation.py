import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
from googletrans import Translator

class SpeechRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Speech Recognition")

        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.text_area = scrolledtext.ScrolledText(master, width=40, height=10)
        self.text_area.pack()

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
        while self.is_recording:
            try:   
                with sr.Microphone() as source2:
                    r.adjust_for_ambient_noise(source2, duration=0.2)
                    audio2 = r.listen(source2)
                    recognized_text = r.recognize_google(audio2)
                    self.text_area.insert(tk.END, recognized_text + '\n')

                    translation = Translator().translate(recognized_text, dest='es').text
                    self.text_area.insert(tk.END, f"Translated Text: {translation}\n")
                    
                    self.output_text_to_file(recognized_text)
            except sr.RequestError as e:
                self.text_area.insert(tk.END, "Could not request results; {0d}\n".format(e))
                self.output_text_to_file("Could not request results; {0d}\n".format(e))
            except sr.UnknownValueError:
                self.text_area.insert(tk.END, "Unknown Error Occurred\n")
                self.output_text_to_file("Unknown Error Occurred\n")

    def output_text_to_file(self, text):
        with open("output.txt", "a") as f:
            f.write(text + "\n")

   

def main():
    root = tk.Tk()
    app = SpeechRecognizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
