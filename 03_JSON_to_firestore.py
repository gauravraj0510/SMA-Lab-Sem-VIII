import datetime
import calendar
import time
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
import os
 
# Get the list of all files and directories
path = "MESSAGES"
channel_list = os.listdir(path)
# print(channel_list)

#authentication
cred = credentials.Certificate('service-key.json')
app = firebase_admin.initialize_app(cred)
DB = firestore.client()

ERROR_LOGS = []

discordRef = DB.collection(u'DISCORD')        

server = open('SERVER_DATA/01_WWG_Server_Details.json')
server_data = json.load(server)
print("Server details extracted from JSON!","\n")


# Update server details on Firebase DB
discordRef.document(server_data['name']).set(server_data)
print("Server details added!","\n")


for channel in channel_list:
    try:
        f = open('MESSAGES/'+channel)
        data = json.load(f)
        
        # Creating CHANNELS collection inside DISCORD collection
        channelRef = discordRef.document(server_data['name']).collection('CHANNELS')

        # Adding channel details
        channel_details = channel.split("-")
        channel_dict = {"channel_id":channel_details[0], "channel_name":channel_details[1][:len(channel_details[1])-5]}
        channelRef.document(channel[:len(channel)-5]).set(channel_dict)
        print("Channel added: ", channel[:len(channel)-5],"\n")

        # Creating MESSAGES collection inside each document of CHANNELS collection
        messageRef = channelRef.document(channel[:len(channel)-5]).collection('MESSAGES')
        print("Starting to add messages of: ", channel[:len(channel)-5])
        
        counter = 0
        for message in data:
            try:
                messageRef.document(str(message['id'])).set(message)
            except:
                print("Couldn't add message of channel:",channel[:len(channel)-5])
            # messageRef.document(str(message['id'])).set(message)
            counter += 1
            if counter%1000 == 0:
                print("1000 Messages added!")

    except:
        print("Error occured with: @", channel)
        ERROR_LOGS.append(channel)

print('\n')
print('=================ERROR HANDLES=================')
print(ERROR_LOGS)

