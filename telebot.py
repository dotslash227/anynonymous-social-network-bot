import requests
import psycopg2

base_url = "https://api.telegram.org/957095282:AAEzEqfTEhCk4LiHUyReCbppeOmsTDAGXXY/"
users = {}
already_replied = []
approved_emails = ["infosys.com", "tcs.com", "mauna.ai"]

def main(conn):    
    cur = conn.cursor()    
    try:
        updates = requests.get("https://api.telegram.org/957095282:AAEzEqfTEhCk4LiHUyReCbppeOmsTDAGXXY/getUpdates")
    except:
        print ("could not connect to telegram")
    else:
        updates = updates.json()        
        for each in updates["result"]:
            uid = each["message"]["from"]["id"]
            username = each["message"]["from"]["username"]                        
            cur.execute("SELECT id, username, step FROM users WHERE id=%s;" % uid)
            user = cur.fetchone()    
            if user is None:
                cur.execute("INSERT INTO users(id, username, step) VALUES (%s, %s, %s);",(uid, username, 0))
                conn.commit()                                                                        
                cur.execute("SELECT id, username, step FROM users WHERE id=%s;" % uid)
                user = cur.fetchone()    
            replyToUser(each, user, conn)


def replyToUser(data, user, conn):
    cur = conn.cursor()
    step = user[2]    
    name = data["message"]["from"]["first_name"]
    try:
        last_name = data["message"]["from"]["last_name"]
    except:
        pass
    else:
        name = name + " " + last_name
    url = base_url + "sendMessage" 


    # Check if the update is already replied to, if it is, don't send a message
    cur.execute('SELECT "updateId", "userId" FROM replies WHERE "updateId"=%s;' % user[0])
    replied = cur.fetchone()
    if replied is not None:
        print ("nothing to do here")        
    else:
        if step == 0:
            message = "Hi %s, let's get you into the anonymous social network, let's start by knowing your company email address %s" % (name, step)
        if step == 1:
            message = "Cool. I have sent you a secret password to your email address, please check and let me know the secret password for me to allow you in. %s" % step
        if step == 2:  
            message = "We have got your email address, and we will be adding you your company's anonymous channel. You will receive a confirmation shortly %s" % step            

        step = step + 1
        cur.execute('UPDATE users SET step=%s WHERE id=%s;', (step, user[0]))
        conn.commit()
        cur.execute('INSERT INTO replies("updateId", "userId") VALUES (%s, %s);', (data["update_id"], user[0]))
        conn.commit()

        print ("still message has to be sent")

        try:            
            data = {
                "chat_id": data["message"]["chat"]["id"],
                "text": message 
            }
            send_message = requests.post(url, data)
        except Exception as e:
            print ("Could not send message")
            print (str(e))
        else:            
            print ("replies sent")


try:    
    conn = psycopg2.connect(host="localhost", database="anonymous_network", user="anonymous_network", password="dillirox@123")
except Exception as e:
    print ("could not connect to db")
    print (e)
else:
    print ("db connection established")
    main(conn)