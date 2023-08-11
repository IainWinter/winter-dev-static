from flask import Flask, request, jsonify
from logic import *
from data import db_close

app = Flask(__name__)

def send_json(obj):
	response = jsonify(obj)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route("/comment-get/<subject>")
def comment_get(subject):
    ip = request.remote_addr
    return send_json(get_comments_for_subject(ip, subject))

@app.route("/comment-post/<subject>/<test>/<parent>/<name>/<content>")
def comment_post(subject, test, parent, name, content):
	ip = request.remote_addr
	return send_json(try_post_comment(ip, subject, test, parent, name, content))

@app.route("/comment-edit/<edit_key>/<name>/<content>")
def comment_edit(edit_key, name, content):
	ip = request.remote_addr
	return send_json(try_edit_comment(ip, edit_key, name, content))

@app.route("/comment-delete/<edit_key>")
def comment_delete(edit_key):
	ip = request.remote_addr
	return send_json(try_delete_comment(ip, edit_key))

@app.teardown_appcontext
def close_connection(exception):
	db_close()

if __name__ == '__main__':
	with app.app_context():
		init_tables()
		create_subject("epa-algorithm", "What is the answer to life, the universe and everything?", "42")

	print("Starting server...")
	app.run(debug=True, use_reloader=False)