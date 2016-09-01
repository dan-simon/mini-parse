from mini_parse import Grammar, string_grammar, one_char, exact

monkey = Grammar(string_grammar)
monkey.stop = one_char('bd')
monkey.plosive = monkey.stop & exact('a')
monkey.syllable = (monkey.plosive + monkey.stop.optional()) | (
    exact('a') + (monkey.plosive | monkey.stop))
monkey.word = monkey.syllable + monkey.syllable.repeat(2).times()
monkey.sentence = monkey.word.join(exact('#'))
monkey.main = monkey.sentence

print(monkey.parse('ba#ababadada#bad#dabbada'))
print(monkey.parse('abdabaadab#ada'))
print(monkey.parse('dad#ad#abaadad#badadbaad'))
