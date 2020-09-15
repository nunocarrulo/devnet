from __future__ import print_function
from datetime import datetime
from time import mktime, time, strftime
import sys, requests, json, web, time
import threading
from constants import *
from webexteamssdk import WebexTeamsAPI, Webhook
from WebexTeamsOps import *
from ngrokwebhook import *

def initVars():
	"""[Main variable initialisation]
	"""
	global app, api, myRoomID, siteURL, relativeURL, teams, me
	
	#TODO read from file in the future
	teams = {
		'INFRA-T1' : ['aleegoro', 'ayaroven','dposadov','dokowals', 'fbembeni', 'hkhambat','kmlynarc','mdemydch','nayere','tzubel', 'vtipiris'], 'INFRA-T2':['nbras','yohasan'], 
		'INFRA-T3':['kciszews'], 'SE-T1':['fszalaj','abohatiu','lrychlik','kjedrol','mikrupin'],'SE-T2':['pzawadzk'],'SE-T3':['kwianeck'], 
		'INFRA-IM':['tmitroul','jofioren']
		}
	
	urls = ('/events', 'webhook')				# Your Webex Teams webhook should point to http://<serverip>:8080/events
	app = web.application(urls, globals())		# Create the web application instance
	api = WebexTeamsAPI(access_token=bot['token'])	# Create the Webex Teams API connection object with bot token

	me = api.people.me()		# me = bot
	# find bot Rooms that contains a specific name
	#roomName = 'Bot Test nbras'
	#myRoomID = findMyRoom(api, roomName)
	#print("MyRoomID:{}".format(myRoomID))

class webhook(object):
	
	def POST(self):
		"""Respond to inbound webhook JSON HTTP POSTs from Webex Teams."""
		
		json_data = web.data()		# Get the POST data sent from Webex Teams
		#print("\nWEBHOOK POST RECEIVED:")
		#print(json_data, "\n")

		webhook_obj = Webhook(json_data)					# Create a Webhook object from the JSON data
		room = api.rooms.get(webhook_obj.data.roomId)		# Get the room details
		message = api.messages.get(webhook_obj.data.id)		# Get the message details

		# Ignore messages bot itself sent
		if message.personId == me.id:
			return 'OK'
		else:	# Message was sent by someone else; parse message and respond.
			person = api.people.get(message.personId)			# Get the sender's details
			
			print("NEW MESSAGE IN ROOM '{}'".format(room.title))
			print("FROM '{}'".format(person.displayName))
			print("MESSAGE '{}'\n".format(message.text))

			#Test message sent
			#response = 'Message received {}'.format(mention(person.emails[0]))		
			#api.messages.create(room.id, markdown=response)
			actionSelector(api, message, teams)				#Depending on message defines action to perform		
			
		return 'OK'

def main():
	initVars()
	
	#creds=getSPCreds()			# Obtain SP creds
	#df = openShiftPlan(creds)	# Access and obtain ShiftPlan
	#today = datetime.today()
	#findTodayRow(df, today)

	deleteWebhooksbyName(api, name=WEBHOOK_NAME) 	# Delete my existing webhooks
	public_url = getNgrokPublicUrl()				# Create web_hook if ngrok tunnel open
	if public_url is not None:
		createNgrokWebhook(api, public_url, me)
	try:
		print ("Starting web server...",end='')
		webserver = threading.Thread(target=app.run(), args=(1,))
		webserver.start()
	except Exception as e:
		print ("WebServer Error {}".format(e))
		
if __name__ == "__main__":
    main()
