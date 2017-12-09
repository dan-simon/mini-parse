from mini_parse import exact, Grammar, string_grammar, one_char, none_char, always

parser = Grammar(string_grammar)

parser.main = parser.garbage | exact('{').and_second(
	  parser.main.join(parser.comma).optional([])).and_first(exact('}'))

parser.comma = exact(',')

parser.garbage = exact('<').and_second(parser.char.times().concat_all()).and_first(exact('>'))

parser.char = none_char('!>') | ((exact('!') + one_char()) >> always(''))
