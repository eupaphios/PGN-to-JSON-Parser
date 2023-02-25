import json
import requests
import sys
import pymongo

# myclient = pymongo.MongoClient("mongodb://root:rootpassword@localhost:27017/")
# mydb = myclient["chess"]
# mycol = mydb["developers"]

# id = sys.argv[1]


url = "https://lichess.org/api/stream/game/yi2rNhT0"
headers = {"Accept": "application/x-ldjson"}
response = requests.get(url, headers=headers, stream=True)
list_resp = response.text.splitlines()
print(list_resp)
json_resp = list(map(lambda x: json.loads(x), list_resp))
lmlist = []
for i in range(len(json_resp)):
    if (not json_resp[i].get('lm') is None):
        lmlist.append(json_resp[i].get('lm'))
        print(lmlist)


# for match in mycol.find({ "ad_accounts.0.ads.campaigns" : { "$in" : lmlist } }):
#     print(match)
