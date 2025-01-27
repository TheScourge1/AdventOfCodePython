from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    beacons = read_data(data)
    all_nodes = set()
    for b in beacons.values():
        node_list = get_nodes(b,len(data),True)
        all_nodes.update(node_list)

    return len(all_nodes)


def part2(data: list[str]):
    beacons = read_data(data)
    all_nodes = set()
    for b in beacons.values():
        node_list = get_nodes(b, len(data), False)
        all_nodes.update(node_list)

    return len(all_nodes)


def read_data(data: list[str]) -> dict[str,list[(int,int)]]:
    result = {}
    for i in range(0, len(data)):
        line = list(data[i].strip())
        for j in range(0,len(line)):
            token = line[j]
            if token != ".":
                result.setdefault(token,[]).append((j,i))

    return result


def get_nodes(antena_lst: list[(int, int)], grid_size: int, only_freq_1:bool) -> list[(int, int)]:
    temp_list = antena_lst.copy()
    result = []
    while len(temp_list) > 0:
        a = temp_list.pop()
        for a2 in temp_list:
            dist = (a2[0]-a[0], a2[1]-a[1])
            n = 1 if only_freq_1 else 0
            while True:
                result_size = len(result)
                n1 = (a2[0]+n*dist[0], (a2[1]+n*dist[1]))
                n2 = (a[0]-n*dist[0], (a[1]-n*dist[1]))
                if 0 <= n1[0] < grid_size and 0 <= n1[1] < grid_size:
                    result.append(n1)
                if 0 <= n2[0] < grid_size and 0 <= n2[1] < grid_size:
                    result.append(n2)
                if len(result) == result_size or only_freq_1:
                    break
                n += 1

    return result

ex = AdventOfCode(8)
ex.executeTest(part1, 14)
ex.executeTest(part2, 34)

ex.execute(part1,part2)