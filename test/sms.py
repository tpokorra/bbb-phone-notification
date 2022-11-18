import requests

url="https://gateway.sms77.io/api/sms"
apikey="<api key>"

recipient="<recipient phone number>"

message = "<my message>"
response = requests.post(url=url, headers={'Authorization': f'basic {apikey}'},
    data={'to':recipient, 'text':message, 'from':'<sender phone number>'})

print(response)
print(str(response.content))