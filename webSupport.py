import requests
import json
import time

class WebSupport:

    url = 'https://python-brysen.c9users.io/'
    username = None
    authToken = None
    s = None

    def startSession():
        WebSupport.s = requests.Session()

    def get(url):
        return WebSupport.s.get(url).text

    def update(url, json):
        WebSupport.s.get(url, params={'update':json})

    def __import__():
        WebSupport.startSession()

    def buildData(**kwords):
        data = {"entities":kwords.get("entities", {}), "world":kwords.get("world", {})}
        return {"method":kwords.get("method", "None"),"data":json.dumps(data)}

    def buildRequests(lis = {}, *reqs):
        ret = []
        for item in reqs:
            ret.append(item)
        lis["requests"] = ret
        return lis

    def buildRequest(typ, **get):
        req = {"request_type":typ}
        for key in get:
            req[key] = get[key]
        return req

    def buildFile(**kwords):
        path = kwords.get("path", None)
        data = kwords.get("data", "")
        if path == None:
            return "Unknown Path"
        open(str(path), "w")

    def authenticate(username, password):
        req = {"method":"AUTHENTICATE","data":json.dumps({"username":username,"password":password})}
        return WebSupport.s.post(WebSupport.url, data=req)

    def login(username, password):
        req = {"method":"LOGIN","data":json.dumps({"username":username,"password":password})}
        ret = WebSupport.s.post(WebSupport.url, data=req)
        rett = json.loads(ret.text)
        if rett["login_status"] == True:
            WebSupport.username = username
            WebSupport.authToken = rett["authToken"]
        return ret

    def logout(username):
        req = WebSupport.__basicLogedInPacket__(method="LOGOUT", data = json.dumps({"username":username}))
        #req = {"method":"LOGOUT","data":json.dumps({"username":username})}
        return WebSupport.s.post(WebSupport.url, data=req)

    def createAccount(username, password):
        req = WebSupport.__basicPacket__(method="CREATEACCOUNT", data = json.dumps({"username":username,"password":password}))
        return WebSupport.s.post(WebSupport.url, data=req)

    def __basicLogedInPacket__(**kwords):
        lil = WebSupport.__basicPacket__(**kwords)
        lil["username"] = kwords.get("username", WebSupport.username)
        lil["authToken"] = kwords.get("authToken", WebSupport.authToken)
        return lil

    def __basicPacket__(**kwords):
        return {"method":kwords.get("method"), "data":kwords.get("data", "{}")}

url = 'https://python-brysen.c9users.io/'
WebSupport.startSession()
r = WebSupport.get(url)

#Unload data
rec = json.loads(r)
rec["pos_x"] += 50

'''
print(r, end = "\n-----------------------\n")
#req = requests.post(url, data={"method":"UPDATE","data":json.dumps(rec)})
rec["pos_y"] += 50
print(webSupport.buildData(method="UPDATE", entities=rec))
req = requests.post(url, data=webSupport.buildData(method="UPDATE", entities=rec))
print(req.text)
'''

req = WebSupport.buildRequests({}, WebSupport.buildRequest("world", world_name="tester"))
print(req, end="\n*****************\n")

res = WebSupport.s.post(url, data={"method":"REQUEST","data":json.dumps(req)}).text
t = time.time()
print(WebSupport.createAccount("username","pass").text)
print(WebSupport.login("username","pass").text)
print(WebSupport.logout("username").text)
print("In " + str(time.time() - t) + " seconds")
