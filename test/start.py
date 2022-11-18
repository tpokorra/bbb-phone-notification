# attempt to join a meeting via simulating accessing the website, with Nextcloud integration
# but I could not get that to work with all the redirects

import requests
import re

url="https://cloud.example.org/index.php/apps/bbb/b/<some ID>"
pwd="<the password>"
user="TestUser"

response = requests.get(url=url, params = {'password': pwd, 'displayname': user})
print(response)
#print(response.content)
#print()
#print()
m = re.search(r'<a href="https://bbbapiproxy.hostsharing.net/([^"]*)"', str(response.content))
redirect = m.group(1)
if redirect:
    redirect = f"https://bbbapiproxy.hostsharing.net/{redirect}"
    #redirect = redirect.replace("userdata-bbb_listen_only_mode=false", "userdata-bbb_listen_only_mode=true")
    #redirect = redirect.replace("redirect=true", "redirect=false")

if redirect:
    print(redirect)
    response = requests.get(url=redirect)
    print(response)
    print(response.content)


