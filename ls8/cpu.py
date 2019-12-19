"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branch_table ={
            130: self.load_command,
            71: self.print_command,
            162: self.mult_command,
            1: self.halt_command
        }
        self.IR = self.ram_read(self.pc)
        self.operand_a = self.ram_read(self.pc + 1)
        self.operand_b = self.ram_read(self.pc + 2)
        self.running = False

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []
        # For now, we've just hardcoded a program:

        input_file = sys.argv[1]

        with open(input_file) as contents:
            for line in contents:
                cleansed_instruction = line.split('#', 1)[0].strip()
                if len(cleansed_instruction) > 0:
                    program.append(int(cleansed_instruction,2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load_command(self):
        self.reg[self.operand_a[0]] = self.operand_b[0]
        self.pc += 3

    def print_command(self):
        print(self.reg[self.operand_a[0]])
        self.pc += 2

    def mult_command(self):
        self.alu("MUL", self.operand_a[0], self.operand_b[0])
        self.pc += 3

    def halt_command(self):
        self.running = True


    def run(self):
        """Run the CPU."""
    
        while self.running == False:

            self.IR = self.ram_read(self.pc)
            self.operand_a = self.ram_read(self.pc + 1),
            self.operand_b = self.ram_read(self.pc + 2),
            
            operation = self.branch_table[self.IR]
            operation()
            

            
