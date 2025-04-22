from AdventOfCode import AdventOfCode

DIRS = {(-1, 0), (1, 0), (0, 1), (0, -1)}


def part1(data: list[str]):
    grid = read_data(data)
    number_grid(grid)
    count_over = 10 if len(grid) < 20 else 100

    result = 0
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[0])-1):
            if grid[i][j] != "#":
                for d in DIRS:
                    v = (i+2*d[0],j+2*d[1])
                    if 0 < v[0] < len(grid) and 0 < v[1] < len(grid[0]) and grid[v[0]][v[1]] != "#":
                        diff = abs(int(grid[i][j]) - int(grid[v[0]][v[1]]))
                        if diff-2 >= count_over:
                            result += 1
    return int(result / 2)  # counting all moves double


def part2(data: list[str]):
    grid = read_data(data)
    number_grid(grid)
    count_over = 50 if len(grid) < 20 else 100
    result = set([])

    path = {}
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[0])-1):
            if grid[i][j] != "#":
                path[(i, j)] = int(grid[i][j])

    locations = list(path.keys())
    for i in range(0,len(locations)):
        for j in range(i+1, len(locations)):
            p1, p2 = locations[i], locations[j]

            dist = abs(p1[0]-p2[0])+abs(p1[1]-p2[1])
            diff = abs(path[p1] - path[p2])
            if dist <= 20 and diff - dist >= count_over:
                result.add((p1, p2))

    return len(result)


def read_data(data: list[str]) -> list[list[str]]:
    return [list(line.strip()) for line in data]


def number_grid(grid: list[list[str]]):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                grid[i][j] = "0"
                cnt = 0
                v = (i,j)
                while True:
                    moved = False
                    for d in DIRS:
                        if grid[v[0]+d[0]][v[1]+d[1]] in {".", "E"}:
                            cnt += 1
                            v = (v[0] + d[0], v[1] + d[1])
                            grid[v[0]][v[1]] = str(cnt)
                            moved = True
                    if not moved:
                        return


def print_grid(grid: list[list[str]]):
    for line in grid:
        print("".join([s+"\t" for s in line]))


ex = AdventOfCode(20)
ex.executeTest(part1, 10)
ex.executeTest(part2, 285)

ex.execute(part1, part2)
