import re
import argparse
from collections import Counter

def main(word_list, patterns):
    contains = []
    excluded = []
    new_pattern = []
    pattern_count = 0

    for pattern in patterns:
        ind = 0
        word_position = 0

        while ind < len(pattern):
            try:
                new_pattern[word_position]
            except IndexError:
                new_pattern.append([])

            if pattern[ind] == '?':
                ind += 1
                contains.append(pattern[ind])
                new_pattern[word_position].append(f'[^{pattern[ind]}{{excluded}}]')
            elif pattern[ind] == '!':
                ind += 1
                new_pattern[word_position].append('[^{excluded}]')
                excluded.append(pattern[ind])
            else:
                contains.append(pattern[ind])
                new_pattern[word_position].append(pattern[ind])

            ind += 1
            word_position += 1

        pattern_count += 1

    excluded = list(set(excluded) - set(contains))
    p_raw = ''.join(f'(?:{wp}.{{hack}})' for wp in [''.join([f'(?={p})' for p in lp]) for lp in new_pattern])
    repattern = re.compile(f"^{p_raw.format(excluded=''.join(excluded), hack='{1}')}$")

    cnuggets = ''.join([f'(?=.*{l.lower()})' for l in contains])
    cpattern = re.compile(f"{cnuggets}.+") if contains else re.compile('.*')

    letters = []
    matches = []

    words = open('word_list', 'r')
    for line in words:
        line = line.strip('\n')
        if repattern.search(line) and cpattern.search(line):
            matches.append({'word': line, 'strength': 0})
            letters.extend([l for l in line if l not in pattern])
        else:
            #print('no match yet')
            pass

    # most popular remaining letters
    pop_remaining = Counter(letters).most_common()
    for match in matches:
        strength = 0
        for l, s in pop_remaining:
            c = match['word'].count(l)
            strength += c * s

        match['strength'] = strength

    res = [l['word'] for l in sorted(matches, key=lambda item: item['strength'], reverse=True)]
    for r in res:
        print(f'{r}')

    print(f'Most popular remaining: {Counter(letters)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--word_list', type=str, required=True)
    parser.add_argument('--pattern', action='append')
    args = parser.parse_args()

    main(args.word_list, args.pattern)
