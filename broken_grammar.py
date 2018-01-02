import mini_parse as mp

parser = mp.Grammar(mp.string_grammar)

parser.main = parser.missing
