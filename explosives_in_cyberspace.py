# Almost complete solution to Advent of Code 2016 Problem 9. Uses and_then.

from mini_parse import exact, Grammar, string_grammar, template, none_char, \
    positive_int, get_n_chars, always

# parser returns a string, and we would get its length.

parser = Grammar(string_grammar)

parser.main = parser.part.times().concat_all()

parser.part = none_char('(') | template(
    '({grab:int}x{repeat:int})', {'int': positive_int}).and_then(
    lambda x: get_n_chars(x['grab']) >> (lambda y: y * x['repeat']))

# parser_2 returns a number.

parser_2 = Grammar(string_grammar)

parser_2.main = parser_2.part.times() >> sum

parser_2.part = (none_char('(') >> always(1)) | template(
    '({grab:int}x{repeat:int})', {'int': positive_int}).and_then(
    lambda x: get_n_chars(x['grab']) >> \
    (lambda y: parser_2.parse(y) * x['repeat']))
