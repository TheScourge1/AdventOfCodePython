from AdventOfCode import AdventOfCode
import re

MOVES = {"<": (0, -1), ">": (0, 1),"^": (-1, 0), "v": (1, 0)}


def part1(data: list[str]):
    grid, commands = read_data(data)
    location = find_start(grid)
    for move in commands:
        location = execute_move(grid, location, move)
    return get_gps_sum(grid)


def part2(data: list[str]):
    grid, commands = read_data(data)
    grid = duplicate_grid(grid)
    location = find_start(grid)
    for move in commands:
        location = execute_move(grid, location, move)
    return get_gps_sum(grid)


def read_data(data: list[str]) -> (list[list[str]], str):
    grid = []
    commands = ""
    command_pattern = r"([v|<|^|>|#])+"
    for line in data:
        if line.count("#") > 0:
            grid.append(list(line.strip()[0:len(line)-1]))
        elif re.match(command_pattern, line) is not None:
            commands += line.strip()
    return grid, commands


def duplicate_grid(grid: list[list[str]]) -> list[list[str]]:
    res = [list("#"*(len(grid[0])*2))]
    mapping = {'#': ['#', '#'], '.': ['.', '.'], '@': ['@', '.'], 'O': ['[', ']']}

    for i in range(1, len(grid)-1):
        line = []
        for j in range(0, len(grid[0])):
            line += mapping[grid[i][j]]
        res.append(line)
    res.append(list("#"*(len(grid[0])*2)))
    return res


def find_start(grid: list[list[str]]) -> (int, int):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "@":
                return i, j
    return None


def execute_move(grid: list[list[str]], start: (int, int), move: str) -> (int, int):
    v = MOVES[move]
    if v[0] == 0:
        return do_horizontal_move(grid, start, v[1])
    else:
        return do_vertical_move(grid, start, v[0])


def do_horizontal_move(grid: list[list[str]], start: (int, int), v: int) -> (int,int):
    y = start[0]
    x = start[1]
    while grid[y][x] not in {"#", "."}:
        x += v
    if grid[y][x] == ".":
        while x != start[1]:
            new_x = x - v
            grid[y][x] = grid[y][new_x]
            x = new_x
        grid[y][x] = "."
        return y, x+v
    else:
        return start


def do_vertical_move(grid: list[list[str]], start: (int, int), v: int) -> (int, int):
    x = start[1]
    y = start[0]

    if grid[y+v][x] == "#" or not can_move(grid, (y+v, x), v):
        return start
    elif grid[y+v][x] == "[" or grid[y+v][x] == "O":
        move_box(grid,(y+v, x), v)
    elif grid[y+v][x] == "]":
        move_box(grid,(y+v,x-1), v)
    elif grid[y+v][x] != ".":
        raise Exception("Unexpected next value: "+grid[y+v][x])

    grid[y+v][x] = "@"
    grid[y][x] = "."
    return y+v, x


def move_box(grid: list[list[str]], start: (int, int), v: int):
    y = start[0]
    x = start[1]
    if grid[y][x] not in {"[", "O", "."}:
        raise Exception("Unexpected char found: " + grid[y][x])
    if grid[y+v][x] == "#":
        raise Exception("Unexpected block found: " + str((y+v,x)))
    if grid[y+v][x] == "[" or grid[y+v][x] == "O":
        move_box(grid, (y+v, x), v)
    if grid[y+v][x] == "]":
        move_box(grid, (y+v, x - 1), v)
    if grid[y+v][x+1] == "[":
        move_box(grid,(y+v, x+1), v)

    if grid[y][x] == "[":
        grid[y+v][x+1] = grid[y][x+1]
        grid[y][x+1] = "."
    grid[y+v][x] = grid[y][x]
    grid[y][x] = "."

    return


def can_move(grid: list[list[str]], start: (int, int), v: int) -> bool:
    y = start[0]
    x = start[1]
    if grid[y][x] == ".":
        return True
    elif grid[y][x] == "#":
        return False
    elif grid[y][x] == "[":
        return can_move(grid,(y+v, x), v) and can_move(grid,(y+v, x+1), v)
    elif grid[y][x] == "]":
        return can_move(grid,(y+v, x), v) and can_move(grid,(y+v, x-1), v)
    elif grid[y][x] == "O":
        return can_move(grid,(y+v, x), v)
    else:
        raise Exception("unexpected char found : "+grid[y][x])


def get_gps_sum(grid: list[list[str]]) -> int:
    result = 0
    for j in range(0, len(grid)):
        for i in range(0, len(grid[0])):
            if grid[j][i] == "O" or grid[j][i] == "[":
                result += 100*j + i
    return result


def print_grid(grid: list[list[str]]):
    for row in grid:
        print(''.join(row))


ex = AdventOfCode(15)
ex.executeTest(part1, 10092)
ex.executeTest(part2, 9021)

ex.execute(part1, part2)