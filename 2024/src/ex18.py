from AdventOfCode import AdventOfCode

NEIGHBOURS = [(-1,0),(1,0), (0,-1), (0,1)]


def part1(data: list[str]):
    bits = read_data(data)
    size = max([b[0] for b in bits])
    bit_cnt = 12 if size == 6 else 1024

    return find_exit(bits, bit_cnt,size)


def part2(data: list[str]):
    bits = read_data(data)
    size = max([b[0] for b in bits])
    bit_cnt = 12 if size == 6 else 1024

    while find_exit(bits, bit_cnt, size) > 0:
        bit_cnt += 1

    return data[bit_cnt-1].strip()


def find_exit(bit_list: list[(int, int)], bit_count, size) -> int:
    grid = [[-1] * (size + 1) for _ in range(size+1)]
    grid[0][0] = 0
    ind = 0

    bits = set(bit_list[:bit_count])
    frontier = [(0, 0)]

    while len(frontier) > 0:
        new_frontier = []
        ind += 1
        for loc in frontier:
            for v in NEIGHBOURS:
                n = (loc[0]+v[0], loc[1]+v[1])
                if 0 <= n[0] <= size and 0 <= n[1] <= size and n not in bits and grid[n[0]][n[1]] == -1:
                    if n == (size,size):
                        return ind
                    else:
                        grid[n[0]][n[1]] = ind
                        new_frontier.append(n)
        frontier = new_frontier
    return -1


def read_data(data: list[str]) -> list[(int, int)]:
    return list([tuple(map(int, line.strip().split(","))) for line in data])


def print_grid(grid: list[list[int]]):
    for line in grid:
        ln = "".join([str(i)+"\t" for i in line])
        print(ln)


ex = AdventOfCode(18)
ex.executeTest(part1, 22)
ex.executeTest(part2, "6,1")

ex.execute(part1, part2)
