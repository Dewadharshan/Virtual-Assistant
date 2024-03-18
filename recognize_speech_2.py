from pydub.silence import split_on_silence
import speech_recognition as sr
from pydub import AudioSegment
import tkinter as tk
import pyautogui
import whisper
import tempfile
import torch
import numpy as np
import pre_analyse
import time
import threading
import keyboard
import data_analyzer
import tasks
import os
import io

listening_status = "None"
transcribed_text = {}

def speech_to_text(initiate):
        
    if initiate:
        window.lift()
        time.sleep(0.1)
        pyautogui.moveTo(20,1050)
        pyautogui.click()

        pyautogui.hotkey('win','h')

    text = text_entry.get()

    transcribed_text = {"text":text}
   
    return transcribed_text
    
def reset():
    text_entry.delete(0,"end")
    pyautogui.press('esc')


def execute_command():
    global is_listening
    print("started")
    while True:
        key_input = None
        key_input = keyboard.read_key()

        print("------------iteration----------")

        if key_input == 'ctrl':
            if not is_listening:
                is_listening = True
                speech_to_text(initiate = True)
                while is_listening:

                    transcribed_text = speech_to_text(initiate=False)
                    print("transcribed_text",transcribed_text['text'])

                    pre_analyse_command = data_analyzer.analyze_command(transcribed_text)
                    print("data analyse command",pre_analyse_command)
                    if pre_analyse_command != None:
                        command = pre_analyse_command

                    else:
                        command = pre_analyse.pre_analyse_command(transcribed_text['text'])

                    print("command = ",command)
                    if command != None:
                        reset()
                        is_listening = False
                        exec("tasks."+command)
                        #tasks.speak("command executed")

                        
                    time.sleep(0.5)
                        
        
        
            

def monitor():
    global is_listening
    while True:
        key_input = None
        key_input = keyboard.read_key()
        if key_input == 'alt':
            is_listening = False
            reset()



window = tk.Tk()
window.geometry(f"{400}x{30}+{0}+{1040}")
window.attributes('-topmost', True)
window.overrideredirect(True)
window.configure(bg="#202020")
window.geometry("400x150")


text_entry = tk.Entry(window,width=300,font=("Helvetica", 15),bg='#202020',fg='white')
text_entry.grid(row=0, column=0)

is_listening = False


command_execution_thread = threading.Thread(target=execute_command)
command_execution_thread.start()
monitor_execution_thread = threading.Thread(target=monitor)
monitor_execution_thread.start()

window.mainloop()


