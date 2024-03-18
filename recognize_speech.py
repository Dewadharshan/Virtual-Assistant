from pydub.silence import split_on_silence
import speech_recognition as sr
from pydub import AudioSegment
import whisper
import tempfile
import torch
import numpy as np
import time
import whisper
import threading
import keyboard
import data_analyzer
import tasks
import os
import io


whisper_model = whisper.load_model('small.en')
listening_status = "None"
transcribed_text = ""

def speech_to_text():

    r = sr.Recognizer()
    global listening_status
    listening_status = "None"

    def callback(recognizer,audio):
        global listening_status
        global transcribed_text

        stop_listening(wait_for_stop=False)
        listening_status = "processing"
        print("processing")
        save_path = "D:\\mini_project\\model_creating\\audio_listen_in_background.mp3"
        data = io.BytesIO(audio.get_wav_data())
        audio_clip = AudioSegment.from_file(data)
        audio_clip.export(save_path, format="mp3") 
        #start_time = time.time()
        #sound = AudioSegment.from_file(save_path, format = "mp3") 

        #audio_chunks = split_on_silence(sound
        #                    ,min_silence_len = 100
        #                    ,silence_thresh = -45
        #                    ,keep_silence = 50
        #                )
        #combined = AudioSegment.empty()
        #for chunk in audio_chunks:
        #    combined += chunk
            
        #combined.export(save_path, format = "mp3")
        transcribed_text = whisper_model.transcribe(save_path,language = "en")
        #transcribed_text['text'] = "what is the time now"
        #print(time.time()-start_time)
        listening_status = "completed"
        
        

    def stop_listen():
        global listening_status
        while True:
            key_input = keyboard.read_key()
            if key_input == "alt":
                stop_listening(wait_for_stop=False)
                listening_status = "interrupted"
                break


    


    
    print("started")
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)

    while True:
        key_input = None
        key_input = keyboard.read_key()
        if key_input == 'ctrl':
            listening_status = "listening"
            print("listening")
            stop_listening = r.listen_in_background(m,callback)
            stop_listen_thread = threading.Thread(target=stop_listen)
            stop_listen_thread.daemon = True
            stop_listen_thread.start()
            break


    while True:
        if listening_status == "completed" or listening_status == "interrupted":
            return transcribed_text
            
        time.sleep(1)
    
    print("listening stopped")
    
while True:

    transcribed_text = speech_to_text()
    print(transcribed_text['text'])
    

    command = data_analyzer.analyze_command(transcribed_text)
    print("command = ",command)
    if command != None:
        exec("tasks."+command)
        tasks.speak("command executed")

