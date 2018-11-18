import time

print("ECE 366 Project 4: MIPS Simulator")


def decimal_to_bin(dec_num):
    if dec_num < 0:
        pos_value = 0 - dec_num
        comp_value = 0b11111111111111111111111111111111 - pos_value + 1
        bin_num = '{0:032b}'.format(comp_value)
        return bin_num
    else:
        bin_num = '{0:032b}'.format(dec_num)
        return bin_num


def bin_to_decimal(bin_str):
    if bin_str[0] == "1":
        pos_num = int(bin_str, 2)
        all_ones = 0b1111111111111111
        dec_num = all_ones - pos_num + 1
        return 0 - dec_num
    else:
        dec_num = int(bin_str, 2)
        return dec_num


def bin_to_decimal_32b(bin_str):
    if bin_str[0] == "1":
        pos_num = int(bin_str, 2)
        all_ones = 0b11111111111111111111111111111111
        dec_num = all_ones - pos_num + 1
        return 0 - dec_num
    else:
        dec_num = int(bin_str, 2)
        return dec_num


def hex_to_bin(hex_str):
    return str(bin(int(hex_str, 16))[2:].zfill(32))


def bin_to_hex(bin_num):
    return '0x{0:08X}'.format(int(bin_num, 2))


def file_to_array(file):
    return_array = []
    for line in file:
        return_array.append(line[0:10].rstrip())
    return return_array


def print_output(reg_arr, pc):
    print("PC: ", pc)
    for i in range(1, 8):
        print("$" + str(i) + ": ", reg_arr[i])


def execute_operation(mc_hex, data_mem, reg_arr, pc, num_multicycle_instr):
    bin_str = hex_to_bin(mc_hex)
    # ADD
    if bin_str[0:6] == "000000" and bin_str[21:32] == "00000100000":
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        print("ADD $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        reg_arr[rd] = reg_arr[rs] + reg_arr[rt]
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
    # SUB
    elif bin_str[0:6] == "000000" and bin_str[21:32] == "00000100010":
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        print("SUB $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        reg_arr[rd] = reg_arr[rs] - reg_arr[rt]
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
    # XOR
    elif bin_str[0:6] == "000000" and bin_str[26:32] == "100110":
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        print("XOR $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        reg_arr[rd] = reg_arr[rt] ^ reg_arr[rs]
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
    # ADDI
    elif bin_str[0:6] == "001000":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("ADDI $" + str(rt) + ", $" + str(rs) + ", " + str(imm))
        reg_arr[rt] = reg_arr[rs] + imm
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
    # BEQ
    elif bin_str[0:6] == "000100":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("BEQ $" + str(rs) + ", $" + str(rt) + ", " + str(imm))
        if reg_arr[rt] == reg_arr[rs]:
            pc += (imm * 4)
        num_multicycle_instr[0] += 1
        print("Multi-Cycle Count: 3 Cycles")
    # BNE
    elif bin_str[0:6] == "000101":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("BNE $" + str(rt) + ", $" + str(rs) + ", " + str(imm))
        if reg_arr[rt] != reg_arr[rs]:
            pc += (imm * 4)
        num_multicycle_instr[0] += 1
        print("Multi-Cycle Count: 3 Cycles")
    # SLT
    elif bin_str[0:6] == "000000" and bin_str[21:32] == "00000101010":
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        print("SLT $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        if reg_arr[rs] < reg_arr[rt]:
            reg_arr[rd] = 1
        else:
            reg_arr[rd] = 0
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
    # LW
    elif bin_str[0:6] == "100011":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("LW $" + str(rt) + ", " + str(imm) + "($" + str(rs) + ")")
        d_mem_index = int((reg_arr[rs] - 0x2000 + imm) / 4)
        d_mem_value = data_mem[d_mem_index]
        print("MEM INDEX FOR LW", d_mem_index)
        reg_arr[rt] = d_mem_value
        num_multicycle_instr[2] += 1
        print("Multi-Cycle Count: 5 Cycles")
    # SW
    elif bin_str[0:6] == "101011":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("SW $" + str(rt) + ", " + str(imm) + "($" + str(rs) + ")")
        d_mem_index = int((reg_arr[rs] - 0x2000 + imm) / 4)
        data_mem[d_mem_index] = reg_arr[rt]
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
    pc += 4

    return [data_mem, reg_arr, pc, num_multicycle_instr]


# Give cpu_design a value of 0 for Multi-Cycle or 1 for Pipelined
def simulator(instr_mem_file_name):
    # Use the file name to create an array of instructions
    instr_mem_file = open(instr_mem_file_name, "r")
    instr_mem = file_to_array(instr_mem_file)
    reg_arr = [0, 0, 0, 0, 0, 0, 0, 0]  # Use an register for $0 - $7 ($0 will not change)
    data_mem = [0] * 1023  # Create a data memory array
    pc = 0
    mc_hex = instr_mem[pc]
    num_multicycle_instr = [0, 0, 0]    # Number of 3, 4, and 5 cycle CPU instructions, respectively
    dic = 0     # Dynamic Instruction Count
    while mc_hex != "0x1000FFFF" or mc_hex != "0x1000ffff":
        if mc_hex == "0x1000ffff":
            dic += 1
            num_multicycle_instr[0] += 1
            break
        data_set = execute_operation(mc_hex, data_mem, reg_arr, pc, num_multicycle_instr)
        data_mem = data_set[0]
        reg_arr = data_set[1]
        pc = data_set[2]
        num_multicycle_instr = data_set[3]
        print_output(reg_arr, pc)
        print("Data Mem:", data_mem[0:10], "\n")
        index = int(pc / 4)
        mc_hex = instr_mem[index]
        dic += 1

    print("Num of 3 Cycle Instructions: ", num_multicycle_instr[0])
    print("Num of 4 Cycle Instructions: ", num_multicycle_instr[1])
    print("Num of 5 Cycle Instructions: ", num_multicycle_instr[2])
    print("Dynamic Instruction Count:   ", dic)



simulator("A1.txt")
# simulator("A2.txt")
# simulator("B1.txt")
# simulator("B2.txt")