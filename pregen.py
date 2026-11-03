wordlist = open("CEL22.txt").read().splitlines(keepends=False)
below6, above_or_eq6 = [], []
for word in wordlist:
    if len(word) >= 6:
        above_or_eq6.append(word)
    else:
        below6.append(word)


def is_subseq(x, y):
    it = iter(y)
    return all(c in it for c in x)


alphabet = "abcdefghijklmnopqrstuvwxyz" + "$"
letter_offset = {l: i for i, l in enumerate(alphabet)}
class Node:
    def __init__(self):
        self.next_ = [None] * 27
        self.count = 0
        self.bad = False

    def next(self, l: str):
        if self.next_[letter_offset[l]] is None:
            self.next_[letter_offset[l]] = Node()
        return self.next_[letter_offset[l]]

    def print(self, indent=0):
        spaced = "  " * indent
        print(f"Node({self.count})")
        for i, a in enumerate(alphabet):
            if self.next_[i] is not None:
                print(spaced + f"  {a}: ", end="")
                self.next_[i].print(indent+1)

    def get_all(self, minimum_amt=15):
        end = self.next_[letter_offset["$"]]
        if (end is not None) and (not end.bad) and (end.count >= minimum_amt):
            yield ""
        for i, letter in enumerate(alphabet[:-1]):
            if self.next_[i] is not None:
                for found in self.next_[i].get_all(minimum_amt):
                    yield letter + found


def all_puzzles(w: str):
    l = len(w)
    for i1 in range(l):
        for i2 in range(i1+1, l):
            for i3 in range(i2+1, l):
                yield w[i1]+w[i2]+w[i3]
                for i4 in range(i3+1, l):
                    yield w[i1]+w[i2]+w[i3]+w[i4]


def add(w: str, node: Node, bad=False):
    for puzzle in {*all_puzzles(w)}:
        cur = node
        for l in puzzle:
            cur = cur.next(l)
        if bad:
            cur.next("$").bad = True
        else:
            cur.next("$").count += 1


def main():
    root = Node()
    for b6 in below6:
        add(b6, root, True)
    print("done b6")
    for i, ae6 in enumerate(above_or_eq6):
        if i % 1000 == 0:
            print(i, len(above_or_eq6))
        add(ae6, root)
    print("done ae6")
    # root.print()
    puzzles_3, puzzles_4 = [], []
    for puzzle in root.get_all(15):
        [puzzles_3, puzzles_4][len(puzzle) == 4].append(puzzle)
    with open("valid_puzzles_3.txt", 'w') as f:
        for puzzle in puzzles_3:
            f.write(puzzle + "\n")
    with open("valid_puzzles_4.txt", 'w') as f:
        for puzzle in puzzles_4:
            f.write(puzzle + "\n")


if __name__ == '__main__':
    main()
