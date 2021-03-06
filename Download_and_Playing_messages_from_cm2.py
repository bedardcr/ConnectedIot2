import datetime
import sounddevice as sd
from scipy.io.wavfile import write
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pygame
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

def download_and_play(channel):
	print(f"brew {time.time()}")
	## Access Drive
	gauth = GoogleAuth()           
	drive = GoogleDrive(gauth)

	gauth.LoadCredentialsFile("credentials.txt") #so we don't have to log in every time

	## List out the files in the folder

	file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1ywQqK_uGBJfJAaOMXFf_o3Z3_7jaRSLK')}).GetList()
	for file in file_list:
		print('title: %s, id: %s' % (file['title'], file['id']))

	## Download and play avalible files
	# 	the code downloads and then plays the file and loops until all files are downloaded and played

	for i, file in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
		print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list)))
		file.GetContentFile(file['title'])
		pygame.mixer.init()
		pygame.mixer.music.load(file['title'])
		pygame.mixer.music.play()

		while pygame.mixer.music.get_busy():
			continue

		print(file['id']) #this prints out the file id for each file

		#changes the parent folder (what folder it is in) to the new folder
		file['parents'] = [{'kind': 'drive#parentReference', 'id':'1qBVNyf0I10AB66xKtKKUsKsArHP2oQWt'}]
		file.Upload() #updates the file with new parent information

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 26 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 24 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 22 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(26,GPIO.RISING,callback=download_and_play) # Setup event on pin 26 rising edge
GPIO.add_event_detect(24,GPIO.RISING,callback=download_and_play) # Setup event on pin 24 rising edge
GPIO.add_event_detect(22,GPIO.RISING,callback=download_and_play) # Setup event on pin 22 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up		