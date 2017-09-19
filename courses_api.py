import json
import pprint
import unirest


# These code snippets use an open-source library. http://unirest.io/python
response = unirest.get("https://datagram-products-v1.p.mashape.com/stores/23070/products/",
  headers={
    "X-Mashape-Key": "TgiAp7CM9RmshFXYe8xESFB54xjGp1TqWU4jsniysYbeLUttz3",
    "Accept": "application/json"
  }
)

for item in response.body:
	print item['label']

