import http.server
import json

from url import URLParams
from logic import *

HOST = "localhost"
PORT = 8801

api = {
	"/comment-post":   [ try_post_comment,         ["subject", "test", "parent", "name", "content"] ],
	"/comment-edit":   [ try_edit_comment,         ["edit_key", "name", "content"] ],
	"/comment-delete": [ try_delete_comment,       ["edit_key"] ],
	"/comment-get":    [ get_comments_for_subject, ["subject"] ]
}

class DevWinterCommentsServer(http.server.SimpleHTTPRequestHandler):
	def return_json(self, jsonObject):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Origin', '*')   # only temp
		self.end_headers()
		self.wfile.write(bytes(json.dumps(jsonObject), 'utf-8'))
        
	def do_GET(self):
		url = URLParams(self.path)
		connection_ip = self.client_address[0]

		json_response = { "status": "error" }

		# Create a new string with the url path, without the trailing slash
		# This is done to make sure that the url path is in the api dictionary
		# even if the user enters the url with a trailing slash

		api_path = url.path
		if api_path.endswith("/"):
			api_path = api_path[:-1]

		if api_path in api:
			action, action_params = api[api_path]
			if url.has_all(action_params):
				try:
					json_response = action(connection_ip, *[url.get_string(param) for param in action_params])
				except Exception:
					pass # default response is error

		return self.return_json(json_response)

webServer = http.server.HTTPServer((HOST, PORT), DevWinterCommentsServer)

try:
	print("Starting server...")

	print("Creating database...")
	init_database_connection("data.db")
	init_tables()

	# should disable
	print("Creating test subject...")
	create_subject("epa-algorithm", "What is the answer to life, the universe and everything?", "42")

	print("Server started http://%s:%s" % (HOST, PORT))
	webServer.serve_forever()

except KeyboardInterrupt:
	webServer.server_close()
	print("The server is stopped.")