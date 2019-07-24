import os
import random
import time
from datetime import date
from datetime import datetime
import pygame
import schedule

#initialize sound mixer module
pygame.mixer.init()

song='/home/pi/Stim_for_test/ZF/B255/norm_B255_42858.46940484_5_3_13_2_20.wav'
BirdID='TEST'


#creates a function that generates minute time stamps for all playbacks.
    #minute_range is the time over which you want the plays spread, in minutes.
    #eg. if you want them to play over a 2 hour period, minute_range=120.
    #num_plays is the number of playbacks you want in that interval. 
def generate_times(minute_range, num_plays):
    rand_minutes=[0 for i in range(num_plays)]
    for i in range(num_plays):
        rand_minutes[i]=random.randint(0,minute_range)
    #creates a list of all unique times
    no_duplicates=[]
    [no_duplicates.append(x) for x in rand_minutes if x not in no_duplicates]
    #adds new time stamps and checks for duplicates until you have the desired number of unique times. 
    while len(no_duplicates) < num_plays:
        for i in range(num_plays-len(no_duplicates)):
            rand_minutes.append(random.randint(0, minute_range))
            [no_duplicates.append(x) for x in rand_minutes if x not in no_duplicates]
    no_duplicates.sort()
    start_time=time.time()
    #converts the numbers to times. 
    all_times=[x*60+start_time for x in no_duplicates]
    return(all_times)

#this will actually play the song file, and pause the program until the file is done.
#it also writes the time stamp at which the file is played into the dailyFile .txt file
def play_song(song, daily_file):
    s=pygame.mixer.Sound(song)
    s.play()
    daily_file.write(str(datetime.now().time())+'\n')
    songDuration=s.get_length()
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
    dailyFile.write('Passive Playbacks   ' + song + '    ' + str(datetime.now().time())+'\n')
    #generates the times at which the songs will be played
    all_times=generate_times(120,10)
    print("Starting morning session... "+str(datetime.now().time())+'\n')
    counter = 1
    for x in all_times:
        #waits for time specified in all_times to pass, then plays song and records it
            #in dailyFile
        while x > time.time():
            time.sleep(0.5)
        print('[' + str(counter) + '] '+ str(datetime.now().time()) + '\n')
        play_song(song, dailyFile)
        counter=counter+1
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
    dailyFile.write('Passive Playbacks   ' + song + '    ' + str(datetime.now().time())+'\n')
    all_times=generate_times(120,10)
    print("Starting afternoon session... "+str(datetime.now().time())+'\n')
    counter=1
    for x in all_times:
        while x > time.time():
            time.sleep(0.5)
        print('[' + str(counter) + '] '+ str(datetime.now().time()) + '\n')
        play_song(song, dailyFile)
        counter=counter+1
    dailyFile.close()
    print("Afternoon session complete."+'\n')


schedule.every().day.at("06:15").do(morning_session)
schedule.every().day.at("15:45").do(afternoon_session)
while True:
    schedule.run_pending()
    time.sleep(1)
    


