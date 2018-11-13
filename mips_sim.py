print("ECE 366 Project 4: MIPS Simulator")


def decimal_to_bin(dec_num):
    if dec_num < 0:
        pos_value = 0 - dec_num
        comp_value = 0b11111111111111111111111111111111 - pos_value  + 1
        bin_num = '{0:032b}'.format(comp_value)
        return bin_num
    else:
        bin_num = '{0:032b}'.format(dec_num)
        return bin_num


def bin_to_decimal(bin_str):
    if bin_str[0] == "1":
        dec_num = 0b11111111111111111111111111111111 \
                  - int(bin_str, 2) + 1
        return dec_num
    else:
        dec_num = int(bin_str, 2)
        return dec_num


def hex_to_bin(hex_str):
    return str(int(hex_str, 16))[2:].zfill(32)


def bin_to_hex(bin_num):
    return '0x{0:08X}'.format(int(bin_num, 2))


def file_to_array(file):
    return_array = []
    for line in file:
        return_array.append(line.rstrip())
    return return_array


def print_output(reg_arr, pc):
    print("PC: ", '0x{0:08X}'.format(pc))
    for i in range(1, 8):
        bin_num = decimal_to_bin(reg_arr[i])
        print("$" + str(i) + ": ", bin_to_hex(bin_num))


def execute_operation(mc_hex, data_mem, reg_arr, pc):
    bin_str = hex_to_bin(mc_hex)
    # ADD
    if bin_str[0:6] == "000000" and bin_str[21:32] == "00000100000":
        print("ADD")
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        reg_arr[rd] = reg_arr[rs] + reg_arr[rt]
    # SUB
    elif bin_str[0:6] == "000000" and bin_str[21:32] == "00000100010":
        print("SUB")
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        reg_arr[rd] = reg_arr[rs] - reg_arr[rt]
    # XOR
    elif bin_str[0:6] == "000000" and bin_str[26:32] == "100110":
        print("XOR")
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        reg_arr[rd] = reg_arr[rt] ^ reg_arr[rs]
    # ADDI
    elif bin_str[0:6] == "001000":
        print("ADDI")
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:31]
        imm = bin_to_decimal(imm_bin)
        reg_arr[rs] = reg_arr[rt] + imm
    # BEQ
    elif bin_str[0:6] == "000100":
        print("BEQ")
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:31]
        imm = bin_to_decimal(imm_bin)
        if reg_arr[rt] == reg_arr[rs]:
            pc += (imm * 4)
    # BNE
    elif bin_str[0:6] == "000101":
        print("BNE")
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:31]
        imm = bin_to_decimal(imm_bin)
        if reg_arr[rt] != reg_arr[rs]:
            pc += (imm * 4)
    # SLT
    elif bin_str[0:6] == "000000" and bin_str[26:32] == "00000101010":
        print("SLT")
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        if reg_arr[rs] < reg_arr[rt]:
            reg_arr[rd] = 1
        else:
            reg_arr[rd] = 0
    # LW
    elif bin_str[0:6] == "100011":
        print("LW")
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:31]
        imm = bin_to_decimal(imm_bin)
        d_mem_index = int((reg_arr[rs] - 0x2000 + imm) / 4)
        d_mem_value = data_mem[d_mem_index]
        reg_arr[rt] = bin_to_decimal(hex_to_bin(d_mem_value))
    # SW
    elif bin_str[0:6] == "101011":
        print("SW")
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:31]
        imm = bin_to_decimal(imm_bin)
        d_mem_index = int((reg_arr[rs] - 0x2000 + imm) / 4)
        data_mem[d_mem_index] = bin_to_hex(decimal_to_bin(reg_arr[rt]))
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
