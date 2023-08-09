from data import *
import secrets
import html

def name_or_content_is_invalid(name, content):
	# name has to be between 2 and 36 characters long
	# name can only include alphabetical, numerical and the following symbols: ' - _
	# name can't start or end with a space
	# name can't have 2 spaces in a row

	if len(name) < 2 or len(name) > 36 or name[0] == " " or name[-1] == " " or "  " in name:
		return True
	
	allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'-._ "

	for c in name:
		if c not in allowed_chars:
			return True

	# content is between 16 and 1024 characters long
	# content can't begin or end with a newline
	# content can't have 3 newlines in a row

	if len(content) < 16 or len(content) > 1024 or content[0] == "\n" or content[-1] == "\n" or "\n\n\n" in content:
		return True
	
	return False

def try_post_comment(connection_ip: str, subject_name: str, test_answer: str, parent_id_str: str, name: str, content: str):
	parent_id = 0

	try:
		parent_id = int(parent_id_str)
	except ValueError:
		return { "status": "error" }
	
	if name_or_content_is_invalid(name, content):
		return { "status": "invalid name or content" }
	
	(reject, penalty) = ip_is_rejected(connection_ip)
	if reject:
		return { "status": "limited", "penalty": penalty }
	
	subject_id = subject_get_id_from_name(subject_name)
	if subject_id == 0:
		return { "status": "error" }

	if subject_or_answer_is_invalid(subject_id, test_answer):
		return { "status": "test failed" }

	sanatized_name = html.escape(name)
	sanatized_content = html.escape(content)
	
	edit_key = secrets.token_urlsafe(16)
	id = comment_insert(parent_id, subject_id, edit_key, connection_ip, sanatized_name, sanatized_content)

	return { "status": "success", "comment_id": id, "edit_key": edit_key }

def try_edit_comment(connection_ip: str, edit_key: str, new_name: str, new_content: str):
	if name_or_content_is_invalid(new_name, new_content):
		return { "status": "invalid name or content" }
	
	(reject, penalty) = ip_is_rejected(connection_ip)
	if reject:
		return { "status": "limited", "penalty": penalty }

	if comment_or_timelimit_invalid(edit_key):
		return { "status": "error" }
	
	sanatized_name = html.escape(new_name)
	sanatized_content = html.escape(new_content)

	comment_update(edit_key, sanatized_name, sanatized_content)

	return { "status": "success" }

def try_delete_comment(connection_ip: str, edit_key: str):
	(reject, penalty) = ip_is_rejected(connection_ip)
	if reject:
		return { "status": "limited", "penalty": penalty }

	if comment_or_timelimit_invalid(edit_key):
		return { "status": "error" }

	comment_delete(edit_key)

	return { "status": "success" }

def get_comments_for_subject(connection_ip: str, subject_name: str):
	subject_id = subject_get_id_from_name(subject_name)
	if subject_id == 0:
		return { "status": "error" }

	comments = comment_get_all_not_deletd_for_subject(subject_id)
	subject = subject_get_info(subject_id)

	return { "status": "success", "comments": comments, "subject": subject }