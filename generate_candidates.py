import argparse
import re


def load_words(words_file):
    with open(words_file) as f:
        return [word.strip() for word in f.readlines()]


def chars_in_word(chars, word):
    for c in chars:
        if(c not in word):
            return False

    return True


def chars_at_pos_in_word(chars_at_pos, word):
    for pos, c in chars_at_pos.items():
        if(word[pos-1] != c):
            return False
    return True


def parse_tries(tries):
    chars_must_have = set()
    chars_must_not = set()
    chars_at_pos = dict()
    chars_not_at_pos = dict()

    for t in tries:
        correct = re.findall(r"\((.)\)", t)
        correct_at_pos = re.findall(r"\[(.)\]", t)
        chars_must_have.update(correct)
        chars_must_have.update(correct_at_pos)

        t = ''.join(re.findall(r'[a-z]', t))

        for char in correct:
            pos = t.index(char)
            chars_not_at_pos[pos] = char

        for char in correct_at_pos:
            pos = t.index(char)
            chars_at_pos[pos] = char

        # get all gray chars (those that are not red or yellow)
        for char in t:
            if(char not in chars_must_have):
                chars_must_not.add(char)

    return chars_must_have, chars_must_not, chars_at_pos, chars_not_at_pos


def select_candidates(tries, words):
    chars_must_have, chars_must_not, chars_at_pos, chars_not_at_pos = parse_tries(tries)

    candidates = []

    for word in words:
        if not all([c in word for c in chars_must_have]):
            continue

        if any([c in word for c in chars_must_not]):
            continue

        if not all([word[pos] == c for pos,c in chars_at_pos.items()]):
            continue

        if any([word[pos] == c for pos,c in chars_not_at_pos.items()]):
            continue

        candidates.append(word)

    return candidates


if __name__ == "__main__":
    '''
    parser = argparse.ArgumentParser("Wordle helper")

    parser.add_argument("--filter-doubles", action="store_true")
    parser.add_argument("--filter-umlauts", action="store_true")

    words = load_words("words.txt")

    candidates = select_candidates(["p(e)nis","(k)lotz", "ac(k)(e)(r)"], words)

    print(candidates)
    '''
    pass
