from AdventOfCode import AdventOfCode

NUMPAD = {'7': (0,0), '8': (1,0), '9': (2,0), '4': (0,1), '5': (1,1), '6': (2,1), '1': (0,2), '2': (1,2), '3': (2,2), '0': (1,3), 'A': (2,3), ' ' : (0, 3)}
INV_NUMPAD = {v: k for k, v in NUMPAD.items()}

KEYPAD = {'<': (0, 1), '>': (2, 1), '^': (1, 0), 'v': (1, 1), 'A': (2, 0),  ' ': (0, 0)}
INV_KEYPAD = {v: k for k, v in KEYPAD.items()}

MOVES = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1),}
INV_MOVES = {v: k for k, v in MOVES.items()}

CACHE: dict[(str, str, int), int] = {}


def part1(data: list[str]):
    codes = read_codes(data)
    res = 0
    keys = get_key_expands()
    for code in codes:
        sequences = set(push_keypad('A', code, NUMPAD, INV_NUMPAD))
        res += min([get_min_key_size('A', seq, keys,2) for seq in sequences]) * int(code[:-1])
    return res


def part2(data: list[str]):
    codes = read_codes(data)
    res = 0
    keys = get_key_expands()
    for code in codes:
        sequences = set(push_keypad('A', code, NUMPAD, INV_NUMPAD))
        res += min([get_min_key_size('A', seq, keys,25) for seq in sequences]) * int(code[:-1])
    return res


def push_keypad(init: str, code: str, pad: dict[str, (int, int)],inv_pad: dict[(int,int),str]) -> set[str]:
    loc = pad[init]
    result = [""]
    for key in code:
        next_loc = pad[key]
        diff = (next_loc[0]-loc[0], next_loc[1]-loc[1])
        horizontal = ("<" if diff[0] < 0 else ">") * abs(diff[0])
        vertical = ("^" if diff[1] < 0 else "v") * abs(diff[1])
        new_result = set([])
        for res in result:
            if len(horizontal) > 0 and len(vertical) > 0 and  inv_pad[(next_loc[0], loc[1])] != ' ':
                new_result.add(res + horizontal + vertical + "A")
            if inv_pad[(loc[0],next_loc[1])] != ' ':
                new_result.add(res + vertical + horizontal + "A")
        result = list(new_result)
        loc = next_loc

    return set(result)


def get_key_expands() -> dict[(str, str), set[str]]:
    result = {}
    keys = set(KEYPAD.keys())
    keys.remove(' ')
    for x in keys:
        for y in keys:
            result[(x,y)] = push_keypad(x, y, KEYPAD, INV_KEYPAD)
    return result


def get_min_key_size(init: str, key: str, key_expands: dict[(str, str), set[str]], depth) -> int:
    if depth == 0:
        return len(key)
    if CACHE.get((init,key,depth)) is not None:
        return CACHE.get((init, key, depth))

    code = init+key
    prefix = ""
    for i in range(0, len(code)-1):
        next_expands = key_expands[code[i], code[i+1]]
        if len(next_expands) == 1:
            prefix += list(next_expands)[0]
        else:
            len_part_1 = min({get_min_key_size('A',prefix+n,key_expands, depth-1) for n in next_expands})
            if i < len(code) - 2:
                len_part_2 = get_min_key_size(code[i+1], code[i+2:], key_expands, depth)
                CACHE[(init, key, depth)] = len_part_1 + len_part_2
                return len_part_1 + len_part_2
            else:
                CACHE[(init, key, depth)] = len_part_1
                return len_part_1
    return get_min_key_size('A',prefix, key_expands, depth - 1)


def read_codes(data: list[str]) -> list[str]:
    return [line.strip() for line in data]


ex = AdventOfCode(21)
ex.executeTest(part1, 126384)

ex.execute(part1, part2)
