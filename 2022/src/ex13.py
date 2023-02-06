from AdventOfCode import AdventOfCode
from functools import cmp_to_key


def part1(data: list[str]):
    pair_list = read_data(data)
    result = 0
    for i in range(0,len(pair_list)):
        pair = pair_list[i]
        if check_order(pair[0],pair[1]) > 0:
            result += i+1
    return result


def part2(data: list[str]):
    pair_list = read_data(data+["", "[[6]]", "[[2]]"])
    input_list = [p[0] for p in pair_list]+[p[1] for p in pair_list]
    input_list.sort(key=cmp_to_key(check_order), reverse=True)

    return (input_list.index([[2]])+1)*(input_list.index([[6]])+1)


def read_data(data: list[str]) -> list[(list, list)]:
    result = []
    current_pair:list = []
    for line in data:
        if line.strip() == "":
            if len(current_pair) != 2:
                raise Exception(f"unexpected pair found: {current_pair}")
            result.append((current_pair[0],current_pair[1]))
            current_pair = []
        else:
            current_pair.append(read_line(line))
    if current_pair:
        result.append((current_pair[0],current_pair[1]))
    return result


def read_line(line: str) -> list:
    result: list = []
    list_stack = [result]
    current_list:list = []
    current_number = ""
    for c in line.strip():
        if c == '[':
            current_list = []
            list_stack[len(list_stack) - 1].append(current_list)
            list_stack.append(current_list)
        elif c == ']':
            if len(current_number) > 0:
                current_list.append(int(current_number))
            current_number = ""
            list_stack.remove(current_list)
            current_list = list_stack[len(list_stack)-1]
        elif c == ",":
            if len(current_number) > 0:
                current_list.append(int(current_number))
                current_number = ""
        else:
            current_number += c
    return result[0]


def check_order(left: list, right: list) -> int:
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return 1
            elif left > right:
                return -1
            else:
                return 0
        else:
            return check_order([left], right)
    else:
        if isinstance(right, int):
            return check_order(left, [right])
        else:
            max_index = min(len(left), len(right))
            for index in range(0, max_index):
                result = check_order(left[index], right[index])
                if result != 0:
                    return result

            if len(left) < len(right):
                return 1
            elif len(right) < len(left):
                return -1
            else:
                return 0

ex13 = AdventOfCode(13)
ex13.executeTest(part1, 13)
ex13.executeTest(part2, 140)
ex13.execute(part1, part2)

