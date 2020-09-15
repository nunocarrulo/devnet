from webexteamssdk import WebexTeamsAPI, Webhook
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File 
import io
import pandas as pd
from datetime import datetime

#Constants
relativeURL = '/sites/CMSDCOTKrakow/Shared Documents/Team Meeting Presentations/DCOT KRK Shift plan.xlsx'
siteURL = 'https://cisco.sharepoint.com/sites/CMSDCOTKrakow'
AM = '7:00 - 15:00'
PM = '12:00 - 20:00'
BH = '9:00 - 17:00'

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
	return '<@personEmail:{}>'.format(email)


#============= Read Excel ================
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
	