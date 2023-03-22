from AdventOfCode import AdventOfCode
from dataclasses import dataclass
from collections import defaultdict

from sortedcontainers import SortedList

@dataclass
class Valve:
    name: str
    rate: int
    tunnels: list[str]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def part1(data: list[str]):
    all_valves = read_data(data)
    usefull_valves = [valve for valve in all_valves if valve.rate > 0]
    start_valve = [valve for valve in all_valves if valve.name == 'AA'][0]

    adjacent_valves = get_adjacent_valves(all_valves,[start_valve]+usefull_valves)
    all_paths = get_all_paths([start_valve]+usefull_valves,adjacent_valves)
    list_of_valves = list(all_paths[start_valve].keys())

    result = find_max_valve_combo(all_paths,start_valve,list_of_valves,0,0)
    return result


def part2(data: list[str]):
    all_valves = read_data(data)
    usefull_valves = [valve for valve in all_valves if valve.rate > 0]
    start_valve = [valve for valve in all_valves if valve.name == 'AA'][0]

    adjacent_valves = get_adjacent_valves(all_valves,[start_valve]+usefull_valves)
    all_paths = get_all_paths([start_valve]+usefull_valves,adjacent_valves)
    list_of_valves = list(all_paths[start_valve].keys())

    print(f"locations_to_visit: {len(all_paths[start_valve].keys())}")
    #result = find_max_valve_double_combo(all_paths,(start_valve,start_valve),list_of_valves,0,(4,4))
    result = find_max_valve_combo2(all_paths,start_valve,4,list_of_valves,[],[],defaultdict(int))


    return result


def find_max_valve_combo2(all_paths: dict[Valve, dict[Valve, int]], start_location: Valve, current_timer:int,
                         locations_to_visit: list[Valve], list1: list[Valve],list2: list[Valve], cache:dict[str,int]) -> int:

    if len(locations_to_visit) > 0:
        remaining_locations = locations_to_visit[1:]
        next_location = locations_to_visit[0]
        res1 = find_max_valve_combo2(all_paths, start_location, current_timer,remaining_locations, list1+[next_location], list2,cache)
        res2 = find_max_valve_combo2(all_paths, start_location, current_timer,remaining_locations, list1, list2+[next_location],cache)
        return max(res1, res2)
    else:
        list1_str = ''.join(v.name for v in list1)
        list2_str = ''.join(v.name for v in list2)
        val1 = 0
        val2 = 0
        if list1_str in cache.keys():
            val1 = cache[list1_str]
            print('cache hit1: '+ list1_str)
        else:
            val1 = find_max_valve_combo(all_paths,start_location,list1,0,current_timer)
            cache[list1_str] = val1

        if list2_str in cache.keys():
            val2 = cache[list2_str]
            print('cache hit2: ' + list2_str)
        else:
            val2 = find_max_valve_combo(all_paths, start_location, list2, 0, current_timer)
            cache[list2_str] = val2

        return val1 + val2


def find_max_valve_combo(all_paths: dict[Valve, dict[Valve, int]], current_location: Valve,
                         locations_to_visit: list[Valve], current_value: int, current_timer: int) -> int:

    result = current_value
    for next_location in locations_to_visit:
        path_length = all_paths[current_location][next_location]
        new_timer = current_timer + path_length + 1
        if new_timer < 30:
            new_value = current_value + (30-new_timer)*next_location.rate
            remaining_locations = locations_to_visit.copy()
            remaining_locations.remove(next_location)
            new_res = find_max_valve_combo(all_paths, next_location, remaining_locations, new_value, new_timer)
            if new_res > result:
                result = new_res

    return result


def find_max_valve_double_combo(all_paths: dict[Valve, dict[Valve, int]], current_locations: tuple[Valve,Valve],
                         locations_to_visit: list[Valve], current_result: int, current_timers: tuple[int,int]) -> int:
    result = current_result

    for next_location in locations_to_visit:
        if current_locations[0] == current_locations[1]:
            print(f"visiting: {next_location}")
        next_timer_1 = current_timers[0] + all_paths[current_locations[0]][next_location] + 1
        next_timer_2 = current_timers[1] + all_paths[current_locations[1]][next_location] + 1

        remaining_locations = locations_to_visit.copy()
        remaining_locations.remove(next_location)

#Finishing timer 1 first does not work as only the remainder locations rest available for timer 2
        if next_timer_1 < 30 and next_timer_1 <= next_timer_2:
            new_possible_value = current_result + (30 - next_timer_1) * next_location.rate
            new_res = find_max_valve_double_combo(all_paths, (next_location, current_locations[1]),
                                                  remaining_locations, new_possible_value, (next_timer_1, current_timers[1]))
            if new_res > result:
                result = new_res

        if next_timer_2 < 30:
            new_possible_value = current_result + (30 - next_timer_2) * next_location.rate
            new_res = find_max_valve_double_combo(all_paths, (current_locations[0],next_location),
                                                  remaining_locations, new_possible_value, (current_timers[0], next_timer_2))
            if new_res > result:
                result = new_res

    return result


def get_path_value(path: list[Valve], all_paths:  dict[Valve,dict[Valve, int]]) -> int:
    result = 0
    current_valve = path[0]
    timer = 0
    for next_valve in path[1:]:
        timer += all_paths[current_valve][next_valve] + 1
        if timer > 30:
            return result
        else:
            result += next_valve.rate * (30-timer)
        current_valve = next_valve

    return result


def get_all_paths(all_valves: list[Valve], adjacent_valves: dict[Valve, dict[Valve, int]]) -> dict[Valve,dict[Valve, int]]:
    result: dict[Valve,dict[Valve, int]] = {}
    for valve in all_valves:
        result[valve] = get_path_lengths(valve, adjacent_valves)
    return result


def get_path_lengths(from_valve: Valve, adjacent_valves: dict[Valve, dict[Valve, int]]) -> dict[Valve, int]:
    result: dict[Valve, int] = {from_valve: 0}
    visited: set[Valve] = set()
    while len(set(result.keys()).difference(visited)) > 0:
        potential_new_visits = set(result.keys()).difference(visited)
        next_visit = potential_new_visits.pop()
        for v in potential_new_visits:
            if result[v] < result[next_visit]:
                next_visit = v
        visited.add(next_visit)

        paths = adjacent_valves[next_visit]
        for path in paths.keys():
            if path not in result.keys():
                result[path] = result[next_visit] + paths[path]
            elif result[path] > result[next_visit] + paths[path]:
                result[path] = result[next_visit] + paths[path]
    result.pop(from_valve)
    return result


def get_adjacent_valves(all_valves: list[Valve], valves_so_search:  list[Valve]) -> dict[Valve, dict[Valve, int]]:
    result: dict[Valve, dict[Valve, int]] = {}
    for source_valve in valves_so_search:
        result[source_valve] = get_neighbour_valves(source_valve, all_valves)
    return result


def get_neighbour_valves(valve:Valve, all_valves: list[Valve]) -> dict[Valve,int]:
    res: dict[Valve, int] = {}
    valves_to_visit = valve.tunnels
    path_length = 0
    visited: set[str] = {valve.name}
    while len(valves_to_visit) > 0:
        new_valves_to_visit = []
        path_length += 1
        for valve_name in valves_to_visit:
            target = list(filter(lambda v: v.name == valve_name, all_valves))[0]
            if target.name in visited:
                pass
            elif target.rate > 0:
                res[target] = path_length
            else:
                new_valves_to_visit.extend([v for v in target.tunnels])
            visited.add(target.name)
        valves_to_visit = new_valves_to_visit
    return res


def read_data(data: list[str]) -> list[Valve]:
    result = []
    for line in data:
        line = line.strip()
        name = line[6:8]
        rate = line[line.index("=")+1:line.index(";")]
        tunnels = []
        if "valves" in line:
            tunnels = line[line.index("valves") + 7:].split(", ")
        else:
            tunnels.append(line[line.index("valve") + 6:])
        result.append(Valve(name=name, rate=int(rate), tunnels=tunnels))

    return result


ex16 = AdventOfCode(16)
ex16.executeTest(part1, 1651)
ex16.executeTest(part2, 1707)

ex16.execute(part1, part2)