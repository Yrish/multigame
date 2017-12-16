import requests
import json
import time
import os
import shutil

class WebSupport:
    """
    WebSupport - STATIC CLASS
    Anything wich deals with the servers

    Inculded Class Variables:
    url - The url the server is at
    username - The username the client's player is loged in with, assigned when login is sucessfull.
    authToken - The token that allows client access to server, assigned when login is sucessfull.
    s - the Session object which becomes live when startSession() is called

    Included Methods:
    startSession() - called at the begining of application lauch, starts connection with the server
    get() - returns json of entire active world
    update() - sends an update to the server
    buildData() - helper method for update() and buildRequests()
    buildRequests() - helper method to build a request to the server
    buildRequest() - helper method to buildRequests(), helps format a singular request
    buildFile() - called when a file needs to be downloaded from server
    authenticate() - called when need to authenticate a user arrises -returns boolean
    login() - Allows a user to login to the server
    logout() - Allows a user to logout of the server
    createAccount() - Creates an account on the server
    
    
    """

    url = 'https://python-brysen.c9users.io/'
    username = None
    authToken = None
    s = None
    r = None

    def startSession():
        """
    Initializes the Session with the server at the server

    Args: None

    Returns:
        True - if connection is established
        False - if connection fails to establish

    Accomplishes:
        -Establishes connection with the server and initalizes the class variable "s" with the Session object
    """
        try:
            WebSupport.s = requests.Session()
            return True
        except Exception:
            return False

    def get(**kwords):
        return WebSupport.s.get(kwords.get("url", WebSupport.url)).text

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

    def downloadFiles(iterableFileNames, downloadpath):
        for filename in iterableFileNames:
            print("Grabbing file: " + filename)
            if filename.startswith("BOX"):
                print("isBox")
                WebSupport._downloadFile(filename, os.sep.join((downloadpath, filename[3:])))

    def _downloadFile(filename, destination):
        packet = WebSupport.__basicPacket__(method="DOWNLOAD", data=json.dumps({"filename":filename}))
        r = WebSupport.s.post(WebSupport.url, data=packet, stream=True)
        r.raw.decode_centent = True
        with open(destination, "wb") as file:
            shutil.copyfileobj(r.raw, file)

    def authenticate(username, password):
        """
    Authenticates the user with a username and password

    Args:
        username - the accounts username
        password - the accounts password

    Returns:
        True - if username is matched with password on the connected server
        False - if the username does not match the password on the connected server
    """
        req = {"method":"AUTHENTICATE","data":json.dumps({"username":username,"password":password})}
        return WebSupport.s.post(WebSupport.url, data=req)

    def login(username, password):
        """
    Logs the user into the connected server and assigns authToken

    Args:
        username - the account's username
        password - the account's password

    Returns:
        Request object which cantains server response

    Accomplishes:
        Assingns username and authToken to WebSupport static variables if sucessfully loged in.
        """
        req = {"method":"LOGIN","data":json.dumps({"username":username,"password":password})}
        ret = WebSupport.s.post(WebSupport.url, data=req)
        rett = json.loads(ret.text)
        if rett["login_status"] == True:
            WebSupport.username = username
            WebSupport.authToken = rett["authToken"]
        return ret

    def logout(username):
        """
    Logs the user out of the connected server

    Args:
        username - the accounts username

    Returns:
        Request object with response

    Accomplishes
        Logs the user out of the server and the server drops the authToken
        """
        req = WebSupport.__basicLogedInPacket__(method="LOGOUT", data = json.dumps({"username":username}))
        #req = {"method":"LOGOUT","data":json.dumps({"username":username})}
        return WebSupport.s.post(WebSupport.url, data=req)

    def createAccount(username, password):
        """
    Creates a user account on connected server

    Args:
        username - the account's username
        password - the account's password

    Returns:
        Request object with response

    Accomplishes
        Creates an account with username and password on connected server
    """
        req = WebSupport.__basicPacket__(method="CREATEACCOUNT", data = json.dumps({"username":username,"password":password}))
        return WebSupport.s.post(WebSupport.url, data=req)

    def __basicLogedInPacket__(**kwords):
        lil = WebSupport.__basicPacket__(**kwords)
        lil["username"] = kwords.get("username", WebSupport.username)
        lil["authToken"] = kwords.get("authToken", WebSupport.authToken)
        return lil

    def __basicPacket__(**kwords):
        return {"method":kwords.get("method"), "data":kwords.get("data", "{}")}


'''
url = 'https://python-brysen.c9users.io/'
WebSupport.startSession()
r = WebSupport.get(url=url)
print(r)

#Unload data
rec = json.loads(r)
rec["pos_x"] += 50


print(r, end = "\n-----------------------\n")
#req = requests.post(url, data={"method":"UPDATE","data":json.dumps(rec)})
rec["pos_y"] += 50
print(webSupport.buildData(method="UPDATE", entities=rec))
req = requests.post(url, data=webSupport.buildData(method="UPDATE", entities=rec))
print(req.text)


req = WebSupport.buildRequests({}, WebSupport.buildRequest("world", world_name="tester"))
print(req, end="\n*****************\n")

res = WebSupport.s.post(url, data={"method":"REQUEST","data":json.dumps(req)}).text
t = time.time()
print(WebSupport.createAccount("username","pass").text)
print(WebSupport.login("username","pass").text)
print(WebSupport.logout("username").text)
print("In " + str(time.time() - t) + " seconds")
'''
