from AdventOfCode import AdventOfCode
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    prev: Optional["Node"] = None
    next: Optional["Node"] = None
    value: int = 0
    start_index: int = 0

    def __repr__(self):
        return f"({self.start_index},{self.value})"

    def __eq__(self,other):
        return self.start_index == other.start_index

    def __hash__(self):
        return hash(self.start_index)


def part1(data: list[str]) -> str:
    start_node = read_list(data)
    start_sequence = get_start_sequence(start_node)

    for node in start_sequence:
        reshuffle_node(node,len(start_sequence))

    zero_node = next((node for node in start_sequence if node.value == 0),None)
    result = find_node(zero_node,1000).value+find_node(zero_node,2000).value+find_node(zero_node,3000).value

    return str(result)


def part2(data: list[str]) -> str:
    start_node = read_list(data)
    _decription_key = 811589153
    decrypt(start_node,_decription_key)
    start_sequence = get_start_sequence(start_node)

    for i in range(0,10):
        for node in start_sequence:
            reshuffle_node(node, len(start_sequence))

    zero_node = [node for node in start_sequence if node.value == 0][0]
    result = find_node(zero_node,1000).value+find_node(zero_node,2000).value+find_node(zero_node,3000).value

    return str(result)


def read_list(data: list[str]) -> Node:
    start_node = Node(start_index = 0, value = int(data[0]))
    current_node = start_node
    for i in range(1,len(data)):
        next_node = Node()
        next_node.value = int(data[i])
        next_node.start_index = i

        next_node.prev = current_node
        current_node.next = next_node
        current_node = next_node

    start_node.prev = current_node
    current_node.next = start_node
    return start_node


def get_start_sequence(start_node:Node) -> list[Node]:
    start_sequence = [start_node]
    current_node = start_node.next
    while current_node != start_node:
        start_sequence.append(current_node)
        current_node = current_node.next
    return start_sequence


def reshuffle_node(node: Node,list_size):
    next_node = node
    max_steps = next_node.value % (list_size -1)

    if max_steps == 0:
        return
    else:
        # removing node from list
        node.prev.next = node.next
        node.next.prev = node.prev

    for i in range(0,max_steps):
        next_node = next_node.next

    #inserting node in list
    node.next = next_node.next
    node.prev = next_node
    next_node.next.prev = node
    next_node.next = node





def decrypt(start_node:Node, key: int):
    next_node = start_node.next
    start_node.value *= key
    while next_node != start_node:
        next_node.value*=key
        next_node = next_node.next


def find_node(start_node: Node, cnt:int) -> Node:
    result = start_node
    for i in range(0,cnt):
        result = result.next

    print(f"node found: {result} at {cnt}")
    return result

def print_list(start_node: Node):
    result = str(start_node)
    node = start_node.next
    while node != start_node:
        result += " " + str(node)
        node = node.next
    print(result)


ex20 = AdventOfCode(20)
ex20.executeTest(part1,"3")
ex20.executeTest(part2,"1623178306")

ex20.execute(part1,part2)
