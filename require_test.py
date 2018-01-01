import mini_parse as mp

parser = mp.Grammar(mp.string_grammar)

parser.main = mp.require(mp.one_char().times(), lambda x: int(x) < 15)
