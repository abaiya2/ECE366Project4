print("ECE 366 Project 4: MIPS Simulator")


def file_to_array(file):
    return_array = []
    for line in file:
        return_array.append(line.rstrip())
    return return_array


def print_output(reg_arr, pc):
    print("PC: ", '0x{0:08X}'.format(pc))
    for i in range(1, 8):
        print("$" + str(i) + ": ", '0x{0:08X}'.format(reg_arr[i]))


def execute_operation(mc_hex, data_mem, reg_arr, pc):
    # TODO: Implement ADD, SUB, XOR, ADDI
    # TODO: Implement BEQ, BNE, SLT, LW, SW
    pc += 4

    return [data_mem, reg_arr, pc]


# Give cpu_design a value of 0 for Multi-Cycle or 1 for Pipelined
def simulator(instr_mem_file_name, cpu_design):
    if cpu_design == 0:
        print("Multi-Cycle CPU: ")
    else:
        print("Pipelined CPU: ")
    # Use the file name to create an array of instructions
    instr_mem_file = open(instr_mem_file_name, "r")
    instr_mem = file_to_array(instr_mem_file)
    reg_arr = [0, 0, 0, 0, 0, 0, 0, 0]  # Use an register for $0 - $7 ($0 will not change)
    data_mem = [0] * 1023  # Create a data memory array
    data_address = 0x2000  # Initialize starting range of data_mem to be 0x2000
    pc = 0
    mc_hex = instr_mem[pc]
    while mc_hex != "0x1000FFFF":
        data_set = execute_operation(mc_hex, data_mem, reg_arr, pc)
        data_mem = data_set[0]
        reg_arr = data_set[1]
        pc = data_set[2]
        index = int(pc / 4)
        mc_hex = instr_mem[index]

    print_output(reg_arr, pc)


simulator("i_mem.txt", 0)
simulator("i_mem.txt", 1)
