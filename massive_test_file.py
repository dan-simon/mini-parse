import and_then
import csv_parser
import template_test

assert template_test.template_grammmar.parse(
    '7 dragons who eat sheep; they make the knights and farmers weep') == \
    {'a': '7', 'c': ['knights', 'farmers'], 'b': 'dragons'}

assert and_then.binary_data.parse('b5:11001') == 25
assert and_then.binary_data.parse('b6:101010') == 42
assert and_then.binary_data.parse('b13:1101') == None
assert and_then.binary_data.parse('b3:10000') == None
