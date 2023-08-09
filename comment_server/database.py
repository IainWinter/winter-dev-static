import sqlite3

##
## Database connection and helpers
##

g_con = None

def init_database_connection(db_file_path):
    global g_con
    g_con = sqlite3.connect(db_file_path)

def dnit_database_connection():
    global g_con
    if g_con == None:
        g_con.close()
        g_con = None

## unsafe
def query_direct(query_string):
	global g_con
	cur = g_con.cursor()
	cur.execute(query_string)

def query(query_template: str, query_arguments: tuple):
	global g_con
	cur = g_con.cursor()
	result = []
	for row in cur.execute(query_template, query_arguments):
		result_row = {}
		for i in range(len(row)):
			result_row[cur.description[i][0]] = row[i]
		result.append(result_row)

	return result

def query_get(query_template: str, query_arguments: tuple):
	return query(query_template, query_arguments)[0]

def query_get_count(query_template: str, query_arguments: tuple):
	return query_get(query_template, query_arguments)["COUNT(*)"]