from urllib import parse

class URLParams():
	def __init__(self, path):
		parts = parse.urlparse(path)
		self.args = parse.parse_qs(parts.query)
		self.path = parts.path

	def get_string(self, name):
		return self.args[name][0]

	def get_int(self, name):
		return int(self.get(name))

	def has(self, name):
		return name in self.args

	def has_all(self, names):
		for name in names:
			if not self.has(name) or len(self.args[name]) == 0:
				return False
		return True