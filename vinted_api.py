from __future__ import annotations

import json
from pprint import pprint
from typing import Any
from typing import Iterator

import requests
from bs4 import BeautifulSoup
import time

HEADERS = { ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'), ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'), ('Accept-Encoding','gzip, deflate, br'),\
    ('Accept-Language','en-US,en;q=0.5' ), ("Connection", "keep-alive"), ("Upgrade-Insecure-Requests",'1')
}


def get_items(url: str) -> Iterator[dict[str, Any]]:
	try:
		response = requests.get(url, headers=HEADERS)
		soup = BeautifulSoup(response.text, 'html.parser')
		script = soup.select('script[type="application/json"]')[-1]
		json_payload = json.loads(script.text)
		items = json_payload['items']['catalogItems']['byId']

		scraped_item = {}
		counter = 0
		for _, item in items.items():
			if counter >= 20:
				break
			scraped_item = {}
			scraped_item['id'] = item['id']
			scraped_item['title'] = item['title']
			scraped_item['price'] = float(item['price'])
			scraped_item['total_price'] = float(item['total_item_price'])
			scraped_item['brand'] = item['brand_title']
			scraped_item['url'] = item['url']
			scraped_item['size'] = item['size_title']
			scraped_item['image'] = item['photo']['url']

			yield scraped_item
			counter += 1
	except:
		print(requests.get(url, headers=HEADERS))
		print("error")
		time.sleep(10)


# def main() -> int:
#     url = 'https://www.vinted.fr/catalog?search_text=&brand_id[]=53&size_id[]=207&size_id[]=208&status_ids[]=6&status_ids[]=1&status_ids[]=2&catalog[]=267&price_to=15.0&currency=EUR&search_id=9153240985&order=newest_first'
#     for item in get_items(url):
#         pprint(item)
#     return 0

# if __name__ == "__main__":
#     raise SystemExit(main())
