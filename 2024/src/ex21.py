from AdventOfCode import AdventOfCode

NUMPAD = {'7': (0,0), '8': (1,0), '9': (2,0), '4': (0,1), '5': (1,1), '6': (2,1), '1': (0,2), '2': (1,2), '3': (2,2), '0': (1,3), 'A': (2,3), ' ' : (0, 3)}
INV_NUMPAD = {v: k for k, v in NUMPAD.items()}

KEYPAD = {'<': (0, 1), '>': (2, 1), '^': (1, 0), 'v': (1, 1), 'A': (2, 0),  ' ': (0, 0)}
INV_KEYPAD = {v: k for k, v in KEYPAD.items()}

MOVES = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1),}


def part1(data: list[str]):
    codes = read_codes(data)
    res = 0
    for code in codes:
        sequences = set(push_keypad(code, NUMPAD))

        for i in range(2):
            next_seq_list = [push_keypad(sequence, KEYPAD) for sequence in sequences]
            sequences = {seq for next_seq in next_seq_list for seq in next_seq}
            print(f'for code {code}: level {i} -> list size {len(sequences)}')
        min_lenght = min([len(seq) for seq in sequences])
        res += min_lenght * int(code[:-1])

    return res


def part2(data: list[str]):
    pass


def push_keypad(code: str, pad: dict[str, (int, int)]) -> set[str]:
    loc = pad['A']
    result = [""]
    for key in code:
        next_loc = pad[key]
        horizontal = "<" * (loc[0] - next_loc[0]) if loc[0] > next_loc[0] else ">" * (next_loc[0] - loc[0])
        vertical = "^" * (loc[1] - next_loc[1]) if loc[1] > next_loc[1] else "v" * (next_loc[1] - loc[1])
        new_result = set([])
        for res in result:
            new_result.add(res + horizontal + vertical + "A")
            new_result.add(res + vertical + horizontal + "A")
        result = list(new_result)
        loc = next_loc

    return {res for res in result if is_valid_keypad_sequence(res, pad)}


def is_valid_keypad_sequence(sequence: str, pad: dict[str, (int, int)]):
    loc = pad['A']
    res = loc
    for s in sequence:
        if s == 'A':
            move = (0, 0)
        else:
            move = MOVES[s]
        loc = (loc[0]+move[0], loc[1]+move[1])
        res += loc
        if loc not in NUMPAD.values():
            raise Exception("invalid move: "+s + " -> " + str(loc))
        elif pad[' '] == loc:
            return None
    return True


def read_codes(data: list[str]) -> list[str]:
    return [line.strip() for line in data]


ex = AdventOfCode(21)
ex.executeTest(part1, 126384)

ex.execute(part1, part2)
