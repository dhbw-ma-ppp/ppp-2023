from matplotlib import pyplot as plt
import pathlib
import numpy as np
import computer

output = []
matrix = np.zeros([23,43])
ball_pos = 0
paddle_pos = 0
score = 0
first_frame = True


"""root_dir = pathlib.Path(__file__).parent.parent.parent
command_file = root_dir / "data" / "breakout_commands.txt"

with open(command_file) as input_file:
    data_input_list = list()
    for line in input_file.readlines():
        line.strip()
        data_input_list.append(int(line))
    data_input_list[0] = 2"""



with open("breakout_commands.txt", "r") as input_file:
    input_list = list()
    for line in input_file.readlines():
        line.strip()
        input_list.append(int(line))
    input_list[0] = 2


def insert_list(value):
    output.append(value)


def insert_matrix(matrix_input):
    global ball_pos
    global paddle_pos
    for index in range(0,len(matrix_input),3):
        x, y, entity = matrix_input[index], matrix_input[index+1], matrix_input[index+2]
        if entity == 4:
            ball_pos = x
        elif entity == 3:
            paddle_pos = x
        elif x == -1:
            global score
            score = entity
            continue
        matrix[y,x] = entity


def control_paddle():
    global first_frame
    insert_matrix(output)
    plt.imshow(matrix, cmap="rainbow")
    if first_frame:
        plt.show(block  = False)
        first_frame = False
    else:
        plt.draw()
    plt.pause(0.000001)

    if ball_pos < paddle_pos:
        return -1
    elif ball_pos > paddle_pos:
        return 1
    else:
        return 0


computer_test = computer.IntComputer(control_paddle, insert_list)

computer_test.run(input_list)
insert_matrix(output)
print(score)
