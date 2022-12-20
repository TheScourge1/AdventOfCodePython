from AdventOfCode import AdventOfCode
from enum import Enum


class Cmd(Enum):
    noop = 1
    add_x = 2


class Regs(Enum):
    X = 1


COMMANDS = {'noop': Cmd.noop, 'addx': Cmd.add_x}
SIGNAL_TIMES = [20, 60, 100, 140, 180, 220]


class Memory:
    def __init__(self, program: [str]):
        self.register = {Regs.X: 0}
        self.program = program
        self.instruction_index = 0


class Processor:
    _command_cycles = {Cmd.noop: 1, Cmd.add_x: 2}

    def __init__(self, program: [str]):
        self.clock = 0
        self.processing_time_left = 0
        self.current_command = None
        self.current_params = []
        self.mem = Memory(program)

    def _execute_noop(self):
        pass

    def _execute_add_x(self, mem: Memory, x: int):
        mem.register[Regs.X] = mem.register[Regs.X] + x

    def tick_clock(self) -> bool:
        if self.processing_time_left == 0:
            self._load_instruction()
        if self.current_command is None:
            return False
        if self.processing_time_left > 1:
            self.processing_time_left -= 1
        else:
            self.processing_time_left = 0
            if self.current_command == Cmd.noop:
                self._execute_noop()
            elif self.current_command == Cmd.add_x:
                self._execute_add_x(self.mem, int(self.current_params[0]))
            else:
                raise Exception(f"Unknown command found: {self.current_command}")
        self.clock += 1
        return True

    def _load_instruction(self):
        if self.mem.instruction_index == len(self.mem.program):
            self.current_command = None
        else:
            instruction = self.mem.program[self.mem.instruction_index].strip().split(" ")
            if not instruction[0] in COMMANDS.keys():
                raise Exception(f"Unknown command: {instruction}")

            self.current_command = COMMANDS[instruction[0]]
            self.current_params = instruction[1:]
            self.mem.instruction_index += 1
            self.processing_time_left = self._command_cycles[self.current_command]

    def get_reg(self, reg: Regs.X):
        return self.mem.register[reg]


def part1(data: [str]) -> int:
    processor = Processor(data)
    processor.mem.register[Regs.X] = 1
    result = 0
    while processor.tick_clock():
        if processor.clock+1 in SIGNAL_TIMES:
            result += (processor.clock+1) * processor.mem.register[Regs.X]
    return result


def part2(data: [str]) -> str:
    processor = Processor(data)
    processor.mem.register[Regs.X] = 1

    line = ""
    for c in range(0,240):
        x = c % 40
        if processor.mem.register[Regs.X]-1 <= x <= processor.mem.register[Regs.X]+1:
            line += "#"
        else:
            line += "."

        if x == 39:
            print(line)
            line = ""
        processor.tick_clock()


ex10 = AdventOfCode(10)

ex10.executeTest(part1, 13140)
ex10.executeTest(part2, None)
ex10.execute(part1, part2)
