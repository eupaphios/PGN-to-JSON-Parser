import requests
from bs4 import BeautifulSoup
import chess.pgn
import re
import io
import sys

id = sys.argv[1]

url = "https://lichess.org/api/stream/game/" + id
r = requests.get(url)
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
print (data["moves"])