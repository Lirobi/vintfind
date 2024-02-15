import subprocess
from pyVinted import Vinted
import time
import threading
import os
from utils import get_short_link
from utils import clearfile
from utils import write_html
import gc
import vinted_api
import server_flask
import requests

print("""
 █████   █████ █████ ██████   █████ ███████████ ███████████ █████ ██████   █████ ██████████      ███████████  █████ █████    █████       █████ ███████████      ███████    ███████████  █████
░░███   ░░███ ░░███ ░░██████ ░░███ ░█░░░███░░░█░░███░░░░░░█░░███ ░░██████ ░░███ ░░███░░░░███    ░░███░░░░░███░░███ ░░███    ░░███       ░░███ ░░███░░░░░███   ███░░░░░███ ░░███░░░░░███░░███ 
 ░███    ░███  ░███  ░███░███ ░███ ░   ░███  ░  ░███   █ ░  ░███  ░███░███ ░███  ░███   ░░███    ░███    ░███ ░░███ ███      ░███        ░███  ░███    ░███  ███     ░░███ ░███    ░███ ░███ 
 ░███    ░███  ░███  ░███░░███░███     ░███     ░███████    ░███  ░███░░███░███  ░███    ░███    ░██████████   ░░█████       ░███        ░███  ░██████████  ░███      ░███ ░██████████  ░███ 
 ░░███   ███   ░███  ░███ ░░██████     ░███     ░███░░░█    ░███  ░███ ░░██████  ░███    ░███    ░███░░░░░███   ░░███        ░███        ░███  ░███░░░░░███ ░███      ░███ ░███░░░░░███ ░███ 
  ░░░█████░    ░███  ░███  ░░█████     ░███     ░███  ░     ░███  ░███  ░░█████  ░███    ███     ░███    ░███    ░███        ░███      █ ░███  ░███    ░███ ░░███     ███  ░███    ░███ ░███ 
    ░░███      █████ █████  ░░█████    █████    █████       █████ █████  ░░█████ ██████████      ███████████     █████       ███████████ █████ █████   █████ ░░░███████░   ███████████  █████
     ░░░      ░░░░░ ░░░░░    ░░░░░    ░░░░░    ░░░░░       ░░░░░ ░░░░░    ░░░░░ ░░░░░░░░░░      ░░░░░░░░░░░     ░░░░░       ░░░░░░░░░░░ ░░░░░ ░░░░░   ░░░░░    ░░░░░░░    ░░░░░░░░░░░  ░░░░░
""")

#current vinted result to check if it already exists
current_item = []
#

#load searchs in search_list[] from the urls.txt file
search_list = []


def thread(thread):
	threading.Thread(thread).start()


def loadurls():
	with open("urls.txt", "r") as f:
		lines = f.readlines()
		for line in lines:
			search_list.append(line)


#

#-----------------------------------------------------------------------------------------------------------------#
#                                                                                                                 #
#                                                   VINTED PART                                                   #
#                                                                                                                 #
#-----------------------------------------------------------------------------------------------------------------#

pub = 0


def main():
	loadurls()
	global current_item
	results = []
	print("Searching for new items...")
	#getting api response for all searchs and store them in results list
	
	try:
		for search in search_list:
			#skipping spaces in the url file
			if search.startswith("https"):
				result = vinted_api.get_items(search)
				for item in result:
					if item not in current_item:
						#if item havent been seen since startup : item is added to current items list and displayed on top of te page
						current_item.append(item)
						print(item["price"], item["size"], item["image"], item["url"])
						#html code por a product div
						text = f'''
														<div id="product"><a href="{get_short_link(item["url"])}" target="_blank" id="product_link">
																<h> {item["price"]}&euro; - {item["brand"]} </h></a> <br><br>
																<img src="{item["image"]}" id="img" tabindex="0"></img><br><br><br><br></div>
										'''

						#checking if file of the brand already exists, if not, create it and format it
						if not os.path.exists(
							f'./specific/{item["brand"]}.html') or os.path.getsize(
							 f'./specific/{item["brand"]}.html') <= 5:
							clearfile(item["brand"])

						#displaying item in its brand page (on another thread because when the file is big writing takes too much time and slows down all the program)
						# global pub
						# if pub != 3: pub += 1
						# if pub == 3:
						# 	thread(
						# 	 write_html(
						# 	  '<div id="awn-z6923390" style="margin: auto; width: 50%;" data-last-modified=""></div>',
						# 	  f'{item["brand"]}.html', "ici"))
						# 	thread(
						# 	 write_html(
						# 	  '<div id="awn-z6923390" style="margin: auto; width: 50%;" data-last-modified=""></div>',
						# 	  "index.html", "ici"))

						thread(write_html(text, f'{item["brand"]}.html', "ici"))
						thread(write_html(text, "index.html", "ici"))

						requests.post("http://vintfind.fr/reload")
						print("reload called")
						#results.append(result)
						time.sleep(1)
	except:
			print("Api cooldown...")
				#bot = vinted_api.VintedBot()
				#print(bot.get(search, 10))
	time.sleep(20)
	#displaying part
	#for result in results:

time.sleep(20.0)
#calling the function again
main()


#STARTUP PART
thread(clearfile("index.html"))
for file in os.listdir("./specific/"):
	clearfile(file)
	thread(
	 write_html(
	  f'<a href="../specific/{file}" id="brandlink">{file.replace(".html", "")}</a>',
	  "index.html", "la"))
	thread(
	 write_html(
	  f'<brand id="brandlink" style="font-size:200%; position: relative;">{file.replace(".html", "")}</brand>',
	  file, "la"))

#web server

#stop logs from server

# def start_server():
# 	subprocess.call("python server.py", shell=True)

#web server thread
#threading.Thread(target=start_server).start()
#main function thread
requests.post(f"http://botvinted.lirobi.repl.co/reload")
print("reload called")
main()
