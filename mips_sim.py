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


def get_dependent_instruction(mc_hex):
    bin_str = hex_to_bin(mc_hex)
    rd = 0
    rt = 0
    rs = 0
    source_registers = []
    target_register = 0
    # R - Type
    if bin_str[0:6] == "000000":
        # *** $rd, $rs, $rt
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        target_register = rd
        source_registers = [rt, rs]
        print("*** $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
    # ADDI
    elif bin_str[0:6] == "001000":
        # ADDI $rt, $rs, imm
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        source_registers = [rs]
        target_register = rt
    # BRANCH
    elif bin_str[0:6] == "000100" or bin_str[0:6] == "000101":
        # B** $rs, $rt, imm
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        source_registers = [rt, rs]
    # LW
    elif bin_str[0:6] == "100011":
        # LW $rt, imm($rs)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        source_registers = [rs]
        target_register = rt
    # SW
    elif bin_str[0:6] == "101011":
        # SW $rt, imm($rs)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        source_registers = [rt, rs]
    return [source_registers, target_register]

def run_cache_sim_config(num_words,num_ways,num_sets):



def cache_sim(addr_mem):
    for i in range(0, len(addr_mem)):
        hex_num = 0x2000 + (addr_mem[i] * 4)
        addr_mem[i] = hex_num
        print(hex(addr_mem[i]))
    run_cache_sim_config(4,1,2)#config 3A
    run_cache_sim_config(2,1,4)#config 3B
    run_cache_sim_config(2,4,1)#config 3C
    run_cache_sim_config(8,2,4)#config 3D

def execute_operation(mc_hex, data_mem, reg_arr, pc, num_multicycle_instr, pipe_delays, mc_prev, mc_next):
    bin_str = hex_to_bin(mc_hex)
    lw_addr = 999999999
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
            print("A STALL IS NEEDED FOR BEQ TO FLUSH THE NEXT INSTR")
            pipe_delays[1] += 1
        num_multicycle_instr[0] += 1
        print("Multi-Cycle Count: 3 Cycles")
        data_registers = get_dependent_instruction(mc_prev)
        target_register = data_registers[1]
        if target_register == rt or target_register == rs:
            print("A STALL IS NEEDED FOR BEQ, WHICH NEEDS AN OPERAND")
            pipe_delays[0] += 1
    # BNE
    elif bin_str[0:6] == "000101":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("BNE $" + str(rt) + ", $" + str(rs) + ", " + str(imm))
        if reg_arr[rt] != reg_arr[rs]:
            pc += (imm * 4)
            print("A STALL IS NEEDED FOR BNE TO FLUSH THE NEXT INSTR")
            pipe_delays[1] += 1
        num_multicycle_instr[0] += 1
        print("Multi-Cycle Count: 3 Cycles")
        data_registers = get_dependent_instruction(mc_prev)
        target_register = data_registers[1]
        if target_register == rt or target_register == rs:
            print("A STALL IS NEEDED FOR BNE, WHICH NEEDS AN OPERAND")
            pipe_delays[0] += 1
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
        lw_addr= d_mem_index
        data_registers = get_dependent_instruction(mc_next)
        source_registers = data_registers[0]
        for i in range(0, len(source_registers)):
            cur_src_reg = source_registers[i]
            print("SOURCE REG: ", source_registers[i])
            if cur_src_reg == rt:
                print("A DELAY WILL BE REQUIRED FOR LW")
                pipe_delays[0] += 1

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

    return [data_mem, reg_arr, pc, num_multicycle_instr, pipe_delays, lw_addr]


# Give cpu_design a value of 0 for Multi-Cycle or 1 for Pipelined
def simulator(instr_mem_file_name):
    # Use the file name to create an array of instructions
    instr_mem_file = open(instr_mem_file_name, "r")
    instr_mem = file_to_array(instr_mem_file)
    reg_arr = [0, 0, 0, 0, 0, 0, 0, 0]  # Use an register for $0 - $7 ($0 will not change)
    data_mem = [0] * 1023  # Create a data memory array
    pc = 0
    index = 0
    mc_hex = instr_mem[pc]
    mc_hex_prev = "0xffffffff"
    mc_hex_next = "0xffffffff"
    num_multicycle_instr = [0, 0, 0]    # Number of 3, 4, and 5 cycle CPU instructions, respectively
    dic = 0     # Dynamic Instruction Count
    pipe_delays = [0, 0]    # Number of Data Hazards and Control Hazards, respectively
    addr_mem = []

    while mc_hex != "0x1000FFFF" or mc_hex != "0x1000ffff":
        if mc_hex == "0x1000ffff":
            dic += 1
            num_multicycle_instr[0] += 1
            break

        if index == 0:
            mc_hex_prev = "0xffffffff"
            mc_hex_next = instr_mem[index + 1]
        elif index == (len(instr_mem) - 2):
            mc_hex_prev = instr_mem[index - 1]
            mc_hex_next = "0xffffffff"
        else:
            mc_hex_prev = instr_mem[index - 1]
            mc_hex_next = instr_mem[index + 1]
        data_set = execute_operation(mc_hex, data_mem, reg_arr, pc, num_multicycle_instr, pipe_delays, mc_hex_prev, mc_hex_next)
        data_mem = data_set[0]
        reg_arr = data_set[1]
        pc = data_set[2]
        num_multicycle_instr = data_set[3]
        pipe_delays = data_set[4]
        lw_addr_index = data_set[5]
        if lw_addr_index != 999999999:
            addr_mem.append(data_set[5])

        print("INDEX:          ", index)
        print("CURR INSTRUCTION", mc_hex)
        print("PREV INSTRUCTION", mc_hex_prev)
        print("NEXT INSTRUCTION", mc_hex_next)

        print_output(reg_arr, pc)
        print("Data Mem:", data_mem[0:10], "\n")
        index = int(pc / 4)
        mc_hex = instr_mem[index]
        dic += 1

    num_3_cycle = num_multicycle_instr[0]
    num_4_cycle = num_multicycle_instr[1]
    num_5_cycle = num_multicycle_instr[2]
    multi_cycle_count = (3 * num_3_cycle) + (4 * num_4_cycle) + (5 * num_5_cycle)
    print("SINGLE-CYLCLE CPU INFORMATION:")
    print("DIC/Number  of Cycles   ", dic)
    print("\n")

    print("MULTI-CYLCLE CPU INFORMATION:")
    print("Num of 3 Cycle Instructions: ", num_3_cycle)
    print("Num of 4 Cycle Instructions: ", num_4_cycle)
    print("Num of 5 Cycle Instructions: ", num_5_cycle)
    print("Total Number of Cycles:      ", multi_cycle_count)
    print("\n")

    data_haz_delays = pipe_delays[0]
    ctrl_haz_delays = pipe_delays[1]
    pipeline_cycle_count = dic + 4 + data_haz_delays + ctrl_haz_delays
    print("PIPELINED CPU INFORMATION:")
    print("Num of Data Hazard Delays: ", data_haz_delays)
    print("Num of Ctrl Hazard Delays: ", ctrl_haz_delays)
    print("Total Number of Cycles:    ", pipeline_cycle_count)

    cache_sim(addr_mem)

simulator("A1.txt")
# simulator("A2.txt")
# simulator("B1.txt")
# simulator("B2.txt")
# simulator("i_mem.txt")
