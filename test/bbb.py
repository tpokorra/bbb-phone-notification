from bigbluebutton_api_python import BigBlueButton

meetingName = '<My Meeting Name>'
meetingId = '<Meeting ID>'
meetingPwd = '<Meeting Pwd>'
bbb_api_url = '<BBB API URL>'
bbb_api_key = '<BBB API KEY>'

b = BigBlueButton(bbb_api_url, bbb_api_key)

def showMeetingDetails(m):
    print(m)
    print (f"{m['meetingName']} {m['meetingID']} running: {m['running']}")
    print (f"Phone number: {m['dialNumber']} PIN: {m['voiceBridge']}")
    if 'attendee' in m['attendees']:
        attendees = m['attendees']['attendee']
        if not isinstance(attendees, list):
            attendees = (attendees,)
        print (f"number of attendees: {len(attendees)}") # see also m['participantCount']?
        for attendee in attendees:
            #print (attendee)
            print (f"{attendee['clientType']} {attendee['fullName']}")

def showMeetingStatus(meetingId):
    response = b.is_meeting_running(meetingId)
    print(response)
    if response.get_field('returncode') == 'SUCCESS':
        if response.get_field('running') == 'true':
            print(f"Meeting {meetingId} is running")
            return True
        else:
            print(f"Meeting {meetingId} is not running")
            return False
    else:
        print("cannot connect to BBB API")
    return False

# Problem: meeting is started, but not active, since nobody joined yet.
# Problem: Meeting Name is N.N.
def startMeeting(meetingId, meetingName):
    print("starting the meeting:")
    params = {}
    params["meetingExpireIfNoUserJoinedInMinutes"] = 10
    params["meetingExpireWhenLastUserLeftInMinutes"] = 5
    params["meetingName"] = meetingName
    meta = {}
    meta["meetingName"] = meetingName

    print(b.create_meeting(meetingId, params=params, meta=meta))


action = 3

if action == 1:
    # get api version
    print(f"API Version: {b.get_api_version().get_version()}")
elif action == 2:
    response = b.get_meetings()
    #print(response)
    print('get_meetings: ')
    if response.get_field('returncode') == 'SUCCESS':
        meetings = response.get_field('meetings')
        for m in meetings:
            #print (meetings[m]
            showMeetingDetails(meetings[m])
elif action == 3:
    print('info about one specific meeting')
    #if showMeetingStatus(meetingId):
    response = b.get_meeting_info(meetingId)
    if response.get_field('returncode') == 'SUCCESS':
        showMeetingDetails(response['xml'])
elif action == 4:
    '''
    start meeting if it is not running yet
    '''
    if not showMeetingStatus(meetingId):
        startMeeting(meetingId, meetingName)

elif action == 5:
    '''
    stop the meeting
    '''
    print(b.end_meeting(meetingId, meetingPwd))


# print(b.join({'fullName': 'Myself','meetingID': meetingId,'password': meetingPwd, 'role':'VIEWER'}))
#join_url = b.get_join_meeting_url('Myself', meetingId, meetingPwd)
#print(f"join_url: {join_url}")
#x = requests.get(join_url)
#print("response of getting join_url: ")
#print(x.content)





