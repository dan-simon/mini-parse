Just another way to parse in Python. Its benefits are that it's clean and very extensible.

Inspiration comes from Haskell's parser combinators and Perl 6's grammars.

There is a known bug where if you define a rule as being the same as a not-yet-defined rule, the rule itself acts as not defined and will not update when you define the new rule. This bug shouldn't be too hard to work around, but maybe I'll eventually fix it.
