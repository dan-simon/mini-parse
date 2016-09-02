from mini_parse import Grammar, string_grammar, and_series, or_series, \
    and_then_series, exact, get_n_chars

series_test = Grammar(string_grammar)
series_test.space = exact(' ')
series_test.main = and_series([
    series_test.and_test, series_test.space, series_test.or_test,
    series_test.space, series_test.and_then_test])
series_test.and_test = and_series([exact('a'), exact('b') | exact('bc'), exact('d')])
series_test.or_test = or_series([
    exact('e'), exact('f') | (exact('g') & exact('h')), exact('i') & exact('j')])
series_test.and_then_test = and_then_series(
    [exact('k') + exact('lm'), lambda s: get_n_chars(len(s)), lambda t: exact(t + 'n')])
print(series_test.parse('abcd f klm1212n'))
