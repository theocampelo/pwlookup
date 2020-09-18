from bs4 import BeautifulSoup
import requests
import pprint
import json
import options as o
import colors  as c

# 192-168-1-1-ip.co

url = 'https://www.192-168-1-1-ip.co/ajaxData.php'
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
}


# DATA HANDLING
# TODO: set this to be argparsing later
brand = '1net1'
model = 'R-90'

# testing options method
#debug: print(f"* sent: {brand:10} {model}")
print(f"* source: {url.rstrip('ajaxData.php')}")
print(f"* searching for {brand} {model}...")
payload = o.get_router(brand, model)

# SESSION HANDLING
session = requests.Session()
session.head('https://www.192-168-1-1-ip.co/default-usernames-passwords/')

# POST REQUEST AND DATA
response = session.post(url, data=payload, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# by now you have the final HTML data
#debug: print(c.green(f"* final status code: {response}"))
#debug: print(soup.prettify())

# formatting results in dict items
results = dict()
for row in soup.findAll('tr'):
    aux = row.findAll('td')
    key = str(aux[0].string).replace('\n','')
    val = str(aux[1].string).replace('\n','')
    results[key] = val

# print results
print(c.green(f"\n(!) common passwords found for {brand} {model}"))
for item in results.items():
    if item[0] != 'Manuals':    # implement manuals later (<a> tag)
        print(f"{item[0]:20} {item[1]}")

print(c.green("\nDone, exiting..."))
session.close()