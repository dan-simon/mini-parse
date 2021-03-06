import and_then
import csv_parser
import template_test
import consistency
import times_test
import repeat_test
import require_test
import template_test_2
import broken_grammar
from mini_parse import UninitializedRuleError

assert template_test.template_grammar.parse(
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

assert times_test.parser.parse('') == []

assert times_test.parser.parse('apple') == ['a', 'p', 'p', 'l', 'e']

assert times_test.parser.parse('5') == ['5']

assert times_test.parser.parse('8') == ['8']

assert times_test.parser.parse('12') == ['1', '2']

assert times_test.parser.parse('27') == ['2', '7']

assert repeat_test.parser.parse('') == None

assert repeat_test.parser.parse('!') == ['!']

assert repeat_test.parser.parse('!!') == None

assert repeat_test.parser.parse('#') == None

assert repeat_test.parser.parse('#!') == None

assert repeat_test.parser.parse('!#') == None

assert require_test.parser.parse('5') == None

assert require_test.parser.parse('8') == ['8']

assert require_test.parser.parse('12') == ['1', '2']

assert require_test.parser.parse('25') == None

assert template_test_2.parser.parse('foo = 5') == {'lhs': 'foo', 'rhs': '5'}

assert template_test_2.parser.parse('foo = 6') == None

try:
    broken_grammar.parser.parse('test')
    assert False
except UninitializedRuleError as e:
    assert str(e) == 'Failed to create rule \'missing\''
