import os
from oauth2client import file
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pydub
import pygame
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

filename = f"{datetime.datetime.now().month}-{datetime.datetime.now().day}-{datetime.datetime.now().year}_{datetime.datetime.now().hour}.{datetime.datetime.now().minute}-cm1"
file_ready = False

## Record audio
    #Used this resource for help with this code: https://realpython.com/playing-and-recording-sound-python/#conclusion-playing-and-recording-sound-in-python
    #Also https://python-sounddevice.readthedocs.io/en/latest/usage.html#recording
def record_audio(channel):
	print("Recording...")
	fs = 44100 #records at 44100 samples per second
	duration = 5 #seconds --> This will change later but for Alpha Prototype 1 will stay as 5 seconds

	myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
	sd.wait()
	filename = f"{datetime.datetime.now().month}-{datetime.datetime.now().day}-{datetime.datetime.now().year}_{datetime.datetime.now().hour}.{datetime.datetime.now().minute}-cm1"

	wav_filename = filename + ".wav"
	write(wav_filename, fs, myrecording)

	sound = pydub.AudioSegment.from_wav(wav_filename)
	sound.export(filename + ".mp3", format = "mp3")
	os.remove(filename + ".wav")

	print (filename + ".mp3")

	#so it plays it back immediately after user records it 
	pygame.mixer.init()
	pygame.mixer.music.load(filename + ".mp3")
	pygame.mixer.music.play()

	while pygame.mixer.music.get_busy() == True:
		continue 

	global file_ready
	file_ready = True

#if button is pressed then upload it to google drive
def upload_button(channel):

	global file_ready
	if not file_ready:
		print("No file ready to upload")
		return

	gauth = GoogleAuth()           
	drive = GoogleDrive(gauth)
	gauth.LoadCredentialsFile("credentials.txt") #this allows us to not have to log in every time
	upload_file_list = [filename + ".mp3"]

	for upload_file in upload_file_list:
		print (f"Uploading file {upload_file}...")
		gfile = drive.CreateFile({'parents': [{'id': '1DFuq54zgnPkIpoLeQaQd4dO3iH6_o69l'}]})
		# Read file and set it as the content of this instance.
		gfile.SetContentFile(upload_file)
    	# Upload the file
		gfile.Upload()
		print("File uploaded.")

	file_ready = False


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 38 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #set pin 40

GPIO.add_event_detect(38,GPIO.RISING,callback=upload_button) # Setup event on pin 38 rising edge
GPIO.add_event_detect(40,GPIO.RISING,callback=record_audio) # Setup event on pin 40 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up

#Delete from Raspberry pi (CronJob) this will delete all things that have cm1 (can run daily)
#CronJob also can have the program run every 10 minutes