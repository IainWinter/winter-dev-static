gCodeStyles = {
	'w': 'code-w', # fields / namespaces  -> white
	's': 'code-s', # symbol               -> grey  
	'a': 'code-a', # argument             -> dark  
	'n': 'code-n', # namespace            -> a shade lighter than grey
	'v': 'code-v', # local variable       -> light-blue
	'c': 'code-c', # comment              -> green
	'r': 'code-r', # reserved             -> purple
	'j': 'code-j', # control flow (jump)  -> blue
	't': 'code-t', # type                 -> green
	'f': 'code-f', # function             -> yellow
	'd': 'code-d', # digit                -> light-green
	'p': "code-p", # pre-processor        -> light-purple
	'l': "code-l", # inner string literal -> literal
	'q': "code-q", # quote                -> quote, in light mode these are different than the contents >:(
	'm': "code-m"  # magic                -> magic functions
}

gAutoStylesCpp = {
	'(': 's', ')': 's',
	'[': 's', ']': 's',
	'{': 's', '}': 's',
	'<': 's', '>': 's',
	'+': 's', '-': 's', '*': 's', '/': 's', '^': 's', '!': 's', '=': 's',
	'&': 's', '*': 's', '&': 's', '|': 's', '%': 's',
	',': 's', '.': 's', ';': 's', ':': 's',
	'?': 's',

	'"': 'q',
	'\'': 'q',

	'::': 's', 'and': 's', 'or': 's',

	'std': 'n',
	
	'if': 'j',
	'else': 'j',
	'for': 'j',
	'while': 'j',
	'switch': 'j',
	'case': 'j',
	'continue': 'j',
	'break': 'j',
	'return': 'j',
	'goto': 'j',

	'new': 'r',
	'delete': 'r',
	'delete': 'r',
	'class': 'r',
	'struct': 'r',
	'enum': 'r',
	'public': 'r',
	'private': 'r',
	'protected': 'r',
	'static': 'r',
	'const': 'r',
	'void': 'r',
	'bool': 'r',
	'boolean': 'r',
	'char': 'r',
	'int': 'r',
	'long': 'r',
	'double': 'r',
	'float': 'r',
	'unsigned': 'r',
	'auto': 'r',
	'nullptr': 'r',
	'this': 'r',
	'true': 'r',
	'false': 'r',
	'template': 'r',
	'typename': 'r',
	'virtual': 'r',
	'override': 'r',
	'using': 'r',
	'inline': 'r',
	'sizeof': 'r',

	'operator': 'r',
	'operator=': 's',
	'operator|': 's',
	'operator&': 's',

	'size_t': 't',
	'uint64_t': 't',
	'uint32_t': 't',

	'vector': 't',
	'pair': 't',
	'tuple': 't',
	'unordered_map': 't',
	'unordered_set': 't',
	'map': 't',
	'set': 't',
	'mutex': 't',
	'condition_variable': 't',
	'function': 't',
	'unique_lock': 't',
	'initializer_list': 't',
	'array': 't',

	'#define': 'a',
	'#include': 'a',
	'#pragma once': 'a',

	'FLT_MAX': 'p',

	'0b': 'd',

	# my stuff

	'm_': 'w', # most of my member vars begin with m_

	'vec2': 't',
	'vec3': 't',
	'vec4': 't',
	'quat': 't',

	'dot': 'f',
	'normalized': 'f',
	'clamp': 'f',
	'cross': 'f',
	'sin': 'f',
	'cos': 'f',
}

gAutoStylesProcessing = {
	'(': 's', ')': 's',
	'[': 's', ']': 's',
	'{': 's', '}': 's',
	'<': 's', '>': 's',
	'+': 's', '-': 's', '*': 's', '/': 's', '^': 's', '!': 's', '=': 's',
	'&': 's', '*': 's', '&': 's', '|': 's',
	',': 's', '.': 's', ':': 's', ':': 's',
	'?': 's',

	'"': 'q',
	'\'': 'q',

	'and': 's', 'or': 's',

	'if': 'j',
	'else': 'j',
	'for': 'j',
	'while': 'j',
	'switch': 'j',
	'case': 'j',
	'goto': 'j',
	
	'return': 'r',
	'new': 'r',
	'class': 'r',
	'struct': 'r',
	'public': 'r',
	'private': 'r',
	'protected': 'r',
	'static': 'r',
	'const': 'r',
	'void': 'r',

	'boolean': 't',
	'char': 't',
	'int': 't',
	'long': 't',
	'double': 't',
	'float': 't',

	'this': 'r',
	'true': 'r',
	'false': 'r',
}

gAutoStylesJavascript = {
	'(': 's', ')': 's',
	'[': 's', ']': 's',
	'{': 's', '}': 's',
	'<': 's', '>': 's',
	'+': 's', '-': 's', '*': 's', '/': 's', '^': 's', '!': 's', '=': 's',
	'&': 's', '*': 's', '&': 's', '|': 's',
	',': 's', '.': 's', ':': 's', ':': 's',
	'?': 's',
	'and': 's', 'or': 's',

	'"': 'q',
	'\'': 'q',

	'if': 'j',
	'else': 'j',
	'for': 'j',
	'while': 'j',
	'switch': 'j',
	'case': 'j',
	
	'return': 'r',
	'new': 'r',
	'class': 'r',
	'let': 'r',
	'var': 'r',
	'const': 'r',
	'function': 'r',
	'Infinity': 'r',

	'this': 'r',
	'true': 'r',
	'false': 'r',
}

gAutoStylesAvalible = {
	"cpp": gAutoStylesCpp,
	"processing": gAutoStylesProcessing,
	"javascript": gAutoStylesJavascript
}

def isLetter(source: str, index: int) -> bool:
	if index < 0 or index >= len(source):
		return False

	# _ is a wildcard for symbols which arn't whitespace

	char = source[index]
	return char == '_' or char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def isDigit(source: str, index: int) -> bool:
	if index < 0 or index >= len(source):
		return False
	
	char = source[index]

	return char == '0'  \
		or char == '1'  \
		or char == '2'  \
		or char == '3'  \
		or char == '4'  \
		or char == '5'  \
		or char == '6'  \
		or char == '7'  \
		or char == '8'  \
		or char == '9'  \
		or char == '.'  \
		or char == 'f'  \
		or char == 'd'  \
		or char == 'l'  \
		or char == 'u'  \

# return the longest string in against which is a prefix for the string at source[index]
# there can only be a single match
# if a string in against start/ends with a letter, the letter before/after can be any non-letter
# returns the empty string if there is no match
def findLongestMatch(source: str, index: int, against) -> str:
	# consider only those which match the wildcard conditions
	# -> if a test begins with a letter, and the source also had a letter before it, no match
	# -> if a test ends with a letter, and the source has a letter after the would be match, no match
	
	# MATCH()
	# thiswillnotMATCH()
	
	avalible = []
	sourceBeforeIsLetter = isLetter(source, index - 1)

	for test in against:
		# can test first letter to remove most options

		if test[0] != source[index]:
			continue

		test_len = len(test)

		sourceAfterIsLetter = isLetter(source, index + test_len)
		testBeginsWithLetter = isLetter(test, 0)
		testEndsWithLetter = isLetter(test, test_len - 1)
		testEndsWithWildcard = test_len > 1 and test[test_len - 1] == '_' # This is only for my m_ thing
		
		if sourceBeforeIsLetter and testBeginsWithLetter: # aNOMATCH
			continue
		
		if not testEndsWithWildcard and sourceAfterIsLetter and testEndsWithLetter:  # NOMATCHa
			continue

		avalible.append(test)

	# count number of chars which match for each string, if there are no fully qualified matches, take the longest

	longestMatch = ''
	lengthMatched = 0

	for test in avalible:
		matched = 0

		for tIndex in range(len(test)):
			testChar = test[tIndex]
			sourceChar = source[index + tIndex]

			if testChar != sourceChar:
				break

			matched += 1

		if matched > lengthMatched:
			longestMatch = test
			lengthMatched = matched

	if lengthMatched != len(longestMatch):
		return ""

	return longestMatch

# return a copy of codeTemplate with specified words prepended with `x` styles where x is a letter
def insertAutoStyles(codeTemplate: str, styles) -> str:
	out = ''
	inComment = 0
	inString = False

	code_template_len = len(codeTemplate)
	cIndex = -1
	while True:
		if cIndex + 1 >= code_template_len:
			break
		cIndex += 1

		# if found " disable until next "

		if codeTemplate[cIndex] == '"':
			inString = not inString
			if inString:
				out += '`l`'

		# if found // disable until new line
		# if found /* disable until the same number of */ have been found

		if cIndex + 1 < len(codeTemplate):
			c0 = codeTemplate[cIndex]
			c1 = codeTemplate[cIndex + 1]

			# this has some bad edge cases

			if (inComment == 0 and c0 == '/' and c1 == '/') or (c0 == '/' and c1 == '*'):
				inComment += 1
				out += '`c`'

			if (inComment > 0) and ( (c0 == '\n') or (c0 == '*' and c1 == '/')):
				inComment -= 1

		if inComment != 0 or inString:
			out += codeTemplate[cIndex]
			continue

		# numbers

		if not isLetter(codeTemplate, cIndex - 1) and isDigit(codeTemplate, cIndex) and not isLetter(codeTemplate, cIndex + 1):
			out += '`d`'

			while (True):
				out += codeTemplate[cIndex] 
				cIndex += 1

				if not isDigit(codeTemplate, cIndex):
					break

			# reset back to before last char
			cIndex -= 1
			continue

		if cIndex - 1 >= 0 and codeTemplate[cIndex - 1] == '`':
			out += codeTemplate[cIndex]
			continue

		match = findLongestMatch(codeTemplate, cIndex, styles.keys())

		if match != "":
			out += f'`{styles.get(match)}`{match}'
			cIndex += len(match) - 1 # -1 because we add one on loop

		else:
			out += codeTemplate[cIndex]

	return out

def render_code(codeTemplate: str, autoStyleType: str) -> str:
	if autoStyleType in gAutoStylesAvalible:
		codeTemplate = insertAutoStyles(codeTemplate, gAutoStylesAvalible.get(autoStyleType))

	out = ''
	acc = ''

	code_template_len = len(codeTemplate)
	cIndex = -1
	while True:
		if cIndex + 1 >= code_template_len:
			break
		cIndex += 1

		c = codeTemplate[cIndex]

		# if the char is not a delimiter, accumulate
		if c != '`':
			# wait! need to replace < and > with their escape sequences for HTML
			if   c == '>': c = '&gt'
			elif c == '<': c = '&lt'

			acc += c

			continue

		# if the char is a delimiter & there is have content, append it
		if len(acc) > 0:
			out += acc + '</span>'
			acc = ''

		# at the start of the next delimiter

		cIndex += 1 # skip it

		style = gCodeStyles.get(codeTemplate[cIndex]) # get style flag, supports only single letters
		acc += f'<span class="{style}">'

 		# skip the flag, loop will skip delim
		cIndex += 1

	# add anything left over if EOF
	out += acc + '</span>'

	return out