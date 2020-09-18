from bs4 import BeautifulSoup
import requests
import colors   as c

url = 'https://www.192-168-1-1-ip.co/default-usernames-passwords/'
ajax = 'https://www.192-168-1-1-ip.co/ajaxData.php'
headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
}

session = requests.Session()
session.head('https://www.192-168-1-1-ip.co/default-usernames-passwords')   # this one only works without the final slash
response = session.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
#debug: print(response) # status code

def get_router(brand, model):
    global soup
    global ajax
    global session
    global headers
    
    # just to confirm the params integrity, printing them
    #debug: print(f"==> options: brand: {brand}")
    #debug: print(f"==> options: model: {model}")

    ################
    brand_id  = None
    model_id  = None
    routers = [] # stores all results in this list
    # groups all routers (name : id)
    for option_tag in soup.findAll('option'):
        if 'Select' not in option_tag.text:  # remove the "select message"
            new_router = dict()
            new_router['tag_name'] = option_tag.text        # raw HTML router name
            new_router['tag_value'] = option_tag['value']   # numeric sequential ID
            routers.append(new_router)

    # verify brand name (called brand_id by site's ajax, so yeah, confusing)
    for item in routers:
        if brand == item['tag_name']:
            brand_id = item['tag_value']
            #debug: print(f"* search brand: {brand}")
            #debug: print(f"* set brand_id: {brand_id}")
    
    # make an ajax request and get models
    # then, search for requests model
    
    r = session.post(ajax, data=dict(brand_id=brand_id), headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')  # set new soup for this response (model list)
    models = []

    for option_tag in soup.findAll('option'):
        if 'Select' not in option_tag.text:
            new_model = dict()
            new_model['tag_name'] = option_tag.text
            new_model['tag_value'] = option_tag['value']
            models.append(new_model)

    # TESTING STUFF HERE
    #debug: print(f"* AJAX request status: {r}") # test status
    #debug: print(c.yellow("--> MODELS: "))
    #debug: for item in models:
    #debug:        print(item)

    for item in models:
        if model == item['tag_name']:
            model_id = item['tag_value']
            #debug: print(f"* search brand: {model}")
            #debug: print(f"* set model_id: {model_id}")

    payload = dict(brand_id=brand_id, model_id=model_id)
    #debug: print(c.green(f"* success: payload set: {payload}"))
    
    session.close()
    return payload

