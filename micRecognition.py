from selenium import webdriver  #version 4.3.0 as of 09_07_22
from selenium.webdriver.chrome.service import Service  #handle chrome driver
from selenium.webdriver.common.by import By  #get element by id
from webdriver_manager.chrome import ChromeDriverManager  #automatically download the correct version of the chrome driver
from selenium.common.exceptions import WebDriverException  #check if browser was closed

import os  #get current directory, check file existance
import shutil  #create backup
import time  #time sleep

import pyaudio  #record audio
import wave  #save audio
import atexit #close backup audio file if exited without executing normal closing line (use only in backup to have different methods of audio saving)

#PREPARING CHROME
chrome_options = webdriver.ChromeOptions()  #add the debug options you need
chrome_options.add_argument('--use-fake-ui-for-media-stream')  #does not ask for microphone access
chrome_options.add_argument("--log-level=3")  #remove some selenium logs
chrome_options.add_argument('--disable-gpu')  #disable hardware acceleration for compatibility reasons


#START CHROME
#download the most up-to-date chrome driver and create a chrome tab with the selected options
chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)

htmlPagePath = os.getcwd() + "//" + "micRecognition/micRecognition.html"  #get absolute path
chrome.get("file:///"+htmlPagePath)  #open page in chrome

#CREATE TXT FILE
def createTxtFile():
    filename = chrome.execute_script('return outputFileName')
    try:
        file = open(filename+".txt", "x")  #there is already a file with this name
    except:
        i = 0
        while(True):  #try different names
            i += 1
            try:
                file = open(filename+str(i)+".txt", "x")
                filename = filename+str(i)
                break
            except:
                continue
    return filename

#AUDIO RECORDING SETUP
timeSleep = 1

sampleFormat = pyaudio.paInt16  # 16 bits per sample (32 too much, 8 too little)
sampleRate = 44100  # Record at 44100 samples per second

#record a chunck for every sleep (no data lost in sleeping because it waits for all the chunk to be created). It is necesssary to have a chunk a little bigger than the timeSleep
#becuase the rest of the program takes time (so having a chunk of the exact size would result in a loss of multiple milliseconds every loop). The chunk should also not so big to
#avoid slowing every loop too much. A loop takes 50ms in the worst case, so 1.25 is a good multiplier for timeSleep greater than 200ms
chunk = int(1.25*timeSleep*sampleRate)
audioFrames = []  #array where to store audio data during recording

portAudio = pyaudio.PyAudio()
stream = portAudio.open(format = sampleFormat, #stream created also if not used
                        channels = 1,
                        rate = sampleRate,
                        frames_per_buffer = chunk,
                        input = True)

def saveAudio(filename, portAudio, sampleFormat, sampleRate, audioFrames):
    wf = wave.open(filename+".wav", 'wb')  #open file to write
    wf.setnchannels(1)
    wf.setsampwidth(portAudio.get_sample_size(sampleFormat))
    wf.setframerate(sampleRate)
    wf.writeframes(b''.join(audioFrames))
    wf.close()

#SAVES TXT BACKUP AND FINAL SAVE
oldNumberOfRecognitions = chrome.execute_script('return numberOfRecognitions')  #placeholders (same value as in the js script)
currentFileName = ""
backupAudio = None

def closeBackupAudio():
    global backupAudio
    if(backupAudio):  #returns True if not None. Closes backup audio file
        backupAudio.close()
    backupAudio = None

atexit.register(closeBackupAudio)  #close backup audio file if closed without normal waiting

while(True):

    try:  #check if browser was closed. If so, end everything
        chrome.current_url
    except WebDriverException:
        break

    if(chrome.execute_script('return fastQuitRequest')):  #exit without waiting for selenium to decide so. The user asked
        break

    recognitionDefined = chrome.execute_script('return recognitionDefined')  #get definition variable from js
    numberOfRecognitions = chrome.execute_script('return numberOfRecognitions')
    recordAudio = chrome.execute_script('return recordAudio')

    if(recognitionDefined):  #everything is defined to start a new recognition
        if(oldNumberOfRecognitions != numberOfRecognitions):  #the recognition has started
            currentFileName = createTxtFile()
            oldNumberOfRecognitions = numberOfRecognitions  #just using +1 may cause discrepancies
            lastAudioSaveTime = time.time()

            if(recordAudio):

                closeBackupAudio()  #if for some reason the previous one was not closed

                backupAudio = wave.open(currentFileName+".wav", 'wb')  #open backup file to write (same settings as the normal one)
                backupAudio.setnchannels(1)
                backupAudio.setsampwidth(portAudio.get_sample_size(sampleFormat))
                backupAudio.setframerate(sampleRate)

    else:
        oldNumberOfRecognitions = numberOfRecognitions  #if there was a page reload, the old number would have been outdated (when reloaded, no recognition is defined)

    recognitionStarted = chrome.execute_script('return recognitionStarted')  #get if the recognition is in progress
    recognitionEnded = chrome.execute_script('return recognitionEnded')  #get if the recognition ended

    if(recognitionStarted and os.path.exists(currentFileName+".txt")):  #there is a rare case when recognitionStarted is True but the file is not created yet

        file = open(currentFileName+".txt", "w", encoding='utf8', errors="ignore")  #write the current results
        currentResult = chrome.find_element(By.ID, "results").text
        file.write(currentResult)
        file.close()

        shutil.copy(currentFileName+'.txt', currentFileName+'_backup.txt')  #create with overwrite a backup of the file in case the next writing goes bad

        if(recordAudio):
            audioData = stream.read(chunk)  #reads only last chunk, does not matter when stream started. Waits for all chunk to be created
            audioFrames.append(audioData)
            backupAudio.writeframes(b''+audioData)  #write single chunk to backup audio file

    if(recognitionEnded and recordAudio and not (len(audioFrames) == 0)):  #recognition ended, audio was recorded and it is not saved completely (only backup)
        closeBackupAudio()

        saveAudio(currentFileName+"_backup", portAudio, sampleFormat, sampleRate, audioFrames)
        audioFrames = []  #reset last recording

    time.sleep(timeSleep)  #sleep to use less CPU

if(not (len(audioFrames) == 0)):  #save before quitting if not already done
    saveAudio(currentFileName+"_backup", portAudio, sampleFormat, sampleRate, audioFrames)

closeBackupAudio()

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
portAudio.terminate()

chrome.quit()
