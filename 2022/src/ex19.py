from AdventOfCode import AdventOfCode
from dataclasses import dataclass
import time


_materials = {"ore":0,"clay":1,"obsidian":2,"geode":3}

@dataclass
class Blueprint:
    id: int
    bots: list[list[int]]


def part1(data: list[str]) -> str:
    blueprints = [read_blueprint(line) for line in data]
    max_geode_produced = [max_geode(blueprint,24) for blueprint in blueprints]

    result = 0
    for id in range(0,len(max_geode_produced)):
        result += (id+1)*max_geode_produced[id]

    return str(result)


def part2(data: list[str]) -> str:
    blueprints = [read_blueprint(line) for line in data]
    result = 1
    for i in range(0,min(len(data),3)):
        result = result * max_geode(blueprints[i],32)

    return str(result)


def max_geode(blueprint: Blueprint,minutes: int) -> int:
    result = max_geode_sub_2(blueprint,minutes)
    return result


def max_geode_sub_2(blueprint: Blueprint, minutes:int) -> int:
    current_states = {((0,0,0,0),(1,0,0,0))} # (material_count,bot_count)
    max_state = [[0,0,0,0],[1,0,0,0]]
    max_mat_needed_per_turn = [0] * 4
    for i in range(0, 4):
        max_mat_needed_per_turn[i] = max([b[i] for b in blueprint.bots])

    start_time_1 = time.time()
    for timer in range(0,minutes):
        start_time = time.time()
        new_states = set()
        for state in current_states:
            material_count = state[0]
            bot_count = state[1]

            for i in range(0,len(blueprint.bots)):
                 if sum([1 for t in zip(material_count,blueprint.bots[i]) if t[0] >= t[1]]) == 4:
                    new_material_count = tuple([t[0]-t[1]+t[2] for t in zip(material_count, blueprint.bots[i], bot_count)])
                    new_bot_count = list(bot_count)
                    new_bot_count[i] += 1
                    new_state= (new_material_count, tuple(new_bot_count))
                    if (i == 3) or bot_needed(new_state[0][i],new_state[1][i],max_mat_needed_per_turn[i],minutes - timer) :
                        new_states.add(new_state)

            if sum([1 for t in zip(material_count, blueprint.bots[3]) if t[0] >= t[1]]) < 4: # producing no bot
                new_material_count = [t[0]+t[1] for t in zip(material_count, bot_count)]
                new_material_count = limit_to_max_needed(new_material_count,bot_count,max_mat_needed_per_turn,minutes - timer)
                new_states.add((tuple(new_material_count), bot_count))

            for i in range(0,4): #only for logging plz remove
                if max_state[0][i] < material_count[i]:
                    max_state[0][i] = material_count[i]
                if max_state[1][i] < bot_count[i]:
                    max_state[1][i] = bot_count[i]

        print(f"state at the end of {timer}: {len(new_states)} - max: {max_state} in {int(time.time() - start_time)} s")
        current_states = new_states
        # prune_states_2(new_states, blueprint,minutes - timer)

    print(f"Max geode: {max([s[0][3] for s in current_states])} in {int(time.time()-start_time_1)} s")
    return max([s[0][3] for s in current_states])


def bot_needed(material:int, bot_count:int, max_material_needed_a_turn: int,time_left:int) -> bool:
    available_mats = material + (bot_count-1) * time_left
    if max_material_needed_a_turn * (time_left ) < available_mats:
        return False
    return True


def limit_to_max_needed(materials: list[int,int,int,int], bots: list[int,int,int,int], max_mats_needed: list[int,int,int,int],time_left:int) -> list[int,int,int,int]:
    result = materials.copy()
    for i in range(0,3):
        if materials[i]+bots[i]*time_left > max_mats_needed[i]*time_left:
            result[i] = min(max_mats_needed[i]*time_left - bots[i] * time_left,max_mats_needed[i])
    return result


def read_blueprint(line: str) -> Blueprint:
    id = int(line.split(" ")[1].split(":")[0])
    bot_defs = [bot_def.strip() for bot_def in line.split(":")[1].split(".") if bot_def.startswith(" Each")]

    bots = [[]] * 4
    for bot_def in bot_defs:
        words = bot_def.split(" ")
        bot_name = words[1]
        costs = [0,0,0,0]
        for i in range(2,len(words)):
            if words[i].isnumeric():
                costs[get_material(words[i+1])] = int(words[i])
        bots[get_material(bot_name)] = costs

    return Blueprint(id,bots)


def get_material(material: str) -> int:
    if material in _materials.keys():
        return _materials[material]
    else:
        raise Exception("Unknown material: " + material)


ex19 = AdventOfCode(19)
#ex19.executeTest(part1, "33")
ex19.executeTest(part2, "3472")

ex19.execute(part1, part2)
# to low: 36432
