## wordle-cheat
---
A simple tool to beat the wordle odds

### Usage
You will need a word list. Perhaps https://github.com/dwyl/english-words

Pass a pathname to the word list to the script using the `--words_list` argument then guess your first word

With the results of your first word, create a pattern string, and pass it in with the `--pattern` argument

#### The pattern argument

The pattern argument is constructed by placing modifiers in front of the letter to denote its status
- `!` means this character is not in the word
- `?` means this character is in the word but not in this position
- A character that IS in the correct position does not need to be prepended

For example, your guess is HOUSE 🟨🟨⬛⬛🟩
pattern: `?h?o!u!se`

The script will output potential next words

Repeat the `--pattern` argument until you solve the puzzle

Example:
`python3 main.py --word_list='/words.txt' --pattern='?h?o!u!se' --pattern='!who!le'`
