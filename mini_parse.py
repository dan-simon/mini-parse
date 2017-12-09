# For compatibility with Python 2, we have all our classes extend object.

class GrammarGen(object):
    def __init__(self, init_state, over):
        self.init_state = init_state
        self.over = over

    def parse(self, value, rule):
        start = self.init_state(value)
        result = rule.run(value, start)
        for i in result:
            if self.over(value, i[1]):
                return i[0]
        return None

class Grammar(object):
    def __init__(self, grammar_gen):
        self.__dict__['rules'] = {};
        self.__dict__['grammar_gen'] = grammar_gen

    def __getattr__(self, name):
        rules = self.__dict__['rules']
        rules.setdefault(name, Rule())
        return rules[name]

    def __setattr__(self, name, value):
        if name in self.rules:
            if type(value) == Rule:
                # Change just a method so that references to the object
                # still return the same object.
               self.rules[name].run = value.run
            else:
                # We've somehow initialized a property, presumably by
                # referring to it, but we're setting it to a non-rule.
                # This makes it hard to keep it the same object
                # (as needed due to our earlier reference to it).
                # Alternatively, we could have defined it and now be
                # redefining it, which we could do. I've decided that
                # until someone does this in practice I won't worry about it.
                raise ValueError('Setting already-used property to non-rule. '
                                 'This usually won\'t do what you expect; '
                                 'if it seems to make sense in your context, '
                                 'please create an issue.')
        else:
            self.rules[name] = value

    def parse(self, value):
        return self.__dict__['grammar_gen'].parse(value, self.main)

class Rule(object):
    def __init__(self, run=None):
        self.run = run

# Ways of creating rules.

def to_output(output_trans):
    def f(rule):
        def g(matched, state):
            result = rule.run(matched, state)
            for i in result:
                yield output_trans(i[0]), i[1]
        return Rule(g)
    return f

Rule.to_output = lambda x, y: to_output(y)(x)

Rule.__rshift__ = Rule.to_output

# This is here since >> always(junk value) can be helpful.
always = lambda x: lambda y: x

Rule.goes_to = lambda x, y: to_output(lambda _: y)(x)

def concat(rule1, rule2):
    def f(matched, state):
        result1 = rule1.run(matched, state)
        for match1, state1 in result1:
            result2 = rule2.run(matched, state1)
            for match2, state2 in result2:
                yield (match1, match2), state2
    return Rule(f)

Rule.__and__ = concat
Rule.__add__ = concat
Rule.concat = concat

def either(rule1, rule2):
    def f(matched, state):
        for i in rule1.run(matched, state):
            yield i
        for j in rule2.run(matched, state):
            yield j
    return Rule(f)

Rule.__or__ = either
Rule.either = either

def and_then(rule1, result_to_rule2):
    def f(matched, state):
        result1 = rule1.run(matched, state)
        for match1, state1 in result1:
            rule2 = result_to_rule2(match1)
            result2 = rule2.run(matched, state1)
            for i in result2:
                yield i
    return Rule(f)

Rule.and_then = and_then

def rule_series(rules, to_get):
    if not rules:
        return auto([])
    rule_count = len(rules)
    def f(matched, state):
        items = 1
        states = [state]
        runs = [rules[0].run(matched, state)]
        l = []
        while True:
            try:
                n = next(runs[-1])
                l.append(n[0])
                if items == rule_count:
                    yield l, n[1]
                    l.pop()
                else:
                    states.append(n[1])
                    g = to_get(rules, items, n[0])
                    runs.append(g.run(matched, n[1]))
                    items += 1
            except StopIteration:
                s = states.pop()
                runs.pop()
                items -= 1
                if l:
                    l.pop()
                else:
                    break
    return Rule(f)

def and_series(rules):
    to_get = lambda rules, items, _: rules[items]
    return rule_series(rules, to_get)

def or_series(rules):
    def f(matched, state):
        for rule in rules:
            for i in rule.run(matched, state):
                yield i
    return Rule(f)

def and_then_series(rules):
    to_get = lambda rules, items, match: rules[items](match)
    return rule_series(rules, to_get)

def require(rule, cond):
    def f(matched, state):
        for i in rule.run(matched, state):
            if cond(i[0]):
                yield i
    return Rule(f)

Rule.require = require

def repeat(rule, a, b='equal'):
    if b == 'equal':
        b = a
    def good(l):
        return a <= len(l)
    def would_be_too_long(l):
        return len(l) == b
    def f(matched, state):
        states = [state]
        runs = [rule.run(matched, state)]
        l = []
        while True:
            try:
                if would_be_too_long(l):
                    raise StopIteration
                n = next(runs[-1])
                l.append(n[0])
                states.append(n[1])
                runs.append(rule.run(matched, n[1]))
            except StopIteration:
                s = states.pop()
                runs.pop()
                if good(l):
                    yield l, s
                if l:
                    l.pop()
                else:
                    break
    return Rule(f)

Rule.repeat = repeat

def times(rule):
    return rule.repeat(0, '*')

Rule.times = times

def plus(rule):
    return rule.repeat(1, '*')

Rule.plus = plus

def auto(null=None):
    def f(x, y):
        yield (null, y)
    return Rule(f)

def optional(rule, null=None):
    return rule | auto(null)

Rule.optional = optional

def join(rule, sep_rule):
    return (rule & (sep_rule & rule).second().times()).to_output(
        lambda x: [x[0]] + x[1])

Rule.join = join

Rule.first = to_output(lambda x: x[0])

Rule.second = to_output(lambda x: x[1])

Rule.and_first = lambda rule1, rule2: (rule1 & rule2).first()

Rule.and_second = lambda rule1, rule2: (rule1 & rule2).second()

# String stuff below.

string_grammar = GrammarGen(lambda _: 0, lambda v, pos: len(v) == pos)

string_grammar_inexhaustive = GrammarGen(lambda _: 0, lambda v, pos: True)

def get_next(string, pos):
    if pos < len(string):
        return string[pos]
    else:
        return None

def get_next_n(n):
    def f(string, pos):
        if pos + n <= len(string):
            yield string[pos:pos + n], pos + n
    return Rule(f)

get_n_chars = get_next_n

def exact(string):
    l = len(string)
    def f(matched, pos):
        if matched[pos:pos + l] == string:
            yield string, pos + l
    return Rule(f)

def one_char(s=None):
    if s is not None:
        s = set(s)
    def f(matched, pos):
        g = get_next(matched, pos)
        if s is None or (g in s and g is not None):
            yield g, pos + 1
    return Rule(f)

def none_char(s):
    if s is not None:
        s = set(s)
    def f(matched, pos):
        g = get_next(matched, pos)
        if s is not None and (g not in s and g is not None):
            yield g, pos + 1
    return Rule(f)

def one_of(s):
    rules = map(exact, s)
    def f(matched, pos):
        for i in rules:
            result = i.run(matched, pos)
            for i in result:
                yield i
    return Rule(f)

def map_by(my_map):
    if type(my_map) == dict:
        my_map = my_map.items()
    rules = [(exact(i), j) for i, j in my_map]
    def f(matched, pos):
        for i in rules:
            result = i.run(matched, pos)
            for i in result:
                yield j, i[1]
    return Rule(f)

def concat_all(rule):
    def f(x):
        if type(x) == str:
            return x
        else:
            return ''.join(map(f, x))
    return rule.to_output(f)

Rule.concat_all = concat_all

# Some special useful parsers.

digit = one_char('013456789')

upper_case = one_char([chr(i) for i in range(ord('A'), ord('Z') + 1)])

lower_case = one_char([chr(i) for i in range(ord('a'), ord('z') + 1)])

letter = upper_case | lower_case

whitespace_char = one_of(' \t\n\r')
whitespace = whitespace_char.times()

# Some functional constructs. What are these doing here? The hope is that
# they might be useful as transformers of list output.

def foldl(f, start, l):
    s = start
    for i in l:
        s = f(s, i)
    return s
