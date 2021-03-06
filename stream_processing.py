# Almost complete solution to Advent of Code 2017 Problem 9.

from mini_parse import exact, Grammar, string_grammar, one_char, none_char, always, foldl

parser = Grammar(string_grammar)

parser.main = parser.garbage | exact('{').and_second(
	  parser.main.join(parser.comma).optional([])).and_first(exact('}'))

parser.comma = exact(',')

parser.garbage = exact('<').and_second(parser.char.times().concat_all()).and_first(exact('>'))

parser.char = none_char('!>') | ((exact('!') + one_char()) >> always(''))

# Now let's do parts 1 and 2 with a parser for fun. We can reuse stuff from
# our old parser, of course.

# Part 1 is tricky. Ultimately it's probably just simpler to recurse
# through a list, but if you don't want to do that, you can go into
# a mess of lambdas and >>.

parser_1 = Grammar(string_grammar)

parser_1.main = (parser.garbage >> always(always(0))) | (exact('{').and_second(
	  parser_1.main.join(parser.comma).optional([])).and_first(exact('}'))) >> \
	  (lambda l: lambda d: d + sum(i(d + 1) for i in l))

# With Part 2, on the other hand, it makes sense to use a parser.

parser_2 = Grammar(string_grammar)

parser_2.main = parser_2.garbage | (exact('{').and_second(
	  parser_2.main.join(parser.comma).optional([])).and_first(exact('}')) >> sum)

parser_2.garbage = parser.garbage >> len

# Alternatively...

def part_1(p, x):
    return x + sum(part_1(i, x + 1) for i in p if type(i) == list)

def part_2(x):
	return len(p) if type(p) == str else sum(g_score(i) for i in p)

# Or alternatively, if you are against recursion...

parser_3 = Grammar(string_grammar)

depth = {'{': 1, '}': -1, ',': 0}
update = {'{': True, '}': False, ',': False}

fold_f = lambda c, new: (c[0], c[1], c[2] + new) if type(new) == int else \
    (c[0] + depth[new], c[1] + c[0] * update[new], c[2])

parser_3.main = \
    ((parser.garbage >> len) | exact('{') | exact('}') | exact(',')).times() >> \
	(lambda x: foldl(fold_f, (1, 0, 0), x)[1:])
