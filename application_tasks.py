from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Listener
from selenium import webdriver
from threading import Thread
import subprocess
import pyautogui
import pyttsx3
import time

def speak(content,slow = False , voice = 1):
    
    engine = pyttsx3.init()
    if slow == True:
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 150)
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[voice].id)
    
    engine.say(content)
    engine.runAndWait()

class file_explorer:

    def new_folder(self):
        pyautogui.hotkey('ctrl','shift','n')

    def file_rename(self):
        pyautogui.press('f2')
    


class chrome:
    global driver
    def __init__(self):
        global driver
        chrome_options = webdriver.ChromeOptions(); 
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])        
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        driver = webdriver.Chrome(r"./chromedriver",desired_capabilities=capabilities,options=chrome_options)
        
    def search(self,url):
        driver.get(url = url)
    def maximize(self):
        driver.maximize_window()
    class youtube:
        def play_video_by_count(self,value):
            try:
                if value == 1:
                    video = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a/yt-image/img")
                    video.click()
                elif value == 2:
                    video = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[2]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a/yt-image/img")
                    video.click()
                elif value == 3:
                    video = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[3]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a/yt-image/img")
                    video.click()
                elif value == 4:
                    video = driver.find_element(By.XPATH,"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[4]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a/yt-image/img")
                    video.click()
                speak("playing the video")
            except:
                print("error while clicking video") 
                
        def play_pause(self):
            try:
                ActionChains(driver).send_keys('k').perform()
            except:
                speak("sorry there was an error while pausing the video")

        def next_video(self):
            pyautogui.hotkey('shift','n')
            speak("playing next video")

        def previous_video(self):
            pyautogui.hotkey('altleft','left')
            speak("going to previous page")

        def like_video(self):
            try:
                like = driver.find_element(By.XPATH,'//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
                like.click()
                speak("liked the video")
            except Exception as e:
                print(e)

        def dislike_video(self):
            try:
                dislike = driver.find_element(By.XPATH,'//*[@id="segmented-dislike-button"]/ytd-toggle-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
                dislike.click()
                speak("disliked the video")
            except Exception as e:
                print(e)

        def share_video(self):
            pass

        def subscribe(self):
            try:
                sub = driver.find_element(By.XPATH,'//*[@id="subscribe-button"]/ytd-subscribe-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
                sub.click()
                speak("subscribed")
            except Exception as e:
                print(e)

        def unsubscribe(self):
            try:
                unsub = driver.find_element(By.XPATH,'//*[@id="subscribe-button"]/ytd-subscribe-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
                unsub.click()
                speak("unsubscribed")
            except Exception as e:
                print(e)
                
        def turn_on_notification(self):
            pass
        def save_to_watchlater(self):
            pass
        def report_video(self):
            pass

    class gmail:
        def write_mail(self):
            pass
        def open_first_mail(self):
            pass
        def reply(self):
            pass
        def forward_mail(self):
            pass
        def delete_mail(self):
            pass
        

