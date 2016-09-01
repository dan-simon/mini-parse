from mini_parse import exact, Grammar, string_grammar, get_next_n, one_char, digit

integer = digit.plus().concat_all() >> int

binary_data = Grammar(string_grammar)

binary_data.main = (exact('b').and_second(integer)).and_then(
	lambda size: exact(':').and_second(get_next_n(size)))
