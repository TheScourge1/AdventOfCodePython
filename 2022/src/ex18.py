from AdventOfCode import AdventOfCode


def part1(data: list[str]) -> str:
    cubes = read_cubes(data)
    result = get_adjacent_surface_count(cubes)

    return str(result)


def part2(data: list[str]) -> str:
    cubes = read_cubes(data)
    air_pockets = get_airpockets(cubes)
    cube_surfaces = get_adjacent_surface_count(cubes)
    air_pockets_surfaces = get_adjacent_surface_count(air_pockets)

    return str(cube_surfaces-air_pockets_surfaces)


def get_airpockets(cubes: set[tuple[int, int, int]]) -> set[tuple[int, int, int]]:
    a, b, c = zip(*cubes)
    limit = (max(a)+1, max(b)+1, max(c)+1)
    open_air_list = set()

    for x in [-1,limit[0]]:
        for y in range(-1,limit[1]):
            for z in range(-1,limit[2]):
                if not (x,y,z) in cubes:
                    open_air_list.add((x,y,z))
    for x in [-1,limit[0]]:
        for z in range(-1,limit[2]):
            for y in range(-1,limit[1]):
                if not (x,y,z) in cubes:
                    open_air_list.add((x,y,z))
    for z in [-1,limit[2]]:
        for y in range(-1,limit[1]):
            for x in range(-1,limit[0]):
                if not (x,y,z) in cubes:
                    open_air_list.add((x,y,z))

    to_visit = open_air_list.copy()
    while len(to_visit) > 0:
        air_node = to_visit.pop()
        adjacent_nodes = get_adjacent_cubes(air_node)
        for node in adjacent_nodes:
            if not(node[0] < 0 or node[0] > limit[0] or
                   node[1] < 0 or node[1] > limit[1] or
                   node[2] < 0 or node[2] > limit[2] or
                   node in open_air_list or node in cubes):
                open_air_list.add(node)
                to_visit.add(node)

    result = set()
    for x in range(0, limit[0]):
        for y in range(0, limit[1]):
            for z in range(0, limit[2]):
                if (x, y, z) not in cubes and (x, y, z) not in open_air_list:
                    result.add((x, y, z))

    return result


def get_adjacent_surface_count(cubes: set[tuple[int, int, int]]) -> int:
    result = 0
    for cube in cubes:
        adjacent_count = 0
        adjacent_cubes = get_adjacent_cubes(cube)
        for adjacent_cube in adjacent_cubes:
            adjacent_count += 1 if adjacent_cube in cubes else 0
        result += 6 - adjacent_count

    return result


def get_adjacent_cubes(cube: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    adjacent_cubes = {(0, 0, 1), (0, 1, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)}
    result = []
    for delta in adjacent_cubes:
        next_cube = tuple(x+y for x,y in zip(cube,delta))
        result.append(next_cube)
    return result


def read_cubes(data: list[str]) -> set(tuple[int, int, int]):
    result = set()
    for line in data:
        cube = line.strip().split(",")
        result.add((int(cube[0]), int(cube[1]), int(cube[2])))
    return result


ex18 = AdventOfCode(18)
ex18.executeTest(part1, "64")
ex18.executeTest(part2, "58")

ex18.execute(part1, part2)