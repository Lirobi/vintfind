import threading
import subprocess


def start_server():
	subprocess.call("python3 server_flask.py", shell=True)


def start_bot():
	subprocess.call("python3 vinted.py", shell=True)


server = threading.Thread(target=start_server)
bot = threading.Thread(target=start_bot)

server.start()
bot.start()
