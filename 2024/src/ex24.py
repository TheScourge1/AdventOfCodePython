from AdventOfCode import AdventOfCode
from enum import Enum


class Cmd(Enum):
    AND = lambda a, b: 1 if a + b == 2 else 0
    OR = lambda a, b: 1 if a + b > 0 else 0
    XOR = lambda a, b: 1 if a + b == 1 else 0


Cmd_map = {"AND": Cmd.AND, "OR": Cmd.OR, "XOR": Cmd.XOR}
Inv_map = {Cmd_map[c]: c for c in Cmd_map.keys()}


def part1(data: list[str]):
    vals, fs = read_data(data)
    zkeys = sorted([v for v in fs.keys() if v[0] == 'z'], reverse=True)
    return int(calc(vals, fs, zkeys), 2)


def part2(data: list[str]):
    vals, fs = read_data(data)
    zkeys = sorted([v for v in fs.keys() if v[0] == 'z'])
    swaps = []
    for i in range(2, len(zkeys)-1):
        z_val = "z"+str(i).zfill(2)

        swap = check_root(fs, z_val)
        if swap:
            print(f"SWAP FOUND: {swap}")
            swaps += swap
            swap_vals(swap[0], swap[1], fs)
    return ",".join(sorted(swaps))


def check_root(fs: dict[str, tuple[str, Cmd, str]], zval:str) -> tuple[str, str]:
    root = fs[zval]
    xVal = 'x'+zval[1:]
    xor_significant_bit = [k for k, v in fs.items() if v[1] == Cmd.XOR and (v[0] == xVal or v[2] == xVal)][0]
    if root[1] != Cmd.XOR:
        new_vals = [k for k, v in fs.items() if v[1] == Cmd.XOR and (v[0] == xor_significant_bit or v[2] == xor_significant_bit)]
        if len(new_vals) != 1:
            raise Exception(f"invalid swaps found for {zval} -> {new_vals}")
        else:
            return zval, new_vals[0]
    elif root[0] != xor_significant_bit and root[2] != xor_significant_bit:
        root1 = root[0] if fs[root[0]][0] == xVal or fs[root[0]][2] == xVal else root[2]
        return xor_significant_bit, root1

    return None


def swap_vals(val1: str, val2: str, fs: dict[str, tuple[str, Cmd, str]]):
    temp = fs[val1]
    fs[val1] = fs[val2]
    fs[val2] = temp


def calc_i(x: int, y: int, fs: dict[str, tuple[str, Cmd, str]]):
    zkeys = sorted([s for s in fs.keys() if s[0] == 'z'])
    vals = encode_values(x, y, len(zkeys))
    return calc(vals, fs, zkeys)


def calc(vals, fs: dict[str, tuple[str, Cmd, str]], zkeys: list[str]):
    to_calculate = set(fs.keys())
    calculated = vals.copy()
    while to_calculate:
        remaining = set()
        for key in to_calculate:
            f = fs[key]
            if f[0] in calculated.keys() and f[2] in calculated.keys():
                calculated[key] = f[1](calculated[f[0]], calculated[f[2]])
            else:
                remaining.add(key)
        to_calculate = remaining
    return "".join([str(calculated[v]) for v in zkeys])


def encode_values(x: int, y: int, size: int) -> dict[str, int]:
    res = {}
    for i in range(size):
        ind = str(i).zfill(2)
        res["x"+ind] = x % 2
        res["y"+ind] = y % 2
        x = x // 2
        y = y // 2
    return res


def read_data(data: list[str]) -> tuple[dict[str, int], dict[str, tuple[str, Cmd, str]]]:
    res1, res2 = {}, {}
    for d in [d.strip() for d in data]:
        if ':' in d:
            line = d.split(": ")
            res1[line[0]] = int(line[1])
        elif " -> " in d:
            line = d.split(" -> ")
            command = line[0].split(" ")
            res2[line[1]] = command[0], Cmd_map[command[1]], command[2]
    return res1, res2


def print_path(key: str, grid: dict[str, tuple[str, Cmd, str]], depth: int, print_depth: int):
    if depth > print_depth:
        return
    if key.startswith('x') or key.startswith('y'):
        print('\t'*depth + key)
    else:
        command = grid[key]
        print_path(command[0], grid, depth+1,print_depth)
        print('\t'*depth + f"{key}={Inv_map[command[1]]}")
        print_path(command[2],grid, depth+1, print_depth)
    return


ex = AdventOfCode(24)
ex.executeTest(part1, 2024)

ex.execute(part1, part2)
