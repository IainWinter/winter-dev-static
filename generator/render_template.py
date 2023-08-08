import io

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
				argument_string = io.StringIO()
				while c != ')':
					argument_string.write(c)
					nextChar()

				functions[type_string](output, argument_string.getvalue())

			else:
				output.write(acc.getvalue())

			acc = io.StringIO()

		else:
			output.write(c)

	return output.getvalue()