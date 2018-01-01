import mini_parse as mp

parser = mp.Grammar(mp.string_grammar)

parser.main = mp.require(mp.one_char().times(),
    lambda x: x and x[-1] in '24680')
