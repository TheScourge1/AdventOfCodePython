from AdventOfCode import AdventOfCode
from enum import Enum

class Dir(Enum):
    N = (-1,0)
    S = (1,0)
    W = (0,-1)
    E = (0,1)

DIRECTIONS = [Dir.N,Dir.E,Dir.S,Dir.W]

def part1(data: list[str]):
    grid = read_data(data)
    coord = get_start(grid)
    while not coord is None:
        grid[coord[0]][coord[1]] = "X"
        coord = get_next_coord(coord,grid)

    return sum([1 for line in grid for c in line if c == "X"])

def part2(data: list[str]):
    grid = read_data(data)
    start = get_start(grid)
    c = start

    while not c is None:
        grid[c[0]][c[1]] = "X"
        c = get_next_coord(c,grid)

    result = 0
    for i in range(0,len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == "X":
                grid[i][j] = "#"
                if contains_loop(grid, start):
                    result += 1
                grid[i][j] = "X"
    return result


def read_data(data: list[str]) -> list[list[str]]:
    result = []
    for line in data:
        result.append([c for c in line.strip()])
    return result


def get_start(grid: list[list[str]]) -> (int,int,Dir):
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j] == "^":
                return i, j, Dir.N
    raise "Missing start location"


def get_next_coord(coord:(int,int,Dir),grid: list[list[str]]) -> (int, int, Dir):
    nextc = (coord[0]+coord[2].value[0], coord[1]+coord[2].value[1], coord[2])
    if nextc[0] < 0 or nextc[1] < 0 or nextc[0] == len(grid) or nextc[1] == len(grid[0]):
        return None
    else:
        if grid[nextc[0]][nextc[1]] == "." or grid[nextc[0]][nextc[1]] == "X":
            return nextc
        elif grid[nextc[0]][nextc[1]] == "#":
            return coord[0],coord[1],DIRECTIONS[(DIRECTIONS.index(coord[2])+1) % 4]
        else:
            raise Exception(f"Unexpected grid value: {nextc} -> {grid[nextc[0]][nextc[1]]}")


def contains_loop(input_grid: list[list[str]],start:(int,int,Dir)) -> bool:
    visit_list = set()
    c = start
    while c is not None:
        if c in visit_list:
            return True
        visit_list.add(c)
        c = get_next_coord(c, input_grid)
    return False


def print_grid(grid: list[list[str]]):
    for line in grid:
        print("".join(line))


ex = AdventOfCode(6)

ex.executeTest(part1, 41)
ex.executeTest(part2, 6)

ex.execute(part1, part2)