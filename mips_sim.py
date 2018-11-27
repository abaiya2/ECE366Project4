import math

print("ECE 366 Project 4: MIPS Simulator")

# Choose the instruction file name here by uncommenting
# file_name = "A1.txt"
# file_name = "A2.txt"
# file_name = "B1.txt"
file_name = "B2.txt"

# Create the output file which will store simulation details
output_text_file_name = "p4_output_imem_" + file_name
print("OUTPUT FILE NAME: ", output_text_file_name)
output_file = open(output_text_file_name, "w")


# Used to check if the user input values for custom cache
# Is a valid power of 2, to prevent cache issues
def is_power_two(num):
    return ((num & num - 1) == 0) and num != 0


# Used to convert decimal to 2s complement binary
def decimal_to_bin(dec_num):
    if dec_num < 0:
        pos_value = 0 - dec_num
        comp_value = 0b11111111111111111111111111111111 - pos_value + 1
        bin_num = '{0:032b}'.format(comp_value)
        return bin_num
    else:
        bin_num = '{0:032b}'.format(dec_num)
        return bin_num


# Converts 2s complement binary to decimal in 16 bits
def bin_to_decimal(bin_str):
    if bin_str[0] == "1":
        pos_num = int(bin_str, 2)
        all_ones = 0b1111111111111111
        dec_num = all_ones - pos_num + 1
        return 0 - dec_num
    else:
        dec_num = int(bin_str, 2)
        return dec_num


# Converts 2s complement binary to decimal in 32 bits
def bin_to_decimal_32b(bin_str):
    if bin_str[0] == "1":
        pos_num = int(bin_str, 2)
        all_ones = 0b11111111111111111111111111111111
        dec_num = all_ones - pos_num + 1
        return 0 - dec_num
    else:
        dec_num = int(bin_str, 2)
        return dec_num


# Converts hex string to binary string
def hex_to_bin(hex_str):
    return str(bin(int(hex_str, 16))[2:].zfill(32))


# Converts binary number to hex number
def bin_to_hex(bin_num):
    return '0x{0:08X}'.format(int(bin_num, 2))


# Create an array made up of each each line in the given input file
def file_to_array(file):
    return_array = []
    for line in file:
        return_array.append(line[0:10].rstrip())
    return return_array


# Ouputs the PC, and Registers $1-$7
def print_output(reg_arr, pc):
    print("PC: ", str(pc))
    output_file.write("PC: " + str(pc) + "\n")
    for i in range(1, 8):
        print("$" + str(i) + ": ", str(reg_arr[i]))
        output_file.write("$" + str(i) + ": " + str(reg_arr[i]) + "\n")


# Returns the useful source and target registers of a dependent instruction
# which is given by a hex string
def get_dependent_instruction(mc_hex):
    bin_str = hex_to_bin(mc_hex)
    rd = 0
    rt = 0
    rs = 0
    source_registers = []
    target_register = 0
    output = ""
    # R - Type
    if bin_str[0:6] == "000000":
        # *** $rd, $rs, $rt
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        target_register = rd
        source_registers = [rt, rs]
        output = ("*** $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
    # ADDI
    elif bin_str[0:6] == "001000":
        # ADDI $rt, $rs, imm
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        source_registers = [rs]
        target_register  = rt
        output = "ADDI $" + str(rt) + ", $" + str(rs) + ", IMM"
    # BRANCH
    elif bin_str[0:6] == "000100" or bin_str[0:6] == "000101":
        # B** $rs, $rt, imm
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        source_registers = [rt, rs]
        output = "B** $" + str(rs) + ", $" + str(rt) + ", IMM"
    # LW
    elif bin_str[0:6] == "100011":
        # LW $rt, imm($rs)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        source_registers = [rs]
        target_register = rt
        output = "LW $" + str(rt) + ", IMM($" + str(rs) + ")"
    # SW
    elif bin_str[0:6] == "101011":
        # SW $rt, imm($rs)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        source_registers = [rt, rs]
        output = "SW $" + str(rt) + ", IMM($" + str(rs) + ")"
    return [source_registers, target_register, output]


# Function for running the cache sim, with given inputs
# number of words per block, number of ways, number of sets,
# and an address memory array of memory locations that were accessed
def run_cache_sim_config(num_words, num_ways, num_sets, addr_mem):
    hits = 0
    misses = 0
    total = len(addr_mem)
    if num_ways == 1:
        block = []
        # cache = [{"tag": "", "block": []}] * num_sets
        cache = [""] * num_sets
        num_bytes = 4 * num_words
        num_offset_bits = int(math.log(num_bytes, 2))
        num_block_bits = int(math.log(num_sets, 2))
        # print("CACHE", cache)
        print("DIRECTLY MAPPED CACHE")
        print("Number of Words in Block: ", num_words)
        print("Number of Blocks:         ", num_sets)
        output_file.write("DIRECTLY MAPPED CACHE" + "\n")
        output_file.write("Number of Words in Block: " + str(num_words) + "\n")
        output_file.write("Number of Blocks:         " + str(num_sets) + "\n")

        for i in range(0, len(addr_mem)):
            bin_num = decimal_to_bin(addr_mem[i])
            bin_str = str(bin_num)
            most_sig_bits = bin_str[0: 32 - num_block_bits - num_offset_bits]
            block = bin_str[len(most_sig_bits): 32 - num_offset_bits]
            block_index = int(block, 2)

            addr_offset_from_start = (addr_mem[i] - 0x2000) % (num_words * 4)
            block_start = addr_mem[i] - addr_offset_from_start

            # print("ADDR OFFSET", addr_offset_from_start)
            # print("BLOCK START", hex(block_start))

            if cache[block_index] == most_sig_bits:
                print(str(hex(addr_mem[i]) + ": HIT"))
                output_file.write(str(hex(addr_mem[i]) + ": HIT") + "\n")
                print("  -->TAG: " + most_sig_bits)
                output_file.write("  -->TAG: " + most_sig_bits)
                hits = hits + 1
                print("  -->Data was read from BLOCK:", block_index)
                output_file.write("  -->Data was read from BLOCK:" + str(block_index) + "\n")

            else:
                print(str(hex(addr_mem[i]) + ": MISS"))
                output_file.write(str(hex(addr_mem[i]) + ": MISS") + "\n")
                print("  -->TAG: " + most_sig_bits)
                output_file.write("  -->TAG: " + most_sig_bits)
                if not cache[block_index]:
                    print("  -->Valid Bit Changed from 0 to 1")
                    output_file.write("  -->Valid Bit Changed from 0 to 1 for this block \n")
                cache[block_index] = most_sig_bits
                misses = misses + 1
                address_range = str(hex(block_start)) + "-" + str(hex(block_start+num_bytes-1))
                print("  -->Data Addresses: " + address_range + " stored in BLOCK: " + str(block_index))
                output_file.write("  -->Data Addresses: " + address_range + " stored in BLOCK: " + str(block_index) + "\n")

        print("\n")
        output_file.write("\n")
    # Set Associative, including Fully Associative
    else:
        # Number of rows is number of Sets
        # Number of columns is number of ways
        if num_sets == 1:
            print("FULLY ASSOCIATIVE CACHE")
            output_file.write("FULLY ASSOCIATIVE CACHE" + "\n")

        else:
            print("SET ASSOCIATIVE CACHE")
        print("Number of Sets: ", num_sets)
        print("Number of Ways: ", num_ways)
        print("Number of Words in Block: ", num_words)
        print("------Mem Cache Information------")
        output_file.write("SET ASSOCIATIVE CACHE" + "\n")
        output_file.write("Number of Sets: " + str(num_sets) + "\n")
        output_file.write("Number of Ways: " + str(num_ways) + "\n")
        output_file.write("Number of Words in Block: " + str(num_words) + "\n")
        output_file.write("------Mem Cache Information------" + "\n")

        num_bytes = 4 * num_words
        num_offset_bits = int(math.log(num_bytes, 2))
        num_set_bits = int(math.log(num_sets, 2))
        least_recently_used = [list(range(num_ways)) for y in range(num_sets)]
        cache_tags = [["" for x in range(num_ways)] for y in range(num_sets)]
        # print(cache_tags)
        # for i in range(0, len(least_recently_used)):
        #     print(least_recently_used[i])
        for i in range(0, len(addr_mem)):
            bin_num = decimal_to_bin(addr_mem[i])
            bin_str = str(bin_num)
            tag = bin_str[0: 32 - num_set_bits - num_offset_bits]
            set_bin = bin_str[len(tag): 32 - num_offset_bits]
            # print(set_bin)
            set_index = 0
            if set_bin != "":
                set_index = int(set_bin, 2)
            # print("SET INDEX", set_index)

            block_found = False
            block_index = 0
            for j in range(0, num_ways):
                if tag == cache_tags[set_index][j]:
                    block_found = True
                    block_index = j
                    break

            if block_found:
                print(str(hex(addr_mem[i]) + ": HIT"))
                output_file.write(str(hex(addr_mem[i]) + ": HIT") + "\n")
                print("  -->TAG: " + tag)
                output_file.write("  -->TAG: " + tag)
                print("  -->Data was read from BLOCK in SET: " + str(set_index) + " , WAY: " + str(block_index))
                output_file.write("  -->Data was read from BLOCK in SET: " + str(set_index) + " , WAY: " + str(block_index) + "\n")
                hits = hits + 1
            else:
                print(str(hex(addr_mem[i]) + ": MISS"))
                output_file.write(str(hex(addr_mem[i]) + ": MISS") + "\n")
                misses = misses + 1
                print("  -->TAG: " + tag)
                output_file.write("  -->TAG: " + tag)
                # Find index of least recently used block to replace
                current_set = least_recently_used[set_index]
                index_of_lru = current_set.index(min(current_set))
                lru_value = least_recently_used[set_index][index_of_lru]
                least_recently_used[set_index][index_of_lru] = lru_value + num_ways
                if not cache_tags[set_index][index_of_lru]:
                    print("  -->Valid Bit Changed from 0 to 1")
                    output_file.write("  -->Valid Bit Changed from 0 to 1 for this block \n")
                cache_tags[set_index][index_of_lru] = tag
                addr_offset_from_start = (addr_mem[i] - 0x2000) % (num_words * 4)
                block_start = addr_mem[i] - addr_offset_from_start
                address_range = str(hex(block_start)) + "-" + str(hex(block_start+num_bytes-1))
                print("  -->Data Addresses " + address_range + " stored in SET: " + str(set_index) + " , WAY: " + str(index_of_lru))
                output_file.write("  -->Data Addresses " + address_range + " stored in SET: " + str(set_index) + " , WAY: " + str(index_of_lru) + "\n")
        print("\n")
        output_file.write("\n")

    print("Mem Access Count: ", len(addr_mem))
    print("Number of Hits:   ", hits)
    print("Number of Misses: ", misses)
    print("---------------------------------")
    output_file.write("Mem Access Count: " + str(len(addr_mem)) + "\n")
    output_file.write("Number of Hits:   " + str(hits) + "\n")
    output_file.write("Number of Misses: " + str(misses) + "\n")
    output_file.write("---------------------------------")


# Driver function that calls run_cache_sim_config for each of the
# four given cache sim test cases
def cache_sim(addr_mem):
    print("\n")
    output_file.write("\n")
    print("MEMORY ADDRESSES ACCESSED")
    output_file.write("MEMORY ADDRESSES ACCESSED" + "\n")
    for i in range(0, len(addr_mem)):
        hex_num = 0x2000 + (addr_mem[i] * 4)
        addr_mem[i] = hex_num
        print(hex(addr_mem[i]))
        output_file.write(hex(addr_mem[i]) + "\n")
    print("\n")
    output_file.write("\n")
    run_cache_sim_config(4, 1, 2, addr_mem)   #config 3A
    run_cache_sim_config(2, 1, 4, addr_mem)   #config 3B
    run_cache_sim_config(2, 4, 1, addr_mem)   #config 3C
    run_cache_sim_config(2, 2, 4, addr_mem)   #config 3D


# Displays all of the information for the forwarding information
# that prevents delays
def display_forwarding_uses(rd, mc_next, mc_2nd, mc_3rd):
    instr_reg_next = get_dependent_instruction(mc_next)
    instr_reg_2nd = get_dependent_instruction(mc_2nd)
    instr_reg_3rd = get_dependent_instruction(mc_3rd)
    src_reg_next = instr_reg_next[0]
    src_reg_2nd = instr_reg_2nd[0]
    src_reg_3rd = instr_reg_3rd[0]
    output_next = instr_reg_next[2]
    output_2nd = instr_reg_2nd[2]
    output_3rd = instr_reg_3rd[2]
    print("(1st Refers to the next instruction, 2ND to the instruction after that, etc...)")
    output_file.write("(1st Refers to the next instruction, 2ND to the instruction after that, etc...)" + "\n")
    for i in range(0, len(src_reg_next)):
        if rd == src_reg_next[i]:
            print("1ST INSTR: " + output_next)
            output_file.write("1ST INSTR: " + output_next + "\n")
            print("1st: The next instruction has a HAZARD solved with forwarding")
            output_file.write("1st: The next instruction has a HAZARD solved with forwarding" + "\n")
            break
    for i in range(0, len(src_reg_2nd)):
        if rd == src_reg_2nd[i] and rd != instr_reg_next[1]:
            print("2ND INSTR : " + output_2nd)
            output_file.write("2ND INSTR : " + output_2nd + "\n")
            print("2nd: The instruction after the next has a HAZARD solved with forwarding")
            output_file.write("2nd: The instruction after the next has a HAZARD solved with forwarding" + "\n")
            break
        elif rd == src_reg_2nd[i] and rd == instr_reg_next[1]:
            print("1ST INSTR : " + output_next)
            output_file.write("1ST INSTR : " + output_next + "\n")
            print("2ND INSTR : " + output_2nd)
            output_file.write("2ND INSTR : " + output_2nd + "\n")
            print("2nd: Current target reg is used as a target for next instruction and"
                  "\n   operand for the instruction below that")
            output_file.write("2nd: Current target reg is used as a target for next instruction and"
                  "\n   operand for the instruction below that" + "\n")

    for i in range(0, len(src_reg_3rd)):
        if rd == src_reg_3rd[i] and rd != instr_reg_2nd[1]:
            print("3RD INSTR : " + output_3rd)
            output_file.write("3RD INSTR : " + output_3rd)
            print("3rd: The instruction 3 counts below this instruction has a HAZARD solved with forwarding")
            output_file.write("3rd: The instruction 3 counts below this instruction has a HAZARD solved with forwarding" + "\n")
            break
        elif rd == src_reg_3rd[i] and rd == instr_reg_2nd[1]:
            print("2ND INSTR : " + output_2nd)
            print("3RD INSTR : " + output_3rd)
            print(
                "3rd: Register used as target in this instruction is used as target in the 3rd, and operand in the 4th")
            output_file.write("2ND INSTR : " + output_2nd + "\n")
            output_file.write("3RD INSTR : " + output_3rd + "\n")
            output_file.write(
                "3rd: Register used as target in this instruction is used as target in the 3rd, and operand in the 4th" + "\n")


# Function that is run for each instruction in the instruction memory
def execute_operation(mc_hex, data_mem, reg_arr, pc, num_multicycle_instr, pipe_delays, adjacent_mc_codes):
    mc_prev = adjacent_mc_codes[0]
    mc_next = adjacent_mc_codes[1]
    mc_2nd = adjacent_mc_codes[2]
    mc_3rd = adjacent_mc_codes[3]

    bin_str = hex_to_bin(mc_hex)
    lw_addr = 999999999
    # ADD
    if bin_str[0:6] == "000000" and bin_str[21:32] == "00000100000":
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        print("ADD $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        output_file.write("ADD $" + str(rd) + ", $" + str(rs) + ", $" + str(rt) + "\n")
        reg_arr[rd] = reg_arr[rs] + reg_arr[rt]
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
        output_file.write("Multi-Cycle Count: 4 Cycles" + "\n")

        display_forwarding_uses(rd, mc_next, mc_2nd, mc_3rd)
    # SUB
    elif bin_str[0:6] == "000000" and bin_str[21:32] == "00000100010":
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        print("SUB $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        output_file.write("SUB $" + str(rd) + ", $" + str(rs) + ", $" + str(rt) + "\n")
        reg_arr[rd] = reg_arr[rs] - reg_arr[rt]
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
        output_file.write("Multi-Cycle Count: 4 Cycles" + "\n")
        display_forwarding_uses(rd, mc_next, mc_2nd, mc_3rd)
    # XOR
    elif bin_str[0:6] == "000000" and bin_str[26:32] == "100110":
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        print("XOR $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        output_file.write("XOR $" + str(rd) + ", $" + str(rs) + ", $" + str(rt) + "\n")
        reg_arr[rd] = reg_arr[rt] ^ reg_arr[rs]
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
        output_file.write("Multi-Cycle Count: 4 Cycles" + "\n")
        display_forwarding_uses(rd, mc_next, mc_2nd, mc_3rd)
    # ADDI
    elif bin_str[0:6] == "001000":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("ADDI $" + str(rt) + ", $" + str(rs) + ", " + str(imm))
        output_file.write("ADDI $" + str(rt) + ", $" + str(rs) + ", " + str(imm) + "\n")
        reg_arr[rt] = reg_arr[rs] + imm
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
        output_file.write("Multi-Cycle Count: 4 Cycles" + "\n")
        display_forwarding_uses(rt, mc_next, mc_2nd, mc_3rd)
    # BEQ
    elif bin_str[0:6] == "000100":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("BEQ $" + str(rs) + ", $" + str(rt) + ", " + str(imm))
        output_file.write("BEQ $" + str(rs) + ", $" + str(rt) + ", " + str(imm) + "\n")
        if reg_arr[rt] == reg_arr[rs]:
            pc += (imm * 4)
            print("A STALL IS NEEDED FOR BEQ TO FLUSH THE NEXT INSTR")
            output_file.write("A STALL IS NEEDED FOR BEQ TO FLUSH THE NEXT INSTR" + "\n")
            pipe_delays[1] += 1
        num_multicycle_instr[0] += 1
        print("Multi-Cycle Count: 3 Cycles")
        output_file.write("Multi-Cycle Count: 3 Cycles" + "\n")
        data_registers = get_dependent_instruction(mc_prev)
        target_register = data_registers[1]
        if target_register == rt or target_register == rs:
            print("A STALL IS NEEDED FOR BEQ, WHICH NEEDS AN OPERAND")
            output_file.write("A STALL IS NEEDED FOR BEQ, WHICH NEEDS AN OPERAND" + "\n")
            pipe_delays[0] += 1
    # BNE
    elif bin_str[0:6] == "000101":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("BNE $" + str(rt) + ", $" + str(rs) + ", " + str(imm))
        output_file.write("BNE $" + str(rt) + ", $" + str(rs) + ", " + str(imm) + "\n")
        if reg_arr[rt] != reg_arr[rs]:
            pc += (imm * 4)
            print("A STALL IS NEEDED FOR BNE TO FLUSH THE NEXT INSTR")
            output_file.write("A STALL IS NEEDED FOR BNE TO FLUSH THE NEXT INSTR" + "\n")
            pipe_delays[1] += 1
        num_multicycle_instr[0] += 1
        print("Multi-Cycle Count: 3 Cycles")
        output_file.write("Multi-Cycle Count: 3 Cycles" + "\n")
        data_registers = get_dependent_instruction(mc_prev)
        target_register = data_registers[1]
        if target_register == rt or target_register == rs:
            print("A STALL IS NEEDED FOR BNE, WHICH NEEDS AN OPERAND")
            output_file.write("A STALL IS NEEDED FOR BNE, WHICH NEEDS AN OPERAND" + "\n")
            pipe_delays[0] += 1
    # SLT
    elif bin_str[0:6] == "000000" and bin_str[21:32] == "00000101010":
        rd = int(bin_str[16:21], 2)
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        print("SLT $" + str(rd) + ", $" + str(rs) + ", $" + str(rt))
        output_file.write("SLT $" + str(rd) + ", $" + str(rs) + ", $" + str(rt) + "\n")
        if reg_arr[rs] < reg_arr[rt]:
            reg_arr[rd] = 1
        else:
            reg_arr[rd] = 0
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
        output_file.write("Multi-Cycle Count: 4 Cycles" + "\n")
        display_forwarding_uses(rd, mc_next, mc_2nd, mc_3rd)
    # LW
    elif bin_str[0:6] == "100011":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("LW $" + str(rt) + ", " + str(imm) + "($" + str(rs) + ")")
        output_file.write("LW $" + str(rt) + ", " + str(imm) + "($" + str(rs) + ")" + "\n")

        d_mem_index = int((reg_arr[rs] - 0x2000 + imm) / 4)
        d_mem_value = data_mem[d_mem_index]
        print("MEM INDEX FOR LW", d_mem_index)
        output_file.write("MEM INDEX FOR LW" + str(d_mem_index) + "\n")
        reg_arr[rt] = d_mem_value
        num_multicycle_instr[2] += 1
        print("Multi-Cycle Count: 5 Cycles")
        output_file.write("Multi-Cycle Count: 5 Cycles" + "\n")
        lw_addr= d_mem_index
        data_registers = get_dependent_instruction(mc_next)
        source_registers = data_registers[0]
        for i in range(0, len(source_registers)):
            cur_src_reg = source_registers[i]
            print("SOURCE REG: ", source_registers[i])
            output_file.write("SOURCE REG: " + str(source_registers[i]) + "\n")
            if cur_src_reg == rt:
                print("A DELAY WILL BE REQUIRED FOR LW")
                output_file.write("A DELAY WILL BE REQUIRED FOR LW" + "\n")
                pipe_delays[0] += 1
    # SW
    elif bin_str[0:6] == "101011":
        rt = int(bin_str[11:16], 2)
        rs = int(bin_str[6:11], 2)
        imm_bin = bin_str[16:32]
        imm = bin_to_decimal(imm_bin)
        print("SW $" + str(rt) + ", " + str(imm) + "($" + str(rs) + ")")
        output_file.write("SW $" + str(rt) + ", " + str(imm) + "($" + str(rs) + ")" + "\n")
        d_mem_index = int((reg_arr[rs] - 0x2000 + imm) / 4)
        data_mem[d_mem_index] = reg_arr[rt]
        num_multicycle_instr[1] += 1
        print("Multi-Cycle Count: 4 Cycles")
        output_file.write("Multi-Cycle Count: 4 Cycles" + "\n")
    pc += 4

    return [data_mem, reg_arr, pc, num_multicycle_instr, pipe_delays, lw_addr]


# Function that wraps the simulation, by taking in the file name of the instruction
# memory text file
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
        # Checks breaking condition, which is the last dead loop
        if mc_hex == "0x1000ffff":
            dic += 1
            num_multicycle_instr[0] += 1
            break

        mc_hex_2nd_next = "0xffffffff"
        mc_hex_3rd_next = "0xffffffff"

        # Gets the next few instructions, which can be
        # checked for hazards and dependencies
        if index == 0:
            mc_hex_prev = "0xffffffff"
            mc_hex_next = instr_mem[index + 1]
            mc_hex_2nd_next = instr_mem[index + 2]
            mc_hex_3rd_next = instr_mem[index + 3]
        elif index == (len(instr_mem) - 2):
            mc_hex_prev = instr_mem[index - 1]
            mc_hex_next = "0xffffffff"
            mc_hex_2nd_next = "0xffffffff"
            mc_hex_3rd_next = "0xffffffff"
        elif index == (len(instr_mem) - 3):
            mc_hex_prev = instr_mem[index - 1]
            mc_hex_next = instr_mem[index + 1]
            mc_hex_2nd_next = "0xffffffff"
            mc_hex_3rd_next = "0xffffffff"
        elif index == (len(instr_mem) - 4):
            mc_hex_prev = instr_mem[index - 1]
            mc_hex_next = instr_mem[index + 1]
            mc_hex_2nd_next = instr_mem[index + 2]
            mc_hex_3rd_next = "0xffffffff"
        else:
            mc_hex_prev = instr_mem[index - 1]
            mc_hex_next = instr_mem[index + 1]
            mc_hex_2nd_next = instr_mem[index + 2]
            mc_hex_3rd_next = instr_mem[index + 3]

        adjacent_mc_codes = [mc_hex_prev, mc_hex_next, mc_hex_2nd_next, mc_hex_3rd_next]
        data_set = execute_operation(mc_hex, data_mem, reg_arr, pc, num_multicycle_instr, pipe_delays, adjacent_mc_codes)
        data_mem = data_set[0]
        reg_arr = data_set[1]
        pc = data_set[2]
        num_multicycle_instr = data_set[3]
        pipe_delays = data_set[4]
        lw_addr_index = data_set[5]
        # Gets the address of any potential lw instruction
        if lw_addr_index != 999999999:
            addr_mem.append(data_set[5])
        # print("INDEX:          ", index)
        # print("CURR INSTRUCTION", mc_hex)
        # print("PREV INSTRUCTION", mc_hex_prev)
        # print("NEXT INSTRUCTION", mc_hex_next)
        print_output(reg_arr, pc)
        #output_file.write(reg_arr, pc)
        print("----------NEXT INSTRUCTION----------")
        output_file.write("----------NEXT INSTRUCTION----------" + "\n")
        index = int(pc / 4)
        mc_hex = instr_mem[index]
        dic += 1

    # Final output
    print("\nFinal Output of Registers")
    output_file.write("\nFinal Output of Registers" + "\n")
    print(instr_mem_file_name)
    output_file.write(instr_mem_file_name + "\n")
    print_output(reg_arr, pc)
    #output_file.write(reg_arr, pc)

    print("---------CPU INFORMATION----------")
    output_file.write("---------CPU INFORMATION----------" + "\n")
    num_3_cycle = num_multicycle_instr[0]
    num_4_cycle = num_multicycle_instr[1]
    num_5_cycle = num_multicycle_instr[2]
    multi_cycle_count = (3 * num_3_cycle) + (4 * num_4_cycle) + (5 * num_5_cycle)
    print("SINGLE-CYCLE CPU INFORMATION:")
    print("DIC/Number  of Cycles   ", dic)
    print("----------------------------------")

    print("MULTI-CYCLE CPU INFORMATION:")
    print("Num of 3 Cycle Instructions: ", num_3_cycle)
    print("Num of 4 Cycle Instructions: ", num_4_cycle)
    print("Num of 5 Cycle Instructions: ", num_5_cycle)
    print("Total Number of Cycles:      ", multi_cycle_count)
    print("----------------------------------")

    output_file.write("SINGLE-CYCLE CPU INFORMATION:" + "\n")
    output_file.write("DIC/Number  of Cycles   " + str(dic) + "\n")
    output_file.write("----------------------------------" + "\n")

    output_file.write("MULTI-CYCLE CPU INFORMATION:" + "\n")
    output_file.write("Num of 3 Cycle Instructions: " + str(num_3_cycle) + "\n")
    output_file.write("Num of 4 Cycle Instructions: " + str(num_4_cycle) + "\n")
    output_file.write("Num of 5 Cycle Instructions: " + str(num_5_cycle) + "\n")
    output_file.write("Total Number of Cycles:      " + str(multi_cycle_count) + "\n")
    output_file.write("----------------------------------" + "\n")

    data_haz_delays = pipe_delays[0]
    ctrl_haz_delays = pipe_delays[1]
    pipeline_cycle_count = dic + 4 + data_haz_delays + ctrl_haz_delays
    print("PIPELINED CPU INFORMATION:")
    print("Num of Data Hazard Delays: ", data_haz_delays)
    print("Num of Ctrl Hazard Delays: ", ctrl_haz_delays)
    print("Total Number of Cycles:    ", pipeline_cycle_count)

    output_file.write("PIPELINED CPU INFORMATION:" + "\n")
    output_file.write("Num of Data Hazard Delays: " + str(data_haz_delays) + "\n")
    output_file.write("Num of Ctrl Hazard Delays: " + str(ctrl_haz_delays) + "\n")
    output_file.write("Total Number of Cycles:    " + str(pipeline_cycle_count) + "\n")

    # Allows the user to enter custom sizes for a memory cache config
    cache_sim(addr_mem)
    block_size = int(input("Enter the block size:   "))
    num_ways = int(input("Enter the number of ways: "))
    num_sets = int(input("Enter the number of sets:  "))

    # Ensures values given are in powers
    if not is_power_two(block_size):
        print("Entered block size is not a power of 2. Defaulting to 2 words")
        block_size = 2
    if not is_power_two(num_ways):
        print("Entered number of ways is not a power of 2. Defaulting to 2 ways")
        num_ways = 2
    if not is_power_two(num_sets):
        print("Entered number of sets is not a power of 2. Defaulting to 2 sets")
        num_sets = 2

    # Runs the cache sim for custom user input sizes
    run_cache_sim_config(block_size, num_ways, num_sets, addr_mem)


# Runs the main simulator, which encapsulates everything in this file
simulator(file_name)
output_file.close()
