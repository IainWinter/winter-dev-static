type StyleMap = { [key: string]: string };

const gCodeStyles: StyleMap = {
	'w': 'code-w', // fields / namespaces  -> white
	's': 'code-s', // symbol               -> grey  
	'a': 'code-a', // argument             -> dark  
	'n': 'code-n', // namespace            -> a shade lighter than grey
	'v': 'code-v', // local variable       -> light-blue
	'c': 'code-c', // comment              -> green
	'r': 'code-r', // reserved             -> purple
	'j': 'code-j', // control flow (jump)  -> blue
	't': 'code-t', // type                 -> green
	'f': 'code-f', // function             -> yellow
	'd': 'code-d', // digit                -> light-green
	'p': "code-p", // pre-processor        -> light-purple
	'l': "code-l", // inner string literal -> literal
	'q': "code-q", // quote                -> quote, in light mode these are different than the contents >:(
	'm': "code-m"  // magic                -> magic functions
};

const gAutoStylesCpp: StyleMap = {
	'(': 's', ')': 's',
	'[': 's', ']': 's',
	'{': 's', '}': 's',
	'<': 's', '>': 's',
	'+': 's', '-': 's', '*': 's', '/': 's', '^': 's', '!': 's', '=': 's',
	'&': 's', '|': 's', '%': 's',
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

	// my stuff

	'm_': 'w', // most of my member vars begin with m_

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
};

const gAutoStylesProcessing: StyleMap = {
	'(': 's', ')': 's',
	'[': 's', ']': 's',
	'{': 's', '}': 's',
	'<': 's', '>': 's',
	'+': 's', '-': 's', '*': 's', '/': 's', '^': 's', '!': 's', '=': 's',
	'&': 's', '|': 's',
	',': 's', '.': 's', ':': 's',
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
};

const gAutoStylesJavascript: StyleMap = {
	'(': 's', ')': 's',
	'[': 's', ']': 's',
	'{': 's', '}': 's',
	'<': 's', '>': 's',
	'+': 's', '-': 's', '*': 's', '/': 's', '^': 's', '!': 's', '=': 's',
	'&': 's', '|': 's',
	',': 's', '.': 's', ':': 's',
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
};

const gAutoStylesAvalible: { [key: string]: StyleMap } = {
	"cpp": gAutoStylesCpp,
	"processing": gAutoStylesProcessing,
	"javascript": gAutoStylesJavascript
};

function isLetter(source: string, index: number): boolean {
	if (index < 0 || index >= source.length) return false;
	const char = source[index];
	return char === '_' || /^[a-zA-Z]$/.test(char);
}

function isDigit(source: string, index: number): boolean {
	if (index < 0 || index >= source.length) return false;
	const char = source[index];
	return '0123456789.fdl u'.includes(char);
}

function findLongestMatch(source: string, index: number, against: { [key: string]: any }): string {
	const avalible: string[] = [];
	const sourceBeforeIsLetter = isLetter(source, index - 1);

	for (const test in against) {
		if (test[0] !== source[index]) continue;
		const test_len = test.length;
		const sourceAfterIsLetter = isLetter(source, index + test_len);
		const testBeginsWithLetter = isLetter(test, 0);
		const testEndsWithLetter = isLetter(test, test_len - 1);
		const testEndsWithWildcard = test_len > 1 && test[test_len - 1] === '_';

		if (sourceBeforeIsLetter && testBeginsWithLetter) continue;
		if (!testEndsWithWildcard && sourceAfterIsLetter && testEndsWithLetter) continue;
		avalible.push(test);
	}

	let longestMatch = '';
	let lengthMatched = 0;

	for (const test of avalible) {
		let matched = 0;
		for (let tIndex = 0; tIndex < test.length; tIndex++) {
			if (test[tIndex] !== source[index + tIndex]) break;
			matched++;
		}
		if (matched > lengthMatched) {
			longestMatch = test;
			lengthMatched = matched;
		}
	}

	if (lengthMatched !== longestMatch.length) return '';
	return longestMatch;
}

function insertAutoStyles(codeTemplate: string, styles: { [key: string]: any }): string {
	let out = '';
	let inComment = 0;
	let inString = false;
	let cIndex = -1;

	while (cIndex + 1 < codeTemplate.length) {
		cIndex++;
		const c0 = codeTemplate[cIndex];

		if (c0 === '"') {
			inString = !inString;
			if (inString) out += '`l`';
		}

		if (cIndex + 1 < codeTemplate.length) {
			const c1 = codeTemplate[cIndex + 1];
			if ((inComment === 0 && c0 === '/' && c1 === '/') || (c0 === '/' && c1 === '*')) {
				inComment += 1;
				out += '`c`';
			}
			if (inComment > 0 && (c0 === '\n' || (c0 === '*' && c1 === '/'))) {
				inComment -= 1;
			}
		}

		if (inComment !== 0 || inString) {
			out += codeTemplate[cIndex];
			continue;
		}

		if (!isLetter(codeTemplate, cIndex - 1) && isDigit(codeTemplate, cIndex) && !isLetter(codeTemplate, cIndex + 1)) {
			out += '`d`';
			while (true) {
				out += codeTemplate[cIndex];
				cIndex++;
				if (!isDigit(codeTemplate, cIndex)) break;
			}
			cIndex--;
			continue;
		}

		if (cIndex - 1 >= 0 && codeTemplate[cIndex - 1] === '`') {
			out += codeTemplate[cIndex];
			continue;
		}

		const match = findLongestMatch(codeTemplate, cIndex, styles);
		if (match !== '') {
			out += `\`${styles[match]}\`${match}`;
			cIndex += match.length - 1;
		} else {
			out += codeTemplate[cIndex];
		}
	}

	return out;
}

export function renderCode(codeTemplate: string, autoStyleType: string): string {
	if (autoStyleType in gAutoStylesAvalible) {
		codeTemplate = insertAutoStyles(codeTemplate, gAutoStylesAvalible[autoStyleType]);
	}

	let out = '';
	let acc = '';
	let cIndex = -1;

	while (cIndex + 1 < codeTemplate.length) {
		cIndex++;
		let c = codeTemplate[cIndex];

		if (c !== '`') {
			if (c === '>') c = '&gt';
			else if (c === '<') c = '&lt';
			acc += c;
			continue;
		}

		if (acc.length > 0) {
			out += acc + '</span>';
			acc = '';
		}

		cIndex++;
		const style = gCodeStyles[codeTemplate[cIndex]];
		acc += `<span class="${style}">`;
		cIndex++;
	}

	out += acc + '</span>';
	return out;
}