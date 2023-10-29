

def evaluate_opcode(opcode, computer_instance):
    opcode_arr = [int(x) for x in str(opcode)]
    operation_to_perform = int("".join(str(x) for x in opcode_arr[-2:]))
    computer_instance.opcode_map[operation_to_perform]()


def get_refs(commands, instruction_pointer, params_to_get):
    """gets references to a set number of params

    Args:
        commands (list): list in format: [opcode, first_ref, second_ref]
        instruction_pointer (number): starting pos in commands
        params_to_get (number): amount of arg refs to get


    Returns:
        tuple: (first_ref, second_ref, third_ref, ...)
    """

    # TODO: fill list with default 0
    # 0001
    # [0,0,0,1]
    params = commands[instruction_pointer] // 100
    # opcode = str(commands[instruction_pointer])
    # opcode_arr = [int(x) for x in opcode]

    # opcode_arr.reverse()
    
    # while len(opcode_arr) < params_to_get + 2:  #operation_code_length
    #     opcode_arr.append(0)
    
    # #get rid of actual opcode
    # opcode_arr = opcode_arr[2:]
    
    refs = []
    for index in range(0, params_to_get):
        if params % 10:
            refs.append(instruction_pointer + 1 + index)
        else:
            # postion
            refs.append(commands[instruction_pointer + 1 + index])
    
    # for index, opcode in enumerate(opcode_arr):
    #     # fill with 
    #     if opcode:
    #         # immediate mode
    #         refs.append(instruction_pointer + 1 + index)
    #     else:
    #         # position mode
    #         refs.append(instruction_pointer + 1 + index)

    return tuple(refs)
