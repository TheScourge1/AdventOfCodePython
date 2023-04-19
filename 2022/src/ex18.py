from AdventOfCode import AdventOfCode




def part1(data: list[str]) -> str:
    cubes = read_cubes(data)
    adjacent_cubes = {(0,0,1),(0,1,0),(1,0,0),(-1,0,0),(0,-1,0),(0,0,-1)}

    result = 0
    for cube in cubes:
        adjacent_count = 0
        for adjacent_index in adjacent_cubes:
            adjacent_tuple = tuple(x+y for x,y in zip(cube,adjacent_index))
            adjacent_count += 1 if adjacent_tuple in cubes else 0
        result += 6 - adjacent_count

    return str(result)


def part2(data: list[str]) -> str:
    pass


def read_cubes(data: list[str]) -> set(tuple[int,int,int]):
    result = set()
    for line in data:
        cube = line.strip().split(",")
        result.add((int(cube[0]), int(cube[1]), int(cube[2])))
    return result


ex18 = AdventOfCode(18)
ex18.executeTest(part1, "64")
ex18.executeTest(part1, "58")

ex18.execute(part1, part2)
