    

def get_refs(commands, instruction_pointer):
    """gets references to relevant entrys

    Args:
        commands (list): list in format: [opcode, first_ref, second_ref, save_ref]
        currentPos (number): starting pos in list_of_nums

    Returns:
        tuple: (first_ref, second_ref, pos_to_write_to)
    """
    first_Ref = list_of_nums[current_pos + 1]
    second_ref = list_of_nums[current_pos + 2]
    pos_to_write_to = list_of_nums[current_pos + 3]
    return (first_Ref, second_ref, pos_to_write_to)
