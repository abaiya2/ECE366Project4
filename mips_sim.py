print("ECE 366 Project 4: MIPS Simulator")


def decimal_to_bin(dec_num):
    bin_num = 0
    if dec_num < 0:
        pos_value = 0 - dec_num
        comp_value = 0b11111111111111111111111111111111 - pos_value  + 1
        bin_num = '{0:032b}'.format(comp_value)
    else:
        bin_num = '{0:032b}'.format(dec_num)
    return bin_num


def bin_to_decimal(bin_str):
    dec_num = 0
    if bin_str[0] == "1":
        dec_num = 0b11111111111111111111111111111111 \
                  - int(bin_str, 2) + 1
    else:
        dec_num = int(bin_str, 2)


def hex_to_bin(hex_str):
    return str(int(hex_str, 16))[2:].zfill(32)


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
    # TODO: Implement BEQ, BNE, SLT, LW, SW
    bin_str = hex_to_bin(mc_hex)
    # ADD
    if bin_str[0:6] == "000000" and bin_str[21:32] == "00000100000":
        print("ADD")
        rd = int(bin_str[16:21], 2)
        rs = int(bin_str[6:11], 2)
        rt = int(bin_str[11:16], 2)
        reg_arr[rd] = reg_arr[rs] + reg_arr[rt]
    # SUB
    elif bin_str[0:6] == "000000" and bin_str[21:32] == "00000100010":
        print("SUB")
        rd = int(bin_str[16:21], 2)
        rs = int(bin_str[6:11], 2)
        rt = int(bin_str[11:16], 2)
        reg_arr[rd] = reg_arr[rs] - reg_arr[rt]
    # XOR
    elif bin_str[0:6] == "000000" and bin_str[26:32] == "100110":
        print("XOR")
    # ADDI
    elif bin_str[0:6] == "001000":
        print("ADDI")
    # BEQ
    elif bin_str[0:6] == "000100":
        print("BEQ")
    # BNE
    elif bin_str[0:6] == "000101":
        print("BNE")
    # SLT
    elif bin_str[0:6] == "000000" and bin_str[26:32] == "00000101010":
        print("SLT")
    # LW
    elif bin_str[0:6] == "100011":
        print("LW")
    # SW
    elif bin_str[0:6] == "101011":
        print("SW")
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
