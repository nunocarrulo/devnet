from __future__ import print_function
from datetime import datetime
from time import mktime, time, strftime
import sys, requests, json, web, time
import threading
from webexteamssdk import WebexTeamsAPI, Webhook
from WebexTeamsOps import *
from ngrokwebhook import *
import pandas as pd
from getpass import getpass

def initVars():
	"""[Main variable initialisation]
	"""
	global bot, app, api, myRoomID, shiftPlanURL, siteURL, relativeURL
	bot = {'id' : 'Y2lzY29zcGFyazovL3VzL0FQUExJQ0FUSU9OLzhmMjUzMWE4LTkwYmUtNGVjMS1iNzAzLWY2YzdjYzA0MTFmMw', 'token' : 'MWE4ZGE2OTctYzVjYS00Y2JhLWExMWUtNTI2MTk1ZDZlZGIxMzEyNmE4MzMtYmE3_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'}
	team = {'Alexander Egorov': 'aleegoro', 'Nosa Ayere':'nayere', 'Mariia Demydchenkova':'mdemydch', 'Filip Bembenik':'fbembeni', 'Hussain Khambaty':'hkhambat', 'Denys Posadovskyi':'dposadov', \
	'Karol Mlynarczyk':'kmlynarc', 'Dobieslaw Kowalski':'dokowals', 'Tomasz Zubel':'tzubel', 'Sivendra Tipirisetty':'vtipiris', 'Artem Yarovenko':'ayaroven', 'Yosef Hasan':'yohasan', \
	'Nuno Bras':'nbras', 'Kamil Ciszewski':'kciszews'}
	roomName = 'nbras'
	
	urls = ('/events', 'webhook')				# Your Webex Teams webhook should point to http://<serverip>:8080/events
	app = web.application(urls, globals())		# Create the web application instance
	api = WebexTeamsAPI(access_token=bot['token'])	# Create the Webex Teams API connection object with bot token
	
	# find bot Rooms that contains a specific name
	myRoomID = findMyRoom(api, roomName)

def get_catfact():
    """Get a cat fact from catfact.ninja and return it as a string.
    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.
    """
    response = requests.get(CAT_FACTS_URL, verify=False)
    response.raise_for_status()
    json_data = response.json()
    return json_data['fact']

class webhook(object):
	
	def POST(self):
		"""Respond to inbound webhook JSON HTTP POSTs from Webex Teams."""
		# Get the POST data sent from Webex Teams
		json_data = web.data()
		print("\nWEBHOOK POST RECEIVED:")
		print(json_data, "\n")

		# Create a Webhook object from the JSON data
		webhook_obj = Webhook(json_data)
		# Get the room details
		room = api.rooms.get(webhook_obj.data.roomId)
		# Get the message details
		message = api.messages.get(webhook_obj.data.id)
		# Get the sender's details
		person = api.people.get(message.personId)

		print("NEW MESSAGE IN ROOM '{}'".format(room.title))
		print("FROM '{}'".format(person.displayName))
		print("MESSAGE '{}'\n".format(message.text))

		sender = person.displayName
		senderID = person.id
		senderEmail = person.emails[0]
		cec = senderEmail.split('@')[0]
		# This is a VERY IMPORTANT loop prevention control step.
		# If you respond to all messages...  You will respond to the messages that the bot posts and thereby create a loop condition.
		me = api.people.me()
		if message.personId == me.id:
			# Message was sent by me (bot); do not respond.
			return 'OK'

		else:	# Message was sent by someone else; parse message and respond.
			response = 'Message received {} {}'.format(sender, mention(senderEmail))
			api.messages.create(room.id, markdown=response)
			
			
			if "/CAT" in message.text:
				print("FOUND '/CAT'")
				# Get a cat fact
				cat_fact = get_catfact()
				print("SENDING CAT FACT '{}'".format(cat_fact))
				# Post the fact to the room where the request was received
				api.messages.create(room.id, text=cat_fact)
		return 'OK'

def main():
	initVars()
	creds=('nbras@cisco.com','')
	while (not mypwd):
		creds[1] = getpass("SP Password:")
	
	# Post a message to the new room
	#api.messages.create(myRoomID, text="Welcome to the room!")
	
	df = openShiftPlan(creds)	# Access and obtain ShiftPlan

	today = datetime.today()
	findTodayRow(df, today)
	sys.exit()

	deleteWebhooksbyName(api, name=WEBHOOK_NAME) # delete my existing webhooks
	#Create web_hook if ngrok tunnel open
	public_url = get_ngrok_public_url()
	if public_url is not None:
		createNgrokWebhook(api, public_url)
	try:
		webserver = threading.thread(target=app.run(), args=(1,))
		webserver.start()
		print ("Web Server started")
	except exception as e:
		print ("WebServer Error {}".format(e))
		
if __name__ == "__main__":
    main()
