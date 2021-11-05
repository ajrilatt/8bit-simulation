# Adam Rilatt
# 02 March 2021
# 8-Bit ToyLang Assembler

import sys

TOYLANG_BIN_EXT = 'tlbin'

#TODO: move to config file
TOYLANG_ASM_EXT = 'tlasm'

#TODO: move to config file
TOYLANG_COMMENT = '//'

#TODO: move to config file
TOYLANG_VAL_WIDTH = 8

#TODO: move to config file
TOYLANG_ADDR_WIDTH = 5

#TODO: move to config file
TOYLANG_INSTRUCT_WIDTH = 5

#TODO: move to config file
TOYLANG_MEM_SIZE = 32


'''
Input:  an integer number to convert to binary, and a binary number width.
Output: a string of 1s and 0s of the specified width, representing the input value.
'''
def bin_convert(val, width = 8):
    bin_val = str(bin(val)).replace('0b', '')
    return '0' * (width - len(bin_val)) + bin_val


INSTRUCTS = {
    'NOP' : {'bin' : bin_convert(0,  TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'LDA' : {'bin' : bin_convert(1,  TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : True },
    'LDR' : {'bin' : bin_convert(2,  TOYLANG_INSTRUCT_WIDTH), 'addr' : True,  'val' : False},
    'STA' : {'bin' : bin_convert(3,  TOYLANG_INSTRUCT_WIDTH), 'addr' : True,  'val' : False},
    'STB' : {'bin' : bin_convert(4,  TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'ADD' : {'bin' : bin_convert(5,  TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'AND' : {'bin' : bin_convert(6,  TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'ORA' : {'bin' : bin_convert(7,  TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'XRA' : {'bin' : bin_convert(8,  TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'NTA' : {'bin' : bin_convert(9,  TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'BSL' : {'bin' : bin_convert(10, TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'BSR' : {'bin' : bin_convert(11, TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'ROL' : {'bin' : bin_convert(12, TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
    'JMP' : {'bin' : bin_convert(16, TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : True },
    'JMZ' : {'bin' : bin_convert(17, TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : True },
    'HLT' : {'bin' : bin_convert(31, TOYLANG_INSTRUCT_WIDTH), 'addr' : False, 'val' : False},
}


'''
Input:  a list of strings elements representing lines of ToyLang assembly.
Output: a list of string elements representing the translations of the input
        elements into valid machine code for the ToyLang machine.
'''
def translate(tl_asm):

    # where machine code will be stored as it is generated. returned by function
    assembled = []

    # the current program line number
    prog_count = 0

    # maps register names to binary addresses. error should be thrown if
    # TOYLANG_MEM_SIZE is exceeded by num_registers.
    registers = {}
    num_registers = 0

    for instruction in tl_asm:

        # looks strange, but removes duplicate spaces (spaced tabs, etc) as
        # well as separating each token of the instruction
        instruct_parts = ' '.join(instruction.split(' ')).split()

        # eliminate inline comments
        instruct_parts_len = len(instruct_parts)

        for i, part in enumerate(instruct_parts):
            if part[:2] == TOYLANG_COMMENT:
                instruct_parts_len = i
                break

        print(instruct_parts)
        instruct_parts = instruct_parts[:instruct_parts_len]

        # single-line comment and empty line detection
        if instruct_parts_len == 0 or instruction == '':
            continue

        # valid assembly command check
        try:
            instruct_info = INSTRUCTS[instruct_parts[0]]
        except KeyError as e:
            raise ValueError(f"{prog_count}: '{instruction}' is not a valid assembly instruction.")

        # arguments length check
        expected_arg_len = 1 + instruct_info['addr'] + instruct_info['val']
        if len(instruct_parts) != expected_arg_len:
            raise ValueError(f"{prog_count}: Bad argument count for {instruction}, expected {expected_arg_len - 1}.")

        # register... registration!
        if instruct_info['addr']:

            if instruct_parts[1] not in registers.keys():

                num_registers += 1

                # detect memory full condition (1 var per address)
                if num_registers > TOYLANG_MEM_SIZE:
                    raise ValueError(f"{prog_count}: Too many variables.")

                # add new variable-address mapping
                registers[instruct_parts[1]] = bin_convert(num_registers, width = TOYLANG_ADDR_WIDTH)

        # saving full instruction
        opcode  = instruct_info['bin']

        address = (registers[instruct_parts[1]] if instruct_info['addr']
                                else bin_convert(0, width = TOYLANG_ADDR_WIDTH))

        value   = bin_convert(int(instruct_parts[-1]) if instruct_info['val'] else 0,
                                                           width = TOYLANG_VAL_WIDTH)

        assembled.append(' '.join((opcode, address, value)) + '\n')

        prog_count += 1

    # assembly finished
    return assembled


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: python toylang_asm.py [filepath/target.{TOYLANG_ASM_EXT}]")
        sys.exit(1)

    inputfile = sys.argv[1]

    if inputfile[-(len(TOYLANG_ASM_EXT) + 1):] != '.' + TOYLANG_ASM_EXT:
        print(f"Input file is not a .{TOYLANG_ASM_EXT} file.")
        sys.exit(1)

    # file read process
    try:

        with open(inputfile, 'r') as f:
            tl_asm = [l.replace('\n', '').strip() for l in f.readlines()]

    except FileNotFoundError as e:

        print(f"File {inputfile} not found. Confirm your filepath.")
        sys.exit(1)

    # translation and writing to machine code file
    outputfile = inputfile.replace(TOYLANG_ASM_EXT, TOYLANG_BIN_EXT)
    with open(outputfile, 'w') as f:

        try:

            machinecode = translate(tl_asm)

        except ValueError as e:
            print(f"An error occured on line {e}")
            sys.exit(1)

        for line in machinecode:
            f.write(line)

    print(f"Saved to {outputfile}.")
