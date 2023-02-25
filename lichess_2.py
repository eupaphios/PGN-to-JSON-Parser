import requests
from bs4 import BeautifulSoup
import chess.pgn
import re
import io
import pymongo
import logging

log = logging.getLogger().error

myclient = pymongo.MongoClient("mongodb://root:rootpassword@localhost:27017/")
mydb = myclient["chess"]
mycol = mydb["developers"]

r = requests.get('https://lichess.org/yi2rNhT0')
soup = BeautifulSoup(r.content, 'html.parser')

all_tables=soup.find_all('div', {'class':'pgn'} )
output = str(all_tables[0].text).splitlines(0)[-1]
print (output)
pgn = io.StringIO(output)
node = chess.pgn.read_game(pgn)
data = node.headers
data["moves"] = []
while node.variations:
    next_node = node.variation(0)
    data["moves"].append(
        re.sub("\{.*?\}", "", node.board().san(next_node.move)))
    node = next_node
print(data["moves"])


for i in range(len(data["moves"])):
    print(data["moves"][i])
    mycol.find({}, { "moves": 1 });
    mycol.a

    match = mycol.products.find({["moves",i]: data["moves"][i]})
    print (match)
#
for match in mycol.find({ "moves" : { "$in" : data["moves"] } }):
