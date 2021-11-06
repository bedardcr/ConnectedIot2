from pydrive.auth import GoogleAuth
import os

os.remove("credentials.txt")

## Access Drive
gauth = GoogleAuth()    
gauth.LocalWebserverAuth()
gauth.SaveCredentialsFile("credentials.txt")