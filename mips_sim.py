print("ECE 366 Project 4: MIPS Simulator")


def file_to_array(file):
    return_array = []
    for line in file:
        return_array.append(line.rstrip())
    return return_array


def simulator(instr_mem_file_name):
    instr_mem_file = open(instr_mem_file_name, "r")
    instr_mem = file_to_array(instr_mem_file)
    print(instr_mem)


simulator("i_mem.txt")