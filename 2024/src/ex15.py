from AdventOfCode import AdventOfCode
import re

MOVES = {"<": (0, -1), ">": (0, 1),"^": (-1, 0), "v": (1, 0)}


def part1(data: list[str]):
    grid, commands = read_data(data)
    start = find_start(grid)
    location = start
    #print_grid(grid)
    #print("")
    for move in commands:
        location = execute_move(grid, location, move)
        #print(f"move: {move}")
        #print_grid(grid)
        #print("")
    return get_gps_sum(grid)


def part2(data: list[str]):
    pass


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


def find_start(grid: list[list[str]]) -> (int, int):
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j] == "@":
                return i, j
    return None


def execute_move(grid: list[list[str]], start: (int, int), move: str) -> (int, int):
    v = MOVES[move]
    dist = 0
    p = start
    while grid[p[0]][p[1]] not in {"#", "."}:
        dist += 1
        p = p[0]+v[0], p[1]+v[1]
    if grid[p[0]][p[1]] == ".":
        while p != start:
            new = p[0]-v[0], p[1]-v[1]
            grid[p[0]][p[1]] = grid[new[0]][new[1]]
            p = new
        grid[p[0]][p[1]] = "."
        return p[0]+v[0], p[1]+v[1]
    else:
        return start


def get_gps_sum(grid: list[list[str]]) -> int:
    result = 0
    for j in range(0, len(grid)):
        for i in range(0, len(grid[0])):
            if grid[j][i] == "O":
                result += 100*j + i
    return result


def print_grid(grid: list[list[str]]):
    for row in grid:
        print(''.join(row))


ex = AdventOfCode(15)
ex.executeTest(part1, 10092)

ex.execute(part1, part2)