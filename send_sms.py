import sqlite3
import requests
from bigbluebutton_api_python import BigBlueButton
import settings

def isMeetingRunning(bbb, meetingId):
    response = bbb.is_meeting_running(meetingId)
    if settings.verbose:
        print(response)
    if response.get_field('returncode') == 'SUCCESS':
        if response.get_field('running') == 'true':
            if settings.verbose:
                print(f"Meeting {meetingId} is running")
            return True
        else:
            if settings.verbose:
                print(f"Meeting {meetingId} is not running")
            return False
    else:
        print("cannot connect to BBB API")
    return False

def getPhoneNumberAndCode(bbb, meetingId):
    response = bbb.get_meeting_info(meetingId)
    if response.get_field('returncode') == 'SUCCESS':
        m = response['xml']
        return (m['dialNumber'], m['voiceBridge'])
    return (None, None)

def connectDB(db_file_name):
    # Connect to the sqlite database
    sq3 = sqlite3.connect(db_file_name)
    sq3.execute("""
CREATE TABLE IF NOT EXISTS Notified (
id INTEGER PRIMARY KEY AUTOINCREMENT,
recipient_number VARCHAR(100),
phone_code VARCHAR(20),
t TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    return sq3

def hasBeenNotifiedWithinLastHour(sq3, recipient_number, phone_code):
    sql = "SELECT * FROM Notified WHERE recipient_number = ? and phone_code = ? and datetime(t) >= datetime('now', '-1 Hour')"
    cursor = sq3.cursor()
    cursor.execute(sql, (recipient_number, phone_code,))
    row = cursor.fetchone()
    if row is None:
      return False
    return True

def setHasBeenNotified(sq3, recipient_number, phone_code):
    sql = "INSERT INTO Notified(recipient_number, phone_code) VALUES(?, ?)"
    cursor = sq3.cursor()
    cursor.execute(sql, (recipient_number, phone_code,))
    sq3.commit()

def notifyPerSMS(sq3, bbb_phone_number, bbb_phone_code):
    message = settings.message. \
            replace("MEETING_URL", settings.meetingUrl). \
            replace("MEETING_PWD", settings.meetingPwd). \
            replace("BBB_PHONE_NUMBER", bbb_phone_number). \
            replace("BBB_PHONE_CODE", bbb_phone_code)

    for recipient in settings.sms_recipients:
        if not hasBeenNotifiedWithinLastHour(sq3, recipient, bbb_phone_code):
            response = requests.post(url=settings.sms_api_url, headers={'Authorization': f'basic {settings.sms_api_key}'},
                data={'to':recipient, 'text':message, 'from':settings.sms_from})
            #print(response)
            print(str(response.content))
            if (str(response.content) == "b'100'"):
                setHasBeenNotified(sq3, recipient, bbb_phone_code)



bbb = BigBlueButton(settings.bbb_api_url, settings.bbb_api_key)
sq3 = connectDB(settings.sqlite_db_file)

if isMeetingRunning(bbb, settings.meetingId):
    (bbb_phone_number, bbb_phone_code) = getPhoneNumberAndCode(bbb, settings.meetingId)
    if bbb_phone_number and bbb_phone_code:
        notifyPerSMS(sq3, bbb_phone_number, bbb_phone_code)

