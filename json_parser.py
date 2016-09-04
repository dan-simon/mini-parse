from mini_parse import exact, Grammar, string_grammar, one_char, none_char, \
    one_of, map_by, digit, whitespace

def pairs_to_dict(pairs):
	d = {}
	for i, j in pairs:
		d[i] = j
	return d

escapes = {
	'"': '"',
	'\\': '\\',
	'/': '/',
	'b': '\b',
	'f': '\f',
	'n': '\n',
	'r': '\r',
	't': '\t'
}

def read_hex(digits):
	d = int(digits, 16)
	return chr(d)

def surround_by_ws(rule):
	return whitespace.and_second(rule).and_first(whitespace)

sign_lambda = lambda t: -t[1] if t[0] == '-' else t[1]

json = Grammar(string_grammar)
json.main = json.object
json.value = json.string | json.number | json.object | json.array | json.bool | json.null
json.bool = exact('true').goes_to(True) | exact('false').goes_to(False)
json.null = exact('null').goes_to(None)

json.colon = surround_by_ws(exact(':'))
json.comma = surround_by_ws(exact(','))

json.array = surround_by_ws(exact('[')).and_second(
	json.value.join(json.comma).optional([])).and_first(
	surround_by_ws(exact(']')))

json.object = surround_by_ws(exact('{')).and_second(
	(json.pair.join(json.comma) >> pairs_to_dict).optional({})).and_first(
	surround_by_ws(exact('}')))

json.pair = json.string.and_first(json.colon) & json.value
json.string = exact('"').and_second(json.char.times().concat_all()).and_first(exact('"'))
json.char = none_char('\\"').require(lambda x: ord(x) >= 32) | (
	exact('\\') + json.backslash_escape).concat_all()
json.backslash_escape = map_by(escapes) | exact('u').and_second(
	json.hex.repeat(4).concat_all() >> read_hex)
json.hex = one_char('0123456789abcdefABCDEF')

json.number = (((json.int + json.frac) >> (lambda x: x[0] + x[1])) + json.exp) >> (
	lambda x: x[0] * 10 ** x[1])

json.int = (exact('-').optional() + json.plus_int) >> sign_lambda
json.plus_int = (exact('0') | (one_of('123456789') + json.digits).concat_all()) >> int
json.frac = ((exact('.') & json.digits).concat_all() >> float).optional(0)
json.digits = digit.times().concat_all()
json.exp = ((json.e + (json.digits >> int)) >> sign_lambda).optional(0)
json.e = one_char('eE').and_second(one_of(['+', '-', ''])) >> (
	lambda x: '-' if x == '-' else '')
