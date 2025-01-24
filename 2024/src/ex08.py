from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    beacons = read_data(data)
    all_nodes = set()
    for b in beacons.values():
        node_list = get_nodes(b)
        all_nodes.update(node_list)

    valid_nodes = [n for n in all_nodes if 0 <= n[0] < len(data) and 0 <= n[1] < len(data)]
    return len(valid_nodes)

def part2(data: list[str]):
    pass


def read_data(data: list[str]) -> dict[str,list[(int,int)]]:
    result = {}
    for i in range(0, len(data)):
        line = list(data[i].strip())
        for j in range(0,len(line)):
            token = line[j]
            if token != ".":
                result.setdefault(token,[]).append((j,i))

    return result


def get_nodes(antena_lst: list[(int,int)]) -> list[(int,int)]:
    temp_list = antena_lst.copy()
    result = []
    while len(temp_list) > 0:
        a = temp_list.pop()
        for a2 in temp_list:
            dist = (a2[0]-a[0], a2[1]-a[1])
            result.append((a2[0]+dist[0],(a2[1]+dist[1])))
            result.append((a[0]-dist[0],(a[1]-dist[1])))

    return result

ex = AdventOfCode(8)
ex.executeTest(part1,14)
#ex.executeTest(part1,)

ex.execute(part1,part2)