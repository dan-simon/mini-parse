from mini_parse import exact, Grammar, string_grammar

parser = Grammar(string_grammar)

parser.main = exact('!').repeat(1)
