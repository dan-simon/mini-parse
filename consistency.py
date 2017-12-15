from mini_parse import one_of, Grammar, string_grammar

consistency = Grammar(string_grammar)

consistency.main = one_of(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
