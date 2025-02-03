from AdventOfCode import AdventOfCode


def part1(data: list[str]):
    line = data[0].strip()
    front_counter = 0
    front_remaining = int(line[front_counter])
    back_counter = len(line)-1
    back_remaining = int(line[back_counter])
    target_position = 0
    result = 0
    res_str = ""
    while front_counter < back_counter:
        while front_remaining > 0:
            result += (front_counter // 2) * target_position
            res_str += str(front_counter // 2) + " "
            target_position += 1
            front_remaining -= 1
        gap_remaining = int(line[front_counter+1])
        while gap_remaining > 0:
            while back_remaining == 0:
                back_counter -= 2
                back_remaining = int(line[back_counter])
            if back_counter <= front_counter:
               break

            result += (back_counter // 2) * target_position
            res_str += str(back_counter // 2) + " "
            target_position += 1
            gap_remaining -= 1
            back_remaining -= 1

        front_counter += 2
        front_remaining = int(line[front_counter])

    while back_remaining > 0 and front_counter == back_counter:
        result += (back_counter // 2) * target_position
        res_str += str(back_counter // 2) + " "
        back_remaining -= 1
        target_position += 1

    return result


def part2(data: list[str]):
    line = data[0].strip()+"0"
    disk_blocks = []
    for i in range(0, len(line)//2):
        for j in range(0, int(line[2*i])):
            disk_blocks.append(str(i))
        for j in range(0, int(line[2*i+1])):
            disk_blocks.append(".")

    print("".join(disk_blocks))

    for i in range(len(line)//2 - 1, -1, -1):
        loc = disk_blocks.index(str(i))
        size = disk_blocks.count(str(i))
        free_space_loc = get_free_space(disk_blocks,size)
        if -1 < free_space_loc < loc:
            for j in range(0,size):
                disk_blocks[free_space_loc+j] = str(i)
                disk_blocks[loc+j] = "."

    print("".join(disk_blocks))
    result = 0
    for i in range(0, len(disk_blocks)):
        result += i * int(disk_blocks[i]) if disk_blocks[i] != "." else 0

    return result


def get_free_space(lst:list[str], size:int) -> int:
    for i in range(0,len(lst)-size):
        if lst[i:i+size] == ["."]*size:
            return i
    return -1


ex = AdventOfCode(9)
ex.executeTest(part1, 1928)
ex.executeTest(part2, 2858)


ex.execute(part1, part2)