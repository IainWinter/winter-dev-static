import sqlite3
from flask import g

##
## Database connection and helpers
##

g_database_path = "data.db"

# this was using a global connection which doesn't work
# because flask uses multiple threads
# g_con = None
# def init_database_connection(db_file_path):
#     global g_con
#     g_con = sqlite3.connect(db_file_path)

# def dnit_database_connection():
#     global g_con
#     if g_con == None:
#         g_con.close()
#         g_con = None

## unsafe

def db_connect():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(g_database_path)

	db.row_factory = sqlite3.Row
	
	return db

def db_close():
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def db_commit():
	db = getattr(g, '_database', None)
	if db is not None:
		db.commit()

def query_direct(query_string):
	cur = db_connect().execute(query_string)
	result = cur.fetchall()
	cur.close()
	return result

	# con = sqlite3.connect(g_database_path)
	# cur = con.cursor()
	# cur.execute(query_string)
	# con.close()

def query(query_template: str, query_arguments: tuple):
	cur = db_connect().execute(query_template, query_arguments)
	result_rows = cur.fetchall()
	cur.close()

	# conver the results into a list of dicts

	result = []
	for row in result_rows:
		result_row = {}
		for i in range(len(row)):
			result_row[cur.description[i][0]] = row[i]
		result.append(result_row)

	return result

	# con = sqlite3.connect(g_database_path)
	# con.row_factory = sqlite3.Row
	# cur = con.execute(query_template, query_arguments)

	# result = []
	# for row in :
	# 	result_row = {}
	# 	for i in range(len(row)):
	# 		result_row[con.description[i][0]] = row[i]
	# 	result.append(result_row)

	# con.close()

	# return result

def query_get(query_template: str, query_arguments: tuple):
	results = query(query_template, query_arguments)
	if len(results) == 0:
		return None

	return results[0]

def query_get_count(query_template: str, query_arguments: tuple):
	results = query_get(query_template, query_arguments)
	if results == None:
		return 0

	return results["COUNT(*)"]