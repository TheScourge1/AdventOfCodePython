from AdventOfCode import AdventOfCode
from dataclasses import dataclass

@dataclass
class Region:
    id: str
    coords: set[(int,int)]


@dataclass(frozen=True)
class Edge:
    p1: (int, int)
    p2: (int, int)

def part1(data: list[str]):
    grid = [list(d.strip()) for d in data]
    regions = get_all_regions(grid)
    return sum([len(r.coords) * len(get_edges(r)) for r in regions])


def part2(data: list[str]):
    grid = [list(d.strip()) for d in data]
    regions = get_all_regions(grid)

    return sum([len(r.coords) * len(get_fences(r)) for r in regions])

def get_all_regions(grid: list[list[str]]) -> list[Region]:
    regions = []
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            allready_visited = False
            for region in regions:
                if (i,j) in region.coords:
                    allready_visited = True
                    break
            if not allready_visited:
                regions.append(get_region(grid,(i,j)))
    return regions


def get_region(grid: list[list[str]], start: (int, int)) -> Region:
    result = Region(grid[start[0]][start[1]], set())
    to_process = {start}
    while len(to_process) > 0:
        loc = to_process.pop()
        if grid[loc[0]][loc[1]] == result.id and loc not in result.coords:
            result.coords.add(loc)
            for delta in {(-1, 0), (1, 0), (0, -1), (0, 1)}:
                neighbour = (loc[0]+delta[0], loc[1]+delta[1])
                if 0 <= neighbour[0] < len(grid) and 0 <= neighbour[1] < len(grid[0]):
                    to_process.add(neighbour)

    return result


def get_edges(region:Region) -> list[Edge]:
    edge_list = []
    for c in region.coords:
        edge_list.append(Edge((c[0], c[1]), (c[0], c[1] + 1)))
        edge_list.append(Edge((c[0], c[1]), (c[0] + 1, c[1])))
        edge_list.append(Edge((c[0], c[1] + 1), (c[0] + 1, c[1] + 1)))
        edge_list.append(Edge((c[0] + 1, c[1]), (c[0] + 1, c[1] + 1)))
    external_edge_list = [e for e in edge_list if edge_list.count(e) == 1]
    return external_edge_list


def get_corner_points(region: Region) -> set[(int,int)]:
    edge_list = get_edges(region)
    corner_points = set()
    for edge1 in edge_list:
        for edge2 in edge_list:
            if edge1 != edge2 and is_corner(edge1, edge2):
                corner_points.add(get_corner_point(edge1, edge2))

    return corner_points


def get_fences(region: Region) -> list[list[Edge]]:
    edges = set(get_edges(region))
    corners = get_corner_points(region)
    result = []
    while len(edges) > 0:
        end_point = None
        fence = []
        for edge in edges:
            if edge.p1 in corners:
                end_point = edge.p2
            elif edge.p2 in corners:
                end_point = edge.p1

            if end_point is not None:
                fence = [edge]
                break

        while end_point not in corners:
            next_edge = [e for e in edges if (e.p1 == end_point or e.p2 == end_point) and e != fence[len(fence)-1]][0]
            fence.append(next_edge)
            if next_edge.p1 == end_point:
                end_point = next_edge.p2
            else:
                end_point = next_edge.p1

        result.append(fence)
        edges -= set(fence)


    return result


def is_corner(edge1: Edge,edge2: Edge) -> bool:
    if edge1.p1 in [edge2.p1, edge2.p2] or edge1.p2 in [edge2.p1, edge2.p2]:
        v1 = (edge1.p2[0]-edge1.p1[0], edge1.p2[1]-edge1.p1[1])
        v2 = (edge2.p2[0]-edge2.p1[0], edge2.p2[1]-edge2.p1[1])
        return (v1[0]*v2[0] + v1[1]*v2[1]) == 0
    return False


def get_corner_point(edge1: Edge,edge2: Edge) -> (int, int):
    points = [edge1.p1, edge1.p2, edge2.p1, edge2.p2]
    for p in points:
        if points.count(p) > 1:
            return p
    raise Exception("Expected mutual point in corner")


ex = AdventOfCode(12)
ex.executeTest(part1, 1930)
ex.executeTest(part2, 1206)
ex.executeTest(part2, 2*4*4+12*28,2)

ex.execute(part1, part2)
