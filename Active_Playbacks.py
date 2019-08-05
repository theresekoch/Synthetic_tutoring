import os
import random
import time
from gpiozero import Button
import pygame
from datetime import datetime
from datetime import date
import schedule

#initialize sound mixer module
pygame.mixer.init()

song='/home/pi/Stim_for_test/ZF/B255/norm_B255_42858.46940484_5_3_13_2_20.wav'
BirdID='TEST'

switch1 = Button(2)

def checkEnd(end_of_session, dailyFile):
    if time.time() > end_of_session:
        if not dailyFile.closed:
            dailyFile.write("The session could not be completed before time out")
            dailyFile.close()
        print("session complete")

def keyPress(song, dailyFile, counter):
    print('[' + str(counter) + ']   ' + str(datetime.now().time()) +'   '+ song)
    s=pygame.mixer.Sound(song)
    s.play()
    dailyFile.write('[' + str(counter) + ']    ' + str(datetime.now().time())+ '    '+song +'\n')
        #This will get the song duration and pause the program for the duration
            ## of the song so that it can't play two at once
    songDuration= s.get_length()
    time.sleep(songDuration)

def morning_session():
    #this creates a file that will record all playbacks and their time stamps.
    #it will do this in a new file called 'birdID_date' in the folder /home/pi/BirdID.
    destinationFolder='/home/pi/'+ BirdID + '/'
    fileName= destinationFolder + BirdID + '_Morning_' + str(date.today())
    fileVersion=0
    fileNameWVersion= fileName+ '.txt'

    #this will check if the file already exists, and if it does, it will change the
    #name of the file to be created by adding a version number, so that no files
    #get overwritten if the program is run multiple times in the same day
    while os.path.exists(fileNameWVersion):
        fileVersion=fileVersion+1
        fileNameWVersion=fileName+'_'+str(fileVersion)+'.txt'
    dailyFile=open(fileNameWVersion, "w+")
    dailyFile.write('Active Playbacks   ' + song + '    ' + str(datetime.now().time())+'\n')

    print("Starting morning session... "+str(datetime.now().time())+'\n')
    counter = 1
    end_of_session=time.time()+2*60*60
    
    while time.time() < end_of_session and counter <= 10:
        if switch1.is_pressed:
            keyPress(song, dailyFile, counter)
            counter=counter+1
            switch1.wait_for_release()
    dailyFile.close()
    print("Morning session complete " + '\n')
    

def afternoon_session():
    destinationFolder='/home/pi/'+ BirdID + '/'
    fileName= destinationFolder + BirdID + '_Afternoon_' + str(date.today())
    fileVersion=0
    fileNameWVersion= fileName+ '.txt'

    #this will check if the file already exists, and if it does, it will change the
    #name of the file to be created by adding a version number, so that no files
    #get overwritten if the program is run multiple times in the same day
    while os.path.exists(fileNameWVersion):
        fileVersion=fileVersion+1
        fileNameWVersion=fileName+'_'+str(fileVersion)+'.txt'
    dailyFile=open(fileNameWVersion, "w+")
    dailyFile.write('Active Playbacks   ' + song + '    ' + str(datetime.now().time())+'\n')
    print("Starting afternoon session... "+str(datetime.now().time())+'\n')
    counter = 1
    end_of_session=time.time()+2*60*60 
    while counter <= 10 and time.time()<end_of_session:
        if switch1.is_pressed:
            keyPress(song, dailyFile, counter)
            counter=counter+1
            switch1.wait_for_release()
    dailyFile.close()
    print("Afternoon session complete."+'\n')

    
schedule.every().day.at("11:50").do(morning_session)
schedule.every().day.at("15:05").do(afternoon_session)
while True:
    schedule.run_pending()
    time.sleep(1)
