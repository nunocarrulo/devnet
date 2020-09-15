from webexteamssdk import WebexTeamsAPI, Webhook
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File 
import io, sys, constants, traceback
import pandas as pd
from datetime import datetime
from getpass import getpass

debug = False

# ======== Person ============
def findPerson(api, cec):
	personEmail=cec+'@cisco.com'
	people = api.people.list(email=personEmail)
	
	# returns the first person with specifc cec
	for person in people:
		print (person.displayName, person.id, person.emails[0], person.firstName, person.lastName)	
		return person

#============ Room ===============
def findMyRoom(api, roomName):
	all_rooms = api.rooms.list() # Obtain all rooms my bot has access
	myRooms = [room for room in all_rooms if roomName in room.title]
	#print(myRooms[0].title+'\t'+myRooms[0].id)
	
	return myRooms[0].id

#============= Messages =================
def mention(email):
	if '@cisco.com' in email:
		return '<@personEmail:{}>'.format(email)
	else:
		email+='@cisco.com'
		return '<@personEmail:{}>'.format(email)

def mentionGroup(emailList):
	mentionList=''
	for email in emailList:
		if '@cisco.com' in email:
			 mentionList+='<@personEmail:{}> '.format(email)
		else:
			email+='@cisco.com'
			mentionList+='<@personEmail:{}> '.format(email)
	#print ('Mention List: {}'.format(mentionList))
	return mentionList

def parseSelector(text=''):
	selector = ''
	if len(text) == 2:
		selector = text[1].strip().upper()
	elif len(text) >= 3:
		selector = text[1].strip().upper()
		text = msg.text.split(' ',2)[2]
	return selector,text

def actionSelector(api, msg, teams):
	try:
		selector,text = parseSelector (msg.text.split(' ',2))
		
		if debug:
			print ("Message received {}".format(msg))
			print ("Selector {}".format(selector))
		
		if selector == '':
			return		# Do nothing if no instructions were sent
		elif selector == 'HELP':
			help=' =============== Help Menu ===============\nINFRA-T1 - Sends a message mentioning all Infra T1 Engineers (same for T2 & T3) \nSE-T1 - Sends a message  mentioning all the SE T1 Engineers (same for T2 & T3)\n\
Infra-IMs - Sends a 1:1 message to each IM with the message'
			api.messages.create(msg.roomId, text=help)
		elif selector == 'INFRA-IMs':
			#unicast to IMs the message
			print("IMs")
		elif selector in teams:
			#print('@{}'.format(selector))
			api.messages.create(msg.roomId, markdown=mentionGroup(teams[selector]))
		else:
			print('Unidentified selector, no action will be taken')
	except Exception as e:
		#type, value, traceback = sys.exc_info()
		print ("Exception {}\nTraceback {}".format(e, traceback.print_exc()))

def listToString(list, separator=' '):
	return separator.join(list)

#============= Read Excel ================
def getSPCreds():
	creds=('nbras@cisco.com','')
	mypwd=''
	while (not mypwd):
		creds[1] = getpass("SP Password:")
	
	return creds

def openShiftPlan(creds):
	ctx_auth = AuthenticationContext(siteURL)
	if ctx_auth.acquire_token_for_user(creds[0], creds[1]):
		ctx = ClientContext(siteURL, ctx_auth)
		web = ctx.web
		ctx.load(web)
		ctx.execute_query()
		print ("Web title: {0}".format(web.properties['Title']))
	else:
		print (ctx_auth.get_last_error())

	response = File.open_binary(ctx, relativeURL)
	#print(ctx.service_root_url())
	#save data to BytesIO stream
	bytes_file_obj = io.BytesIO()
	bytes_file_obj.write(response.content)
	bytes_file_obj.seek(0) #set file object to start

	#read file into pandas dataframe
	return pd.read_excel(bytes_file_obj, sheet_name='Daily - Infra')

def findTodayRow(df, today):
	#print (df.columns.ravel())
	#print (df.info)
	myIndex = datetime.now().timetuple().tm_yday - 1
	for col,val in df.iloc[myIndex].items():
		print ('Col={}\nValue={}'.format (col,val))
	
	#print ((df.iloc[myIndex]))
	