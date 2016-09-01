from mini_parse import exact, none_char, one_of, Grammar, string_grammar

csv_grammar = Grammar(string_grammar)
csv_grammar.main = (csv_grammar.line & csv_grammar.eol).first().times()
csv_grammar.eol = one_of(['\n', '\r', '\r\n', '\n\r'])
csv_grammar.line = csv_grammar.cell.join(exact(','))
csv_grammar.cell = csv_grammar.quoted_cell | \
    none_char(',\n\r').plus().concat_all()
csv_grammar.quoted_cell = csv_grammar.quote.and_second(
	csv_grammar.quoted_char.plus().concat_all()).and_first(
    csv_grammar.quote)
csv_grammar.quoted_char = none_char('"') | exact('""').goes_to('"')
csv_grammar.quote = exact('"')
