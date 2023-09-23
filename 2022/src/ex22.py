from AdventOfCode import AdventOfCode
from dataclasses import dataclass
import re, math


@dataclass
class Location:
    x: int = 0
    y: int = 0
    direction: int = 0
    face_id = 1

    def __init__(self, x, y, direction, face_id = 1):
        self.x = x
        self.y = y
        self.direction = direction
        self.face_id = face_id

    def __repr__(self):
        return f"({self.x},{self.y},{self.direction},f{self.face_id})"

    def get_move_vector(self) -> (x,y):
        match self.direction:
            case 0:
                return -1, 0
            case 90:
                return 0, 1
            case 180:
                return 1, 0
            case 270:
                return 0, -1
            case _:
                raise Exception("Unknown direction: " + str(self.direction))


    def turn_R(self):
        return Location(self.x,self.y,(self.direction+90) % 360, self.face_id)

    def turn_L(self):
        return Location(self.x,self.y,(self.direction+270) % 360, self.face_id)

    def get_value(self):
        return 1000 * (self.x + 1) + 4 * (self.y + 1) + int((self.direction + 270) % 360 / 90)


@dataclass
class Edge:
    p1: tuple[int, int] = (0, 0)
    p2: tuple[int, int] = (0, 0)

    def __init__(self, p1: tuple[int, int], p2: tuple[int, int]):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"{self.p1}-{self.p2}"

    def __hash__(self):
        return hash(self.p1)+hash(self.p2)

    def __eq__(self,other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def vec(self) -> tuple[int,int]:
        return (self.p2[0] - self.p1[0], self.p2[1] - self.p1[1])

    def add(self, vector: tuple[int,int]) -> 'Edge':
        return Edge((self.p1[0]+vector[0], self.p1[1]+vector[1]), (self.p2[0]+vector[0], self.p2[1]+vector[1]))


@dataclass
class Face:
    id: int
    grid_location: (int, int)
    size: int

    def __init__(self, id: int, location: (int, int), size):
        self.id = id
        self.grid_location = location
        self.size = size

    def __repr__(self):
        return f"{self.id} {self.grid_location}"

    def get_edges(self) -> list[Edge]:
        result = list()
        x0 = self.grid_location[1]
        y0 = self.grid_location[0]
        end = self.size - 1
        result.append(Edge((x0, y0), (x0 + end, y0)))
        result.append(Edge((x0, y0), (x0, y0 + end)))
        result.append(Edge((x0 + end, y0), (x0 + end, y0 + end)))
        result.append(Edge((x0, y0 + end), (x0 + end, y0 + end)))
        return result

    def step_out_direction(self, edge: Edge) -> int :
        degrees = (270,0,180,90)
        ind = self.get_edges().index(edge)
        return degrees[ind]


def part1(data: list[str]) -> str:
    data_grid = read_datagrid(data)
    password = read_password(data)
    location = Location(0, data_grid[0].index("."), 90)
    for s in password:
        location = walk(data_grid, location, s, False,list(),"")

    return str(location.get_value())


def part2(data: list[str]) -> str:
    data_grid = read_datagrid(data)
    password = read_password(data)

    cube_size: int = get_cube_size(data_grid)
    faces: list[Face] = get_faces(data_grid, cube_size)
    edges_to_map: dict[Edge, Face] = get_edges(faces)
    adjacent_edges,remaining_edges = extract_adjacent_edges(edges_to_map)

    inner_corners = get_inner_corners(set(edges_to_map.keys()))
    adjacent_edges1 = extract_edges_at_distance(inner_corners, remaining_edges, remaining_edges,1)

    for k in adjacent_edges.keys():
        adjacent_edges[k].update(adjacent_edges1[k])

    location = Location(0, 0, 90)
    for s in password:
        location = walk(data_grid, location, s, True, adjacent_edges,faces)

    print_datagrid(data_grid)

    cube_location = cube_to_grid_location(data_grid, location,faces)
    print(f"final location: {location} -> in grid: {cube_location}")

    return str(cube_location.get_value())


def walk(data_grid: list[list[str]], location: Location, command: str, is_cube: bool,adjacent_grids,faces: list[Face]) -> Location:
    match command:
        case "R":
            return location.turn_R()
        case "L":
            return location.turn_L()
        case _:
            moves = int(command)
            if is_cube:
                return move_forward_cube(data_grid,location,moves,adjacent_grids,faces)
            else:
                return move_forward(data_grid, location, moves)


def move_forward(data_grid: list[list[str]], location: Location, moves: int) -> Location:
    m = 0
    x = location.x
    y = location.y
    x_dir, y_dir = location.get_move_vector()
    result = location
    while m < moves:
        x1 = (x + x_dir) % len(data_grid)
        y1 = (y + y_dir) % len(data_grid[0])
        match data_grid[x1][y1]:
            case " ":
                pass
            case ".":
                result = Location(x1, y1,location.direction)
                m += 1
            case "#":
                break
            case _:
                raise Exception("Unknown grid item: " + data_grid[x + x_dir][y + y_dir])
        x, y = x1, y1

    return result


def get_cube_size(data_grid: list[list[str]]) -> int:
    data_elements = len([s for line in data_grid for s in line if s != " "])
    return int(math.sqrt(data_elements/ 6))


def get_faces(data_grid: list[list[str]], cube_size) -> list[Face]:
    result = list()
    face_id = 1
    for y in range(0, len(data_grid), cube_size):
        for x in range(0, len(data_grid[0]), cube_size):
            if data_grid[y][x] != " ":
                result.append(Face(face_id, (x, y),cube_size))
                face_id += 1
    return result


def get_edges(faces: list[Face]) -> dict[Edge, Face]:
    result:  dict[Edge, Face] = {}
    for face in faces:
        for edge in face.get_edges():
            result[edge] = face
    return result


def extract_adjacent_edges(edges: dict[Edge, Face]) -> (dict[tuple[int, int], dict[int, tuple[int, int, str]]], dict[Edge, Face]):
    vectors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    degrees = [0, 180, 270, 90]
    result:  dict[int, dict[int, tuple[int, int, str]]] = {}
    mapped_edges = {}
    for degree in degrees:
        result[degree] = {}
    for edge in edges.keys():
        for vector in vectors:
            new_edge = edge.add(vector)
            if new_edge in edges.keys():
                current_face = edges[edge]
                new_face = edges[new_edge]
                result[degrees[vectors.index(vector)]][current_face.id] = (new_face.id, 0, 'N')
                mapped_edges[edge] = edges[edge]

    return result, {k:v for k,v in edges.items() if k not in mapped_edges.keys()}


def get_inner_corners(edges: set[Edge]) -> list[tuple[int,int]]:
    vectors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = list()
    pointset = set([e.p1 for e in edges] + [e.p2 for e in edges])
    for p in pointset:
        surrounding_points = [(p[0]+v[0], p[1]+v[1]) for v in vectors]
        if len(pointset.intersection(surrounding_points)) == 2:
            result.append(p)
    return result


def extract_edges_at_distance(inner_corners: list[tuple[int,int]], all_edges:  dict[Edge, Face],
                              remaining_edges: dict[Edge, Face], distance:int) -> (dict[int, dict[int, tuple[int, int, str]]], dict[Edge, Face]):
    #print(f"distance {distance} - remaining_edges {remaining_edges}")
    vectors = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
    degrees = [0, 180, 270, 90]
    result = {}
    new_remaining_edges = remaining_edges.copy()
    for degree in degrees[0:4]:
        result[degree] = {}
    for corner in inner_corners:
        next_edge_points = list()
        prev_edge_points = list()
        for v in vectors:
            point = (v[0]+corner[0], v[1]+corner[1])
            next_edge_points.extend([(e, point) for e in all_edges.keys() if e.p1 == point or e.p2 == point])

        for i in range(0, distance):
            prev_edge_points = [e1, e2] if i > 0 else list()
            e1 = next_edge_points[0][0]
            e2 = next_edge_points[1][0]
            p1 = next_edge_points[0][1]
            p2 = next_edge_points[1][1]
            next_edge_points = [get_next_point(ep[1], ep[0], list(all_edges.keys())) for ep in next_edge_points]

        if not e1 in new_remaining_edges or not e2 in new_remaining_edges:
            continue

        if len(prev_edge_points) > 0: # not the sides next to corner
            ne1 = prev_edge_points[0]
            ne2 = prev_edge_points[1]
            is_orthogonal_1 = e1.vec()[0] * ne1.vec()[0] + e1.vec()[1] * ne1.vec()[1] #in product of the two vectors
            is_orthogonal_2 = e2.vec()[0] * ne2.vec()[0] + e2.vec()[1] * ne2.vec()[1]
            if is_orthogonal_1 == 0 and is_orthogonal_2 == 0:
                continue #skip if both sides make a corner

        f1 = all_edges[e1]
        f2 = all_edges[e2]
        v1 = f1.step_out_direction(e1)
        v2 = f2.step_out_direction(e2)
        if ((e1.p1[0] == p1[0] and e1.p1[1] == p1[1]) and (e2.p1[0] == p2[0] and e2.p1[1] == p2[1])) \
                or ((e1.p2[0] == p1[0] and e1.p2[1] == p1[1]) and (e2.p2[0] == p2[0] and e2.p2[1] == p2[1])):
            invert = 'N'
        else:
            invert = 'Y'

        result[v1][f1.id] = (f2.id, (360 + 180 + v2 - v1) % 360, invert)
        result[v2][f2.id] = (f1.id, (360 + 180 + v1 - v2) % 360, invert)
        new_remaining_edges.pop(e1)
        new_remaining_edges.pop(e2)

    if len(new_remaining_edges) > 0:
        extra_result = extract_edges_at_distance(inner_corners, all_edges, new_remaining_edges, distance+1)
        for r in extra_result:
            result[r].update(extra_result[r])
    return result


def get_next_point(current_point:tuple[int,int],current_edge: Edge, all_edges: list[Edge]):
    vectors = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0), (-1,-1),(1 , 1),(-1,1), (1,-1)]
    edge_endpoint = current_edge.p2 if current_edge.p1 == current_point else current_edge.p1

    for v in vectors:
        point = (v[0] + edge_endpoint[0], v[1] + edge_endpoint[1])
        for e in all_edges:
            if e != current_edge and (e.p1 == point or e.p2 == point):
                return e, point

    raise Exception(f"No next point found for: {current_point} on edge: {current_edge}")

def move_forward_cube(data_grid: list[list[str]], location: Location, moves: int,adjacent_grids,faces: list[Face]) -> Location:
    cube_size = get_cube_size(data_grid)
    m = 0
    current_location = location
    result = current_location
    while m < moves:
        potential_new_location = get_next_cube_location(cube_size,current_location,adjacent_grids)
        match get_face_item(data_grid,potential_new_location,faces):
            case " ":
                raise Exception("Unexpected white space found")
            case ".":
                result = potential_new_location
                m += 1
            case "#":
                break
            case _:
                result = potential_new_location
                m += 1
                #raise Exception("Unknown grid item: " + get_face_item(data_grid,potential_new_location,faces))
        current_location = potential_new_location
        log_step(data_grid,cube_to_grid_location(data_grid,current_location,faces))

    return result


def log_step(data_grid: list[list[str]], location: Location):
    cursor = {0: "^", 90: ">", 180: "v", 270: "<"}
    data_grid[location.x][location.y] = cursor[location.direction]


def get_face_item(data_grid: list[list[str]], location: Location,faces: list[Face]) -> str:
    grid_location = cube_to_grid_location(data_grid,location,faces)
    #print(grid_location)
    if grid_location.x >= len(data_grid) or grid_location.y >= len(data_grid[0]):
        print("invalid location: "+str(grid_location))
        print("")
        print_datagrid(data_grid)

    return data_grid[grid_location.x][grid_location.y]


def cube_to_grid_location(data_grid, location: Location, faces: list[Face]) -> Location:
    cube_size = int(len(data_grid) / 3)
   # offsets = {1: (0, 2), 2: (1, 0), 3: (1, 1), 4: (1, 2), 5: (2, 2), 6: (2, 3)}
    face_id = location.face_id
    x = faces[face_id-1].grid_location[1]+location.x
    y = faces[face_id-1].grid_location[0]+location.y

    return Location(x, y, location.direction, face_id)


def get_next_cube_location(cube_size:int, location:Location,adjacent_grids) -> Location:
    # direction:(grid,rotation,invert(Y/N)

    x_dir, y_dir = location.get_move_vector()
    x, y = location.x, location.y
    dir = location.direction
    face_id = location.face_id

    if x + x_dir < 0 or x + x_dir >= cube_size or y + y_dir < 0 or y + y_dir >= cube_size:
        new_face_id, rotation, invert_xy = adjacent_grids[dir][face_id]
    else:
        rotation = 0
        new_face_id = location.face_id
        invert_xy = 'N'

    new_direction = (location.direction + rotation) % 360
    match rotation:
        case 0:
            new_x, new_y = (x + x_dir + cube_size) % cube_size, (y + y_dir + cube_size) % cube_size
        case 180:
            new_x, new_y = x, y
        case 90:
            if location.direction == 90 or location.direction == 270: # only invert if switch in direction walking
                new_x = (y + y_dir + cube_size) % cube_size
                new_y = (x + x_dir + cube_size) % cube_size
            else:
                new_x, new_y = y, x
        case 270:
            if location.direction == 0 or location.direction == 180:  # only invert if switch in direction walking
                new_x = (y + y_dir + cube_size) % cube_size
                new_y = (x + x_dir + cube_size) % cube_size
            else:
                new_x, new_y = y, x

    if invert_xy == 'Y':
        if new_direction == 0 or new_direction == 180:
            new_y = (cube_size - 1 - new_y) % cube_size
        else:
            new_x = (cube_size - 1 - new_x) % cube_size

    return Location(new_x, new_y, new_direction, new_face_id)


def print_datagrid(data_grid: list[list[str]]):
    for x in range(0,len(data_grid)):
        row = ""
        for y in range(0,len(data_grid[0])):
            row = row + data_grid[x][y]
        print(row)

def read_datagrid(data: list[str]) -> list[list[str]]:
    result: list[list[str]] = []
    max_length = max([len(line.rstrip()) for line in data[:len(data)-2]]) # removing whitespace in cube lines
    for line in data:
        new_list = list(line[:len(line)-1])
        while len(new_list) < max_length:
            new_list.append(" ")
        result.append(new_list)
    return result[:len(result)-2]


def read_password(data: list[str]) -> list[str]:
    line = data[len(data)-1]
    result = re.findall(r"(\d+|\D)", line)
    return result


ex22 = AdventOfCode(22)
ex22.executeTest(part1,"6032")
ex22.executeTest(part2,"5031")

ex22.execute(part1,part2)