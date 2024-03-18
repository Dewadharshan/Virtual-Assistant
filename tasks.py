import json
import os
import comtypes
import subprocess
import time
from datetime import datetime
import cv2
import PIL.Image
import pyautogui
import pytesseract
import pyttsx3
import threading
from PIL import Image, ImageOps, ImageEnhance
from bs4 import BeautifulSoup
import spacy
from gtts import gTTS
from openpyxl import Workbook, load_workbook
from pynput.keyboard import Controller, Key
from pytesseract import Output
import AppOpener
import requests
import application_tasks
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Listener 
from selenium import webdriver

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
global nlp
driver = "temp"
#nlp = spacy.load("en_core_web_lg")
def speak_2(content,slow = False , voice = 1, needed_thread = True):
    print(content)
    try:
        def speak_thread():
            engine = pyttsx3.init()
            if slow == True:
                rate = engine.getProperty('rate')
                engine.setProperty('rate', 150)
            voices = engine.getProperty('voices') 
            engine.setProperty('voice', voices[voice].id)
            
            engine.say(content)
            engine.runAndWait()
        if needed_thread:
            thread = threading.Thread(target=speak_thread)
            thread.start()
        else:
            speak_thread()
    except:
        print("error while speaking")


def speak(content, slow=False, voice=1, needed_thread=True):
    def speak_thread():
        # Initialize COM
        comtypes.CoInitialize()
        try:
            engine = pyttsx3.init()
            if slow:
                rate = engine.getProperty('rate')
                engine.setProperty('rate', 150)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[voice].id)
            
            engine.say(content)
            engine.runAndWait()
        except:
            print("some error BS")

        finally:
            # Uninitialize COM
            comtypes.CoUninitialize()

    if needed_thread:
        thread = threading.Thread(target=speak_thread)
        thread.start()
    else:
        speak_thread()



def speak_google(content, slow = False):

    audio = myobj = gTTS(text=content, lang='en', slow=slow)
    audio.save("D:\\mini_project\\temp\\welcome.mp3")
    from playsound import playsound
    playsound('D:\\mini_project\\temp\\welcome.mp3')
    os.remove('D:\\mini_project\\temp\\welcome.mp3')

def open_application(app, speak_needed = True):

    if True:
        open_app = None
        open_app_arr = []
        dict1 = dict()
        temp = ""
        tot_application = AppOpener.give_appnames()
        #print(tot_application)
        for i in tot_application:
            if app.strip() == i:
                open_app = i
                break
            elif app.strip() in i:
                open_app_arr.append(i)
        
        if open_app_arr != [] and len(open_app_arr) >1:
            print(open_app_arr)
            speak("which one do you want to open")
            for i in open_app_arr:
                temp += i+"   "
            speak(temp)
            app = input()     #needs to be changed to voice input
            for i in open_app_arr:
                dict1[i] = nlp(i).similarity(nlp(app))
                print(dict1)
            index_app = list(dict1.values()).index(max(dict1.values()))
            
            if list(dict1.values())[index_app] >=0.5:
                open_app = open_app_arr[index_app]
           


        elif len(open_app_arr) == 1:
            open_app = open_app_arr[0]

        
        if open_app != None:
            if speak_needed:
                speak("opening"+open_app)
            AppOpener.open(open_app)
        else:
            speak("sorry ! "+app+" is not installed")
            print("not installed")

def find_text_on_screen(text):

    def invert_image_if_needed(image):
        avg_color = ImageOps.exif_transpose(image).convert("RGB").resize((1, 1)).getpixel((0, 0))
        is_dark_background = sum(avg_color) / 3 < 128

        if is_dark_background:
            inverted_image = ImageOps.invert(image)
        else:
            inverted_image = image

        inverted_image = inverted_image.convert("L")

        enhancer = ImageEnhance.Contrast(inverted_image)
        enhanced_image = enhancer.enhance(1.2)

        return enhanced_image




    text = text.lower().strip()
    myscreenshot=pyautogui.screenshot()
    inverted_image = invert_image_if_needed(myscreenshot)
    inverted_image.save(r"D:\\mini_project\\temp\\screenshot.png")

    data = pytesseract.image_to_data(PIL.Image.open("D:\\mini_project\\temp\\screenshot.png"),output_type = Output.DICT) 
    
    for i,value in enumerate(data['text']):
        data['text'][i] = data['text'][i].lower()

    with open("temp.json",'w') as f:
        f.write(json.dumps(data))
    try:
        x,y,width,height = data['left'][data['text'].index(text)],  data['top'][data['text'].index(text)],  data['width'][data['text'].index(text)],  data['height'][data['text'].index(text)]
        pyautogui.moveTo(x+width/2,  y+height/2)
        pyautogui.click()
        speak("clicking "+text)
        print(x+width/2,y+height/2)
    except:
        print("cannot find",text,"on the screen")
        speak("Sorry. Cannot find",text,"on the screen")
        return str("cannot find"+text+"on the screen") , False

def wifi_on_and_off(value):
    
    if value == 1:
        MyWish = subprocess.run (['netsh', 'interface', 'set', 'interface', "wi-fi", "ENABLED"])
        speak ("The wifi has been turned on")
    elif value == 0:
        MyWish = subprocess.run (['netsh', 'interface', 'set', 'interface', "wi-fi", "DISABLED"])
        speak( "The wifi has been turned off")
    else:
        return "sorry ! some error occured during the process"

def wifi_connect():
    pyautogui.moveTo(1766,1047)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(1573,454)
    pyautogui.click()
    network_name = 'student'
    temp = 10
    while temp:
        try:
            for i in range(0,10):
                x,y = find_text_on_screen(network_name)
                if y != False:
                    break
        
            if y != False:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                time.sleep(0.8)
                for i in range(0,5):
                    x,y = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\wifi_connect.png',confidence = 0.9)
                    if x != None:
                        break
                pyautogui.moveTo(x,y)
                pyautogui.click()
            else:
                print('cannot find the network')
            break
        except:
            temp-=1

def pause_play():
    pyautogui.press("playpause")

def mute_volume():
    keyboard = Controller()
    try:
        speak("The volume has been muted",needed_thread=False)
        keyboard.press(Key.media_volume_mute)
    except:
        speak("Sorry ! there was a problem while muting the volume")
    time.sleep(0.1)

def sleep_computer():
    speak("turning computer to sleep")
    try:
        os.system('cmd /c "powercfg -H off" ')
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    except:
        speak("sorry ! there was a problem while turning the computer to sleep")

def hibernate_computer():
    speak("turning computer to hibernate")
    try:
        os.system('cmd /c "powercfg -H on" ')
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    except:
        speak("sorry ! there was a problem while turning the computer to hibernate")

def shutdown_computer():
    speak('do you want to shutdown your computer')
    response = input()
    if "yes" in response:
        speak('shutting down the computer')
        try:
            os.system("shutdown /s /t 1")
        except:
            speak('sorry ! there was a problem while shutting down the computer')
    else:
        speak('ok exitting from shutdown ')

def restart_computer():
    speak('do you want to restart your computer')
    response = input()
    if "yes" in response:
        speak('restarting the computer')
        try:
            os.system("shutdown /r /t 1")
        except:
            speak('sorry ! there was a problem while restarting the computer')
    else:
        speak('ok exitting from restart ')

def take_photo():
    AppOpener.open("camera")
    speak("ready ?",needed_thread=False)
    pyautogui.moveTo(960,540)
    pyautogui.click()
    speak("say chheeeeeese",slow = 1,needed_thread=False)
    pyautogui.press("space")

def record_video():
    cap= cv2.VideoCapture(0)

    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer= cv2.VideoWriter('D:\\mini_project\\files_by_assistant\\recoded_video_.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))


    while True:
        ret,frame= cap.read()

        writer.write(frame)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break


    cap.release()
    writer.release()
    cv2.destroyAllWindows()

def scroll_down():
    pyautogui.moveTo(960,540)
    for i in range(20):
        pyautogui.scroll(-30)

def scroll_up():
    pyautogui.moveTo(960,540)
    for i in range(20):
        pyautogui.scroll(30)

def zoom_in():
    pyautogui.hotkey('alt','tab')
    for i in range(0,3):
        pyautogui.hotkey('ctrl','+')

def zoom_out():
    pyautogui.hotkey('alt','tab')
    for i in range(0,3):
        pyautogui.hotkey('ctrl','-')

def refresh():
    pyautogui.hotkey('alt','tab')
    pyautogui.press('f5')
    pyautogui.hotkey('ctrl','r')

def take_screenshot():

    pyautogui.hotkey('win','printscreen')
    speak("done")

def screen_record():
    pyautogui.keyDown('win')
    pyautogui.keyDown('alt')
    pyautogui.keyDown('r')

    pyautogui.keyUp('r')
    pyautogui.keyUp('alt')
    pyautogui.keyUp('win')
    speak("screen record has been started")

def undo():
    pyautogui.hotkey('alt','tab')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl','z')

def redo():
    pyautogui.hotkey('alt','tab')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl','y')

def type(content):
    pyautogui.typewrite(content)

def press(key):
    pyautogui.press(key)

def volume(value):
    if value == 0:
        for temp_i in range(20):
            pyautogui.press("volumedown")
    if value == 1:
        for temp_i in range(20):
            pyautogui.press("volumeup")

def brightness(value):

    brightness_value = subprocess.run('powershell -Command "Get-Ciminstance -Namespace root/WMI -ClassName WmiMonitorBrightness | Select -ExpandProperty "CurrentBrightness""',capture_output=True)
    if value == 1:
        subprocess.run('powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,'+str(int(brightness_value.stdout)+30)+')')
        speak("brightness increased")
    if value == 0:
        subprocess.run('powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,'+str(int(brightness_value.stdout)-30)+')')
        speak("brightness decreased")

def show_desktop():
    speak('showing desktop')
    pyautogui.hotkey('win','d')

def maximize():
    pyautogui.hotkey('win','tab')
    time.sleep(0.2)
    pyautogui.press('enter')

def get_date_and_time(time = False, date = False, date_time = True):
    
    day = str(datetime.now().day)
    month = str(datetime.now().month)
    year = str(datetime.now().year)
    date_now = str(day+" "+month+" "+year)
    
    hour = int(datetime.now().hour)
    minute = str(datetime.now().minute)
    if hour > 12:
        meridiem = "PM"
        hour = str(hour - 12)
    else:
        meridiem = "AM"
        hour = str(hour)
    time_now = hour+" "+minute+" "+meridiem
    if time:
        speak("the time is "+time_now,slow = True)
        return time_now
    elif date:
        speak("today's date is "+date_now,slow = True)
    else:
        speak("today's date is "+date_now+" and the time is "+time_now, slow = True)

def mouse_left_click():
    speak("clicked")
    pyautogui.hotkey('alt','tab')
    pyautogui.click()

def mouse_right_click():
    speak("clicked")
    pyautogui.hotkey('alt','tab')
    pyautogui.click(button='right')

def airplane_mode(value):

    pyautogui.moveTo(1791,1057)
    pyautogui.click()
    start_time = time.perf_counter()
    status = 'init'
    while(time.perf_counter() - start_time <3):
        coor_off = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\airplane_mode_off.png', confidence=0.9)
        coor_on = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\airplane_mode_on.png', confidence=0.9)
        coor_on2 = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\airplane_mode_on_2.png', confidence=0.9)
        if coor_off:
            status = 0
            break
        elif coor_on:
            status = 1
            break
        elif coor_on2:
            status = 1
            break

    if status == 'init':
        speak('sorry there was an error occured while turning the airplane mode on or off')
        pyautogui.press('esc')
    elif value and status:
        speak('airplane mode is already turned on')
        pyautogui.press('esc')
    elif value == 0 and status == 0:
        speak('airplane mode is already turned off')
        pyautogui.press('esc')
    elif value == 1:
        pyautogui.moveTo(coor_off)
        pyautogui.click()
        pyautogui.press('esc')
        speak('airplane mode has been turned on')
    elif value == 0:
        pyautogui.moveTo(coor_on)
        pyautogui.click() 
        pyautogui.press('esc')
        speak('airplane mode has been turned off')   
    
def mobile_hotspot(value):
    pyautogui.moveTo(1791,1057)
    pyautogui.click()
    start_time = time.perf_counter()
    status = 'init'
    while(time.perf_counter() - start_time <3):
        coor_off2 = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\mobile_hotspot_cannot_on.png', confidence=0.95)
        if coor_off2:
            status = 'cannot'
            break

        coor_off = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\mobile_hotspot_off.png', confidence=0.95)
        if coor_off:
            status = 0
            break

        coor_on = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\mobile_hotspot_on.png', confidence=0.95)
        if coor_on:
            status = 1
            break

        coor_on2 = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\mobile_hotspot_on_2.png', confidence=0.95)
        if coor_on2:
            status = 1
            break
        

    if status == 'init':
        speak('sorry there was an error occured while turning the airplane mode on or off')
        pyautogui.press('esc')
    elif status == 'cannot':
        speak('sorry you need internet connection to turn on mobile hotspot')
        pyautogui,press('esc')
    elif value and status:
        speak('mobile hotspot is already turned on')
        pyautogui.press('esc')
    elif value == 0 and status == 0:
        speak('mobile hotspot is already turned off')
        pyautogui.press('esc')
    elif value == 1:
        pyautogui.moveTo(coor_off)
        pyautogui.click()
        pyautogui.press('esc')
        speak('mobile hotspot has been turned on')
    elif value == 0:
        pyautogui.moveTo(coor_on)
        pyautogui.click() 
        pyautogui.press('esc')
        speak('mobile hotspot has been turned off')   
    
def bluetooth(value):

    pyautogui.moveTo(1791,1057)
    pyautogui.click()
    start_time = time.perf_counter()
    status = 'init'
    while(time.perf_counter() - start_time <3):
        coor_off = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\bluetooth_off.png')
        if coor_off:
            status = 0
            break

        coor_on = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\bluetooth_on.png')
        if coor_on:
            status = 1
            break
        

    if status == 'init':
        speak('sorry there was an error occured while turning the bluetooth on or off')
        pyautogui.press('esc')
    elif value and status:
        speak('bluetooth is already turned on')
        pyautogui.press('esc')
    elif value == 0 and status == 0:
        speak('bluetooth is already turned off')
        pyautogui.press('esc')
    elif value == 1:
        x,y = coor_off
        pyautogui.moveTo(x-30,y)
        pyautogui.click()
        pyautogui.press('esc')
        speak('bluetooth has been turned on')
    elif value == 0:
        x,y = coor_on
        pyautogui.moveTo(x-30,y)
        pyautogui.click() 
        pyautogui.press('esc')
        speak('bluetooth has been turned off') 

def battery_saver(value):
    pyautogui.moveTo(1791,1057)
    pyautogui.click()
    start_time = time.perf_counter()
    status = 'init'
    while(time.perf_counter() - start_time <3):
        coor_off = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\battery_saver_off.png',confidence=0.95)
        if coor_off:
            status = 0
            break
        coor_off = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\battery_saver_cannot_on.png')
        if coor_off:
            status = 'cannot'
            break
        coor_on = pyautogui.locateCenterOnScreen('D:\\mini_project\\dependency_images\\battery_saver_on.png')
        if coor_on:
            status = 1
            break
        

    if status == 'init':
        speak('sorry there was an error occured while turning the battery saver on or off')
        pyautogui.press('esc')
    elif status == 'cannot':
        speak('sorry cannot turn on or off battery saver while plugged in')
        pyautogui.press('esc')
    elif value and status:
        speak('battery saver is already turned on')
        pyautogui.press('esc')
    elif value == 0 and status == 0:
        speak('battery saver is already turned off')
        pyautogui.press('esc')
    elif value == 1:
        x,y = coor_off
        pyautogui.moveTo(x,y)
        pyautogui.click()
        pyautogui.press('esc')
        speak('battery saver has been turned on')
    elif value == 0:
        x,y = coor_on
        pyautogui.moveTo(x,y)
        pyautogui.click() 
        pyautogui.press('esc')
        speak('battery saver has been turned off')  

def location():
    speak("sorry! there no location service on your computer")

def greeting():
    speak("hello! How can I help you today?")

def open_chrome():
    global driver
    speak("opening chrome")
    chrome_options = webdriver.ChromeOptions(); 
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])        
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(r"./chromedriver",desired_capabilities=capabilities,options=chrome_options)
    driver.maximize_window()

def open_youtube():
    
    try:
        speak("going to youtube")
        driver.get("https://www.youtube.com")
    except:
        print("error opening youtube")
        speak("sorry. The was an error opening youtube")

def introduction():
    speak("hello. I am a voice assistant specifically available on windows",needed_thread=False)
    speak("I can do anything you do on your computer",needed_thread=False)
    speak("you just need to command me ",needed_thread=False)
    speak("and I will do the rest",needed_thread=False)

def close_current_tab():
    #pyautogui.hotkey("alt","f4")
    pyautogui.moveTo(1900,20)
    pyautogui.click()
    speak("closed")

def play_video_by_count(value):
    if True:#try:
        if value == 1:
            video = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a/yt-image/img")
            video.click()
        elif value == 2:
            video = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[2]/div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a/yt-image/img")
            video.click()
        elif value == 3:
            video = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[3]/div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a/yt-image/img")
            video.click()
        elif value == 4:
            video = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[4]/div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a/yt-image/img")
            video.click()
        speak("playing the video")
    else:#except:
        print("error while clicking video")

def login_to_tel():
    global driver
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    chrome_options = webdriver.ChromeOptions(); 
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])        

    driver = webdriver.Chrome(r"./chromedriver",desired_capabilities=capabilities,options=chrome_options)
    driver.page_load_strategy = 'eager'

    driver.maximize_window()
    while True:
        try:
            driver.get("https://tlc.krgi.in/#/")
            break
        except:
            x=input("Network Error press ENTER to try again")
    tel=driver.find_element(By.XPATH,'//*[@id="mainArc-TELCURRICULA"]')
    tel.click()
    ug=driver.find_element(By.XPATH,'//*[@id="root"]/section/main[2]/div/div/div[4]/div/div[1]/div[2]/div/div/div[1]')
    ug.click()
    p=driver.current_window_handle
    test=driver.window_handles[0]
    test2=driver.window_handles[1]
    driver.switch_to.window(test2)
    time.sleep(2)
    start=driver.find_element(By.XPATH,'//*[@id="root"]/div/section/section/main[1]/div/div/div/div[1]/button')
    start.click()
    username=driver.find_element(By.XPATH,'//*[@id="Username1"]')
    username.send_keys("459437942815")
    time.sleep(0.5)
    password=driver.find_element(By.XPATH,'//*[@id="Password"]')
    password.click()
    password.send_keys("Rajeswari")
    time.sleep(0.5)
    enter=driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[3]/div[2]/div[3]/button")
    enter.click()
    #print("clicking sem2")
    try:
        sem2=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/section/main/div/div[2]/div[2]/div/button[2]/div/img')
        sem2.click()
    except:
        pass
    speak("opened")

def like_video(self):
    try:
        like = driver.find_element(By.XPATH,'//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
        like.click()
        speak("liked the video")
    except Exception as e:
        speak("sorry. There was an error")

def like_video(self):


    try:
        dislike = driver.find_element(By.XPATH,'//*[@id="segmented-dislike-button"]/ytd-toggle-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
        dislike.click()
        speak("disliked the video")
    except Exception as e:
        speak("sorry. There was an error")

def weather():
    speak("checking weather data")
    chrome = application_tasks.chrome()
    chrome.maximize()

    city = "karur"
    
    url = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(url).content
    
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    strdata = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    
    data = strdata.split('\n')
    time = data[0]
    sky = data[1]
    
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text
    
    pos = strd.find('Wind')
    
    speak("The temperature now is "+str(temp)+"\n The Sky is "+str(sky)+"\nThe Time is "+str(time))

    chrome.search("https://www.google.com/search?q="+"weather"+"karur")

def get_news():

    speak("here some current news for you")
    chrome = application_tasks.chrome()
    chrome.maximize()

    chrome.search("https://www.msn.com/en-in/news")

def search_google(text):

    speak("searching"+text)
    chrome = application_tasks.chrome()
    chrome.maximize()

    chrome.search("https://www.google.com/search?q="+text)

def take_notes():
    speak('taking notes')
    open_application('notepad',speak_needed=False)
    time.sleep(0.7)
    pyautogui.hotkey('win','h')