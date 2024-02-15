import errno
import logging
import urllib
from flask import Flask, request, send_file, redirect, make_response
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # import the CORS module

app = Flask(__name__)
PORT = 9091  # Change this to the desired port number
DIRECTORY = "./"  # Change this to the directory containing index.html
URL_FILE = "urls.txt"

# Initialize CORS
CORS(app)
socketio = SocketIO(app,
                    cors_allowed_origins="https://vintfind.fr",
                    async_mode='threading')

socketio.init_app(app, cors_allowed_origins="*")

logging.basicConfig(level=logging.INFO)


@app.route("/")
def index():
	return redirect("/index.html")


@app.route("/<path:path>")
def serve_file(path):
	try:
		return send_file(path)
	except FileNotFoundError:
		return redirect("/index.html")


@app.route("/add_url", methods=["POST"])
def add_url():
	url = request.form["url"]
	with open(URL_FILE, "a") as f:
		f.write("\n" + url + "\n")
	return redirect("/")


@socketio.on('reload')
@app.route("/reload", methods=["POST"])
def reload():
	response = make_response("Forcing all clients to reload")
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "0"
	response.headers["Refresh"] = "0; url=/"
	socketio.emit('reload_page', namespace='/')
	return response


if __name__ == "__main__":
	port = PORT
	while True:
		try:
			app.run(port=port, host="0.0.0.0")
		except OSError as e:
			if e.errno == errno.EADDRINUSE:
				print(f"Port {port} is already in use. Trying the next port...")
				port += 1
				continue
			else:
				raise
