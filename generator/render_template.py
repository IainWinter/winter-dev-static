import io
from file import ref

def render_template(text, functions):
	output = io.StringIO()
	acc = io.StringIO()

	i = -1
	c = '\0'

	def nextChar():
		nonlocal i
		nonlocal c
		i += 1
		c = text[i]

	# emulate a for loop (continue still increments)
	total_length = len(text)
	while True:
		if i + 1 >= total_length:
			break

		nextChar()

		# At the beginning of an object
		if c == '[':
			acc.write(c)
			nextChar()

			# parse out the type
			type = io.StringIO()

			while c != ']':
				type.write(c)
				acc.write(c)
				nextChar()

			# skip to the first argument
			while c != '(':
				acc.write(c)
				nextChar()
			
			acc.write(c)
			nextChar()

			type_string = type.getvalue()

			# Exit if the type is not in the functions

			if type_string in functions:
				arguments = io.StringIO()
				while c != ')':
					arguments.write(c)
					nextChar()

				argument_string = arguments.getvalue()
				has_arguments = len(argument_string) > 0
				func = functions[type.getvalue()]

				if has_arguments:
					func(output, argument_string)
				else:
					func(output)

			else:
				output.write(acc.getvalue())

			acc = io.StringIO()

		elif c == '~':
			nextChar()
			if c == '/':
				output.write(ref("~/"))
			else:
				output.write('~')
				output.write(c)

		else:
			output.write(c)

	return output.getvalue()