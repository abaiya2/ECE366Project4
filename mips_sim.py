print("ECE 366 Project 4: MIPS Simulator")


def file_to_array(file):
    return_array = []
    for line in file:
        return_array.append(line.rstrip())
    return return_array


def execute_operation(mc_bin, data_mem, reg_arr, pc):
    # TODO: Implement ADD, SUB, XOR, ADDI
    # TODO: Implement BEQ, BNE, SLT, LW, SW
    pc += 4

    return [mc_bin, data_mem, reg_arr, pc]


def simulator(instr_mem_file_name):
    # Use the file name to create an array of instructions
    instr_mem_file = open(instr_mem_file_name, "r")
    instr_mem = file_to_array(instr_mem_file)
    reg_arr = [0, 0, 0, 0, 0, 0, 0, 0]  # Use an register for $0 - $7 ($0 will not change)
    data_mem = [0] * 1023  # Create a data memory array
    data_address = 0x2000  # Initialize starting range of data_mem to be 0x2000
    pc = 0
    mc_bin = instr_mem[pc]
    while mc_bin != "00010000000000001111111111111111":
        print(mc_bin)
        data_set = execute_operation(mc_bin, data_mem, reg_arr, pc)
        mc_bin = data_set[0]
        data_mem = data_set[1]
        reg_arr = data_set[2]

        pc = data_set[3]
        index = int(pc / 4)
        mc_bin = instr_mem[index]


simulator("i_mem.txt")
