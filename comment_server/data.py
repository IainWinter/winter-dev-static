from database import *

##
## Database layer
##

SECONDS_PENALTY_PER_CONNECTION = 2
MAX_CONNECTIONS_BEFORE_LIMIT = 3

def init_tables():
	query_direct('''
		CREATE TABLE IF NOT EXISTS comments (
			id             INTEGER     PRIMARY KEY AUTOINCREMENT,
       
			parent_id      INTEGER     NOT NULL,
			subject_id     INTEGER     NOT NULL,
       
			edit_key       VARCHAR(16) NOT NULL,
       
			creation_time  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
			creation_ip    VARCHAR(64) NOT NULL,
		
       		is_deleted     BOOLEAN     NOT NULL DEFAULT FALSE,
       
			name           VARCHAR(64) NOT NULL,
			content        TEXT        NOT NULL
       );
	''')
	
	query_direct('''
		CREATE TABLE IF NOT EXISTS subjects (
			id            INTEGER     PRIMARY KEY AUTOINCREMENT,
			name          VARCHAR(64) NOT NULL,
			test_question VARCHAR(64) NOT NULL,
			test_answer   VARCHAR(64) NOT NULL
       );
	''')
	
	query_direct('''
		CREATE TABLE IF NOT EXISTS ip_limiters (
			id           INTEGER     PRIMARY KEY AUTOINCREMENT,
			ip           VARCHAR(64) NOT NULL UNIQUE,
			is_banned    BOOLEAN     NOT NULL DEFAULT FALSE,
	      	recent_count INTEGER     NOT NULL DEFAULT 0,
	      	last_time    DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP
       );
    ''')

	db_commit()

def create_subject(subject_name: str, test_question: str, test_answer: str):
	query("INSERT INTO subjects (name, test_question, test_answer) VALUES (?, ?, ?)", (subject_name, test_question, test_answer))
	db_commit()

def subject_or_answer_is_invalid(subject_id: int, test_answer: str):
	count = query_get_count("SELECT COUNT(*) FROM subjects WHERE id = ? AND test_answer = ?", (subject_id, test_answer))
	return count == 0

def comment_or_timelimit_invalid(edit_key: str):
	count = query_get_count("SELECT COUNT(*) FROM comments WHERE edit_key = ? AND creation_time > datetime('now', '-15 minutes')", (edit_key, ))
	return count == 0

def comment_insert(parent_id: int, subject_id: int, edit_key: str, creation_ip: str, name: str, content: str):
	id = query_get("INSERT INTO comments (parent_id, subject_id, edit_key, creation_ip, name, content) VALUES (?, ?, ?, ?, ?, ?) RETURNING id", (parent_id, subject_id, edit_key, creation_ip, name, content))
	db_commit()
	return id["id"]

def comment_update(edit_key: str, new_name: str, new_content: str):
	query("UPDATE comments SET name = ?, content = ? WHERE edit_key = ?", (new_name, new_content, edit_key))
	db_commit()

def comment_delete(edit_key: str):
	query("UPDATE comments SET is_deleted = TRUE WHERE edit_key = ?", (edit_key, ))
	db_commit()

def comment_get_all_not_deletd_for_subject(subject_id: int):
	return query("SELECT id, parent_id, creation_time, name, content, strftime('%s', creation_time) - strftime('%s', datetime('now', '-15 minutes')) AS edit_time_left FROM comments WHERE subject_id = ? AND is_deleted = FALSE", (subject_id, ))

def subject_get_info(subject_id: int):
	return query_get("SELECT name, test_question FROM subjects WHERE id = ?", (subject_id, ))

def ip_reduce_recent_count(ip: str):
	# Insert ip if it doesn't exist
	query("INSERT OR IGNORE INTO ip_limiters (ip) VALUES (?)", (ip, ))
	db_commit()

	# Add 1 for each query and subtract 1 for every 30 second interval since query, limit the count to 0
	query("UPDATE ip_limiters SET recent_count = 1 + MAX(0, recent_count - (strftime('%s', 'now') - strftime('%s', last_time)) / ?), last_time = CURRENT_TIMESTAMP WHERE ip = ?", (SECONDS_PENALTY_PER_CONNECTION, ip))
	db_commit()

def ip_is_rejected(ip: str):
	# Just run this here, assumes this is done once per connection
	ip_reduce_recent_count(ip)

	#get the recent count for the ip, if the ip is banned return a larger recent count to flub the check
	recent_count = query_get("SELECT recent_count + is_banned * 10000 AS recent_count FROM ip_limiters WHERE ip = ?", (ip, ))["recent_count"]
	
	reject = recent_count >= MAX_CONNECTIONS_BEFORE_LIMIT
	penalty = (recent_count - MAX_CONNECTIONS_BEFORE_LIMIT + 1) * SECONDS_PENALTY_PER_CONNECTION

	if (reject):
		print("%s recent count is %d, wait %s" % (ip, recent_count, penalty))

	return (reject, penalty)

def subject_get_id_from_name(subject_name: str):
	id = query_get("SELECT id FROM subjects WHERE name = ?", (subject_name, ))
	return 0 if id == None else id["id"]