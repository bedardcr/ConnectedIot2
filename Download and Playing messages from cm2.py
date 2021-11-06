from playsound import playsound
import datetime
import sounddevice as sd
from scipy.io.wavfile import write
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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
	playsound(file['title'])

	print(file['id']) #this prints out the file id for each file

	#changes the parent folder (what folder it is in) to the new folder
	file['parents'] = [{'kind': 'drive#parentReference', 'id':'1qBVNyf0I10AB66xKtKKUsKsArHP2oQWt'}]
	file.Upload() #updates the file with new parent information