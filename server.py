import http.server
import socketserver
import errno
import urllib
import logging
from utils import Style
import gc

PORT = 9091  # Change this to the desired port number
DIRECTORY = "/"  # Change this to the directory containing index.html
URL_FILE = "urls.txt"

Handler = http.server.SimpleHTTPRequestHandler

logging.basicConfig(level=logging.INFO)


class CustomHandler(Handler):

	def translate_path(self, path):
		path = super().translate_path(path)
		try:
			AUTH_CODE = "Lclpgydtlt6*"
			if 'urls.html' in path:
				# Check if the code parameter is present and matches the expected code
				query_params = urllib.parse.urlparse(self.path).query
				code = urllib.parse.parse_qs(query_params).get('code', [''])[0]
				if code != AUTH_CODE:
					# Return a 403 error if the code is incorrect
					self.send_error(403, "Access denied")
					return None

			if path == '/':
				self.send_response(301)
				self.send_header('Location', '/index.html')
				self.end_headers()
				return None
			# Get the absolute path of the requested file

			# Check if the requested file is an HTML file
			if not path.endswith('.html') and not path.endswith(
			  '.css') and not path.endswith('.js'):
				# Return a 404 error if the file is not an HTML file

				self.send_response(301)
				self.send_header('Location', '/index.html')
				self.end_headers()
				return None

			# Return the path if the file is an HTML file
			return path
		except:
			print("error")

	def end_headers(self):
		self.send_header("Cache-Control", "no-cache")
		super().end_headers()

	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Cache-Control', 'no-store')
		self.send_header('Pragma', 'no-cache')
		self.send_header('Expires', '-1')
		self.end_headers()

	def do_POST(self):
		# Get the URL parameter from the POST request
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		params = urllib.parse.parse_qs(post_data.decode())
		url = params['url'][0]

		# Append the URL to the file
		with open(URL_FILE, "a") as f:
			f.write("\n" + url + "\n")

		# Redirect to the homepage
		self.send_response(303)
		self.send_header('Location', '/')
		self.end_headers()

	# def log_message(self, format, *args):
	# 	# disable logging for incoming requests
	# 	pass


def run_server(port):
	with socketserver.TCPServer(("", port), CustomHandler) as httpd:

		print(f"\n{Style.RED} SERVER PORT :{port}\n {Style.WHITE}")
		httpd.serve_forever()


def server():
	port = PORT
	while True:
		try:
			run_server(port)
		except OSError as e:
			if e.errno == errno.EADDRINUSE:
				print(f"Port {port} is already in use. Trying the next port...")
				port += 1
				continue
			else:
				raise


server()
