import json
import requests
import sys


id = sys.argv[1]

url = "https://lichess.org/api/stream/game/" + id
headers = {"Accept": "application/x-ldjson"}
response = requests.get(url, headers=headers, stream=True)
list_resp = response.text.splitlines()
json_resp = list(map(lambda x: json.loads(x), list_resp))
i = 2
lmlist = []
for i in range(len(json_resp)):
    if (not json_resp[i].get('lm') is None):
        lmlist.append(json_resp[i].get('lm'))
print(lmlist)

