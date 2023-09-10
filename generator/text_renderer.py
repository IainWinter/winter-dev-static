import io
from file import ref

# This takes in a string and a dict of functions by name

# first find all functions and collect their names and locations

# this class is an iterator through a string which can peek n characters ahead
class TextIterator:
	def __init__(self, text: str):
		self.text = text
		self.len = len(text)
		self.index = 0
		self.current = '\0' if self.len == 0 else text[0]

	# return either the n characters forward or \0
	def peek(self, n: int = 1) -> str:
		peek_index = self.index + n

		if peek_index >= self.len or peek_index < 0:
			return '\n' # treat as if document is surrounded by newlines
		
		return self.text[peek_index]

	def next(self, n: int = 1) -> None:
		self.current = self.peek(n)
		self.index += n

	def more(self) -> bool:
		return self.index < self.len

def find_functions(text: str, functions: dict) -> list:
	# find the location of all functions that are in the functions dict
	# each list element is (func_name, index, args_list)
	func_locations = []

	itr = TextIterator(text)
	last_bracket = 0

	while itr.more():
		if itr.current == '[':
			last_bracket = itr.index

		elif itr.current == ']' and itr.peek() == '(':
			function_name = text[last_bracket + 1:itr.index]

			# skip ](
			itr.next(2)

			if function_name in functions:
				# find the argument string
				arg_str = ""
				
				pcount = 1

				while itr.more():
					if itr.current == '(':
						pcount += 1
					elif itr.current == ')':
						pcount -= 1

					# check count here so the last ) is not written
					if pcount == 0:
						break

					arg_str += itr.current
					itr.next()

				func_locations.append((function_name, arg_str, last_bracket, itr.index + 1))

		itr.next()

	return func_locations

# return a copy of the text with each instance of ~/ replace with the
# current root dir
def convert_local_links(text: str) -> str:
	out = io.StringIO()
	itr = TextIterator(text)

	while itr.more():
		if itr.current == '~' and itr.peek() == '/':
			out.write(ref("~/"))
			itr.next(2)

		out.write(itr.current)
		itr.next()

	return out.getvalue()

# writes the text outside of functions directly
def render_template(text: str, functions: dict) -> str:
	out = io.StringIO()

	func_locations = find_functions(text, functions)
	last_index = 0

	for (name, args, index, end_index) in func_locations:
		out.write(convert_local_links(text[last_index:index]))

		if len(args) == 0:
			functions[name](out)
		else:
			functions[name](out, args)

		last_index = end_index

	out.write(convert_local_links(text[last_index:]))

	return out.getvalue()

# writes the text outside of functions as blocks like markdown
def render_article(text: str, functions: dict) -> str:
	out = io.StringIO()

	func_locations = find_functions(text, functions)
	last_index = 0

	last_block_was_newline = False
	in_paragraph = False

	# only reason this is a local function and not inline is that the last block needs to be added
	# after the loop as well
	def add_block(text):
		nonlocal last_block_was_newline
		nonlocal in_paragraph

		is_newline = block == ''
		
		# Skip consecutive newlines
		if is_newline and last_block_was_newline:
			return
		
		last_block_was_newline = is_newline

		if not is_newline and not in_paragraph:
			out.write('<p>')
			in_paragraph = True

		if is_newline and in_paragraph:
			out.write('</p>')
			in_paragraph = False
			return
		
		out.write(block)

	for (name, args, index, end_index) in func_locations:
		for block in text[last_index:index].split('\n'):
			add_block(block)

		if len(args) == 0:
			functions[name](out)
		else:
			functions[name](out, convert_local_links(args))

		last_index = end_index

	for block in text[last_index:].split('\n'):
		add_block(block)

	return out.getvalue()