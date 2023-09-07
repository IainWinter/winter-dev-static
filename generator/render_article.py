import io
from render_code import render_code

# This renders an article from a markdown-like file

# the file must start with ---
# after --- 0 or more lines with 1 key value pair per line is read into a string->string dictionary
# 	key is first span of letters before the : and value is the rest of the line
# after 0 or more lines --- must end the metadata section

# after the metadata section, the text is parsed as follows:

# two newlines followed by any character starts a paragraph
# [<type>](arg1, arg2) is an object which calls a function in map a named <type> and passed the arguments in the parens as a single string

# examples

# [title](Title)
# [subtitle](Subtitle)
# [equation](x^2 + y^2 = z^2)
# [iframe](https://example.com)
# [link](name of link, https://example.com)
# [code](TypeErasureCopy.h, cpp,
# 	using `t`func_DeepCopy = std::function<void(void*, void*)>;
# )

STATE_START = 0
STATE_META = 1
STATE_TEXT = 2

def render_article(text, functions, exit_on_meta = False):
    # the renderer output is a list of strings and the metadata
	strings = []
	meta = {}

	i = -1
	c = '\0'
	current_block = io.StringIO()
	current_block_is_paragraph = False
	line_count = 0

	def nextChar():
		nonlocal i
		nonlocal c
		nonlocal line_count

		i += 1
		c = text[i]

		if c == '\n':
			line_count += 1

	def advance(count):
		nonlocal i
		i += count

	def isWhitespace():
		nonlocal c
		return c.isspace()
	
	def writeBlock():
		nonlocal current_block
		nonlocal current_block_is_paragraph
		nonlocal strings

		if current_block_is_paragraph:
			current_block.write("</p>") 

		previous_block = current_block.getvalue()

		if len(previous_block) > 0:
			strings.append(previous_block)

		current_block = io.StringIO()
		current_block_is_paragraph = False

	state = STATE_START
	was_just_object = False

	# emulate a for loop (continue still increments)
	total_length = len(text)
	while True:
		if i + 1 >= total_length:
			break

		nextChar()

		# look for metadata delim
		if state == STATE_START:

			if isWhitespace():
				continue

			if c == '-':
				c1 = text[i + 1]
				c2 = text[i + 2]

				if c1 == '-' and c2 == '-':
					state = STATE_META
					advance(2)
					continue
				else:
					raise Exception("Expected --- at start of file")
		
		elif state == STATE_META:
			# skip all whitespace until first letter
			if isWhitespace():
				continue

			# extract key and value pair for this line
			if c.isalpha():
				key_value_line = io.StringIO()

				while c != '\n':
					key_value_line.write(c)
					nextChar()

				key_value_pair = key_value_line.getvalue().split(':', 1)

				if len(key_value_pair) != 2:
					raise Exception("Expected key-value pair")

				name = key_value_pair[0].strip()
				value = key_value_pair[1].strip()

				meta[name] = value

				continue

			# if not in a line, test for end of meta section
			elif c == '-':
				c1 = text[i + 1]
				c2 = text[i + 2]

				if c1 == '-' and c2 == '-':
					# This should be in its own functions
					# but this works for now
					if exit_on_meta:
						return (meta, i + 3)

					state = STATE_TEXT
					advance(2)
					continue
				else:
					raise Exception("Expected --- at end of meta section")

			else:
				raise Exception("Expected key name or ---")

		elif state == STATE_TEXT:
			if i + 1 >= total_length: # finish in text
				break

			c1 = text[i + 1]

			if c == '\n' and (c1 == '\n' or was_just_object):
				was_just_object = False
				writeBlock()

				if c1 == '\n':
					advance(1)

				continue

			# At the beginning of an object, may be inside of a paragraph or may be free
			if c == '[':
				nextChar()

				# parse out the type are arguments
				type = io.StringIO()
				while c != ']':
					type.write(c)
					nextChar()

				# skip to the first argument
				while c != '(':
					nextChar()
				
				nextChar()

				# print(f"Found object {type.getvalue()} at line {line_count}")

				# Let the user parse the arguments themselves
				# alls we need to parse out now is everything between two paranthesis, but the content can contain paranthesis
				# apply the constraint that there needs to be an even number of paranthesis in the arguments, this should be fine for everything I can think of

				arguments = io.StringIO()

				paren_count = 1
				while True:
					if c == '(':
						paren_count += 1
					elif c == ')':
						paren_count -= 1
					
					if paren_count == 0:	
						break

					arguments.write(c)
					nextChar()

				argument_string = arguments.getvalue()
				has_arguments = len(argument_string) > 0
				func = functions[type.getvalue()]

				if has_arguments:
					func(current_block, argument_string)
				else:
					func(current_block)

				was_just_object = True

			else:
				if not current_block_is_paragraph:
					current_block.write("<p>")

				current_block_is_paragraph = True
				current_block.write(c)
				was_just_object = False

	# write final block
	writeBlock()

	return (strings, meta)