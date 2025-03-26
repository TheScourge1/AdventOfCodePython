from AdventOfCode import AdventOfCode
import math


class Device:
    a: int
    b: int
    c: int
    p: int

    data: list[int]
    output: list[int]

    def __init__(self, a, b, c, data):
        self.a = a
        self.b = b
        self.c = c
        self.p = 0
        self.data = data
        self.output = []

    def __repr__(self):
        return f"({self.a}, {self.b}, {self.c}) -> p = {self.p} \n{"".join(map(str, self.data))}\nOut: {self.output}"

    def get_combo(self, combo):
        if combo in [0, 1, 2, 3]:
            return combo
        elif combo == 4:
            return self.a
        elif combo == 5:
            return self.b
        elif combo == 6:
            return self.c
        else:
            return None

    def do_step(self):
        if self.p >= len(self.data):
            return -1

        cmd = self.data[self.p]
        combo = self.get_combo(self.data[self.p+1])
        literal = self.data[self.p+1]
        #print(f"cmd: {cmd} comb: {combo} lit:{literal} {self}")
        if cmd == 0:
            self.a = self.a // int(math.pow(2, combo))
        elif cmd == 1:
            self.b = self.b ^ literal
        elif cmd == 2:
            self.b = combo % 8
        elif cmd == 3:
            if self.a != 0:
                self.p = literal
            else:
                self.p += 2
        elif cmd == 4:
            self.b = self.b ^ self.c
        elif cmd == 5:
            self.output.append(combo % 8)
        elif cmd == 6:
            self.b = self.a // int(math.pow(2, combo))
        elif cmd == 7:
            self.c = self.a // int(math.pow(2, combo))

        if cmd != 3:
            self.p += 2
        return self.p

    def test_output(self) -> bool:
        return self.data[:len(self.output)] == self.output


    def get_result(self) -> list[int]:
        while self.do_step() >= 0:
            pass
        return self.output


def part1(data: list[str]):
    device = read_data(data)
    result = device.get_result()

    return "".join([str(i)+"," for i in result])[0:-1]


def part2(data: list[str]):
    device = read_data(data)
    min_value = get_min_value(device)
    search_size = 4
    digits = len(str(min_value))
    part_found = len(device.data)-4

    return find_digit(digits-search_size,min_value,device,search_size, part_found)


def find_digit(d: int, current_val: int, device: Device, search_size:int, part_found) -> int:
    if part_found < 0:
        return current_val
    if d < 0:
        return -1

    for i in range(0,  int(math.pow(10, search_size))):
        next_val = current_val + i*int(math.pow(10, d))
        t = Device(next_val,device.b, device.c, device.data)
        output = t.get_result()
        if output[part_found:] == device.data[part_found:]:
            if output == device.data:
                return next_val
            min_value = current_val + (i-1)*int(math.pow(10, d))
            res = find_digit(d-1, min_value, device, search_size, part_found-1)
            if res != -1:
                return res
    return -1


def get_min_value(device: Device) -> int:
    length = len(device.data)
    up = int(math.pow(10, length))
    low = 0

    while up - low > 2:
        new_mid = low + (up - low) // 2
        t1 = Device(new_mid, device.b,device.c,device.data)
        res = len(t1.get_result())
        if res < length:
            low = new_mid
        else:
            up = new_mid
    return up


def read_data(data: list[str]) -> Device:
    a = int(data[0].split().pop())
    b = int(data[1].split().pop())
    c = int(data[2].split().pop())

    input_str = list(map(int,data[4].split().pop().split(",")))
    return Device(a, b, c, input_str)


ex = AdventOfCode(17)
ex.executeTest(part1, "4,6,3,5,6,3,5,2,1,0")
ex.executeTest(part2, 117440, 2)

ex.execute(part1, part2)
