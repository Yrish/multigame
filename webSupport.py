import requests
import json

class webSupport:

    def startSession():
        webSupport.s = requests.Session()

    def get(url):
        return webSupport.s.get(url).text

    def update(url, json):
        webSupport.s.get(url, params={'update':json})

    def __import__():
        webSupport.startSession()

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

url = 'https://python-brysen.c9users.io/'
webSupport.startSession()
r = webSupport.get(url)

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

req = webSupport.buildRequests({}, webSupport.buildRequest("world", world_name="tester"))
print(req, end="\n*****************")

res = requests.post(url, data={"method":"REQUEST","data":json.dumps(req)}).text
