from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    grid = [list(map(int,list(d.strip()))) for d in data]
    starts = get_start_positions(grid)

    return sum([len(heads_reachable(start,grid).keys()) for start in starts])


def part2(data: list[str]):
    grid = [list(map(int,list(d.strip()))) for d in data]
    starts = get_start_positions(grid)

    return sum([sum(heads_reachable(start, grid).values()) for start in starts])


def get_start_positions(grid: list[list[int]]) -> list[(int,int)]:
    result = []
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j] == 0:
                result.append((i, j))
    return result


def heads_reachable(start_loc: (int,int), grid: list[list[int]]) -> dict[int, int]:
    level = grid[start_loc[0]][start_loc[1]]

    current_locations = {start_loc:1}
    while level < 9:
        next_levels = dict()
        for loc in current_locations.keys():
            path_count = current_locations[loc]
            for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new = (loc[0]+delta[0], loc[1]+delta[1])
                if 0 <= new[0] < len(grid) and 0 <= new[1] < len(grid[0]) and grid[new[0]][new[1]] == level + 1:
                    next_levels[new] = next_levels.setdefault(new, 0) + path_count
        current_locations = next_levels
        level += 1
    return current_locations


ex = AdventOfCode(10)
ex.executeTest(part1, 36)
ex.executeTest(part2, 81)

ex.execute(part1, part2)
