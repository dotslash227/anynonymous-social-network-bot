import requests
import json

base_url = "https://api.telegram.org/bot808378125:AAEJxb5qJdSugysaGzxxHRsEQLDho-lcbcs/"
users = {}
approved_emails = ["infosys.com", "tcs.com", "mauna.ai"]

def main():
    try:
        updates = requests.get("https://api.telegram.org/bot808378125:AAEJxb5qJdSugysaGzxxHRsEQLDho-lcbcs/getUpdates")
    except:
        print ("could not connect to telegram")
    else:
        updates = updates.json()
        # print (updates)
        for each in updates["result"]:
            uid = each["message"]["from"]["id"]
            if uid in users.keys():
                replyToUser(each, uid)
            else:
                users[uid] = 0        
                replyToUser(each, uid)


def replyToUser(data, uid):
    step = users[uid]    
    name = data["message"]["from"]["first_name"]
    try:
        last_name = data["message"]["from"]["last_name"]
    except:
        pass
    else:
        name = name + " " + last_name
    url = base_url + "sendMessage" 

    # Checking user steps
    if step == 0:
        message = "Hi %s, let's get you into the anonymous social network, let's start by knowing your company email address %s" % (name, step)
    if step == 1:
        message = "Cool. I have sent you a secret password to your email address, please check and let me know the secret password for me to allow you in. %s" % step
    if step == 2:  
        message = "We have got your email address, and we will be adding you your company's anonymous channel. You will receive a confirmation shortly %s" % step

    try:
        data = {
            "chat_id": data["message"]["chat"]["id"],
            "text": message 
        }
        send_message = requests.post(url, data)
    except:
        print ("Could not send message")
    else:
        users[uid] += 1
        print ("replies sent")


main()        