from typing import Optional

wordlist = open("CEL22.txt").read().splitlines(keepends=False)


def is_subseq(x, y):
    it = iter(y)
    return all(c in it for c in x)


alphabet = "abcdefghijklmnopqrstuvwxyz" + "$"
letter_offset = {l: i for i, l in enumerate(alphabet)}
class Node:
    def __init__(self):
        self.next_: list[Optional[Node]] = [None] * 27
        self.count = 0
        self.bad = False
        self.bullseye_length = 999
        self.min_length = 999
        self.bullseye_relpts = 0

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

    def get_all(self, minimum_amt=15, bullseye_length=6):
        end = self.next_[letter_offset["$"]]
        if (end is not None) and (not end.bad) and (end.count >= minimum_amt):
            yield "", end.bullseye_length
        for i, letter in enumerate(alphabet[:-1]):
            if self.next_[i] is not None:
                for found, bullseye_length in self.next_[i].get_all(minimum_amt, bullseye_length):
                    yield letter + found, bullseye_length


def all_puzzles(w: str):
    l = len(w)
    for i1 in range(l):
        for i2 in range(i1+1, l):
            for i3 in range(i2+1, l):
                yield w[i1]+w[i2]+w[i3]
                for i4 in range(i3+1, l):
                    yield w[i1]+w[i2]+w[i3]+w[i4]


def add(w: str, node: Node):
    w0 = w[0]
    for puzzle in {*all_puzzles(w)}:
        cur = node
        for l in puzzle:
            cur = cur.next(l)
        end = cur.next("$")
        if len(w) < 6:
            end.bad = True
        end.count += 1

        prev_relpts = end.bullseye_relpts
        if end.bullseye_length == end.min_length:
            prev_relpts -= 250
        else:
            prev_relpts -= max(0, 150 - 25 * (end.bullseye_length - 7))
        end.min_length = min(end.min_length, len(w))
        new_relpts = 250 if puzzle[0] != w0 else 0
        if len(w) == end.min_length:
            new_relpts += 250
        else:
            new_relpts += max(0, 150 - 25 * (len(w) - 7))
        if end.bullseye_length == end.min_length:
            prev_relpts += 250
        else:
            prev_relpts += max(0, 150 - 25 * (end.bullseye_length - 7))
        if prev_relpts < new_relpts:
            end.bullseye_length = len(w)
            end.bullseye_relpts = new_relpts
        else:
            end.bullseye_relpts = prev_relpts
        if puzzle == "wdl":
            print(w, end.bullseye_length, "prev", prev_relpts, "new", new_relpts)


def main():
    root = Node()
    print("starting")
    for i, w in enumerate(wordlist):
        if i % 1000 == 0:
            print(i, len(wordlist))
        add(w, root)
    print("done words")
    # root.print()
    puzzles_3, puzzles_4 = [], []
    for puzzle, bullseye_length in root.get_all(15, 3):
        [puzzles_3, puzzles_4][len(puzzle) == 4].append((puzzle, bullseye_length))
    with open("valid_puzzles_3.txt", 'w') as f:
        for puzzle, bullseye_length in puzzles_3:
            f.write(f"{puzzle},{bullseye_length}\n")
    with open("valid_puzzles_4.txt", 'w') as f:
        for puzzle, bullseye_length in puzzles_4:
            f.write(f"{puzzle},{bullseye_length}\n")


if __name__ == '__main__':
    main()
