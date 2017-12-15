import and_then
import csv_parser
import template_test
import consistency

assert template_test.template_grammmar.parse(
    '7 dragons who eat sheep; they make the knights and farmers weep') == \
    {'a': '7', 'c': ['knights', 'farmers'], 'b': 'dragons'}

assert and_then.binary_data.parse('b5:11001') == 25
assert and_then.binary_data.parse('b6:101010') == 42
assert and_then.binary_data.parse('b13:1101') == None
assert and_then.binary_data.parse('b3:10000') == None

assert csv_parser.csv_grammar.parse('""""\n') == [['"']]
assert csv_parser.csv_grammar.parse('a,b', 'line') == ['a', 'b']
assert csv_parser.csv_grammar.parse('a,b\n') == [['a', 'b']]
assert csv_parser.csv_grammar.parse('a!e,b\r\n"cat",dragon\r') == \
    [['a!e', 'b'], ['cat', 'dragon']]

# There was an annoying use of a generator instead of a list
# which made one_of only work once. This is here to avoid reversion.
assert consistency.consistency.parse('a') == 'a'
assert consistency.consistency.parse('g') == 'g'
assert consistency.consistency.parse('d') == 'd'
assert consistency.consistency.parse('a') == 'a'
assert consistency.consistency.parse('h') == None
assert consistency.consistency.parse('a') == 'a'
