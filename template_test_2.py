import mini_parse as mp

parser = mp.Grammar(mp.string_grammar)

parser.main = mp.template(
    '{lhs:variable}{!ws}={!ws}{rhs:value}',
    {'variable': parser.variable, 'value': parser.value, 'ws': mp.whitespace})

parser.variable = mp.exact('foo')

parser.value = mp.exact('5')
