from mini_parse import Grammar, string_grammar, template, digit, letter, exact

template_grammmar = Grammar(string_grammar)

template_grammmar.main = template(
    '{a:digit} {b:dragons} {!:id}; {!:id} {c:people} {!:id}',
    {'digit': digit, 'id': (letter | exact(' ')).plus().concat_all(),
    'people': letter.plus().concat_all().join(exact(' and '), 2)})
