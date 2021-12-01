import datetime
import sounddevice as sd
from scipy.io.wavfile import write
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pygame
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

def download_and_play(channel):
	## Access Drive
	gauth = GoogleAuth()    
	drive = GoogleDrive(gauth)

	gauth.LoadCredentialsFile("credentials.txt") #so we don't have to log in every time

	## List out the files in the folder

	file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1DFuq54zgnPkIpoLeQaQd4dO3iH6_o69l')}).GetList()
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
		file['parents'] = [{'kind': 'drive#parentReference', 'id':'10lfu4-EFf9njNIgy0x8uXMVJG2YLfBnD'}]
		file.Upload() #updates the file with new parent information

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 12 to be an input pin and set initial value to be pulled low (off)
 
GPIO.add_event_detect(12,GPIO.RISING,callback=download_and_play) # Setup event on pin 12 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up		