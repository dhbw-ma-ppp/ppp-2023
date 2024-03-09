from matplotlib import pyplot as plt
import pathlib
import numpy as np
import Int_Computeromputer

output = []
matrix = np.zeros([23, 43])
ball_pos = 0
paddle_pos = 0
score = 0
first_frame = True


def read_input_file(file_name):
    with open(file_name, "r") as input_file:
        input_list = []
        for line in input_file.readlines():
            line.strip()
            input_list.append(int(line))
        input_list[0] = 2
    return input_list


def insert_list(value):
    output.append(value)


def insert_matrix(matrix_input):
    global ball_pos
    global paddle_pos
    for index in range(0, len(matrix_input), 3):
        x, y, entity = matrix_input[index], matrix_input[index + 1], matrix_input[index + 2]
        if entity == 4:
            ball_pos = x
        elif entity == 3:
            paddle_pos = x
        elif x == -1:
            global score
            score = entity
            continue
        matrix[y, x] = entity


def control_paddle():
    global first_frame
    insert_matrix(output)
    plt.imshow(matrix, cmap="rainbow")
    if first_frame:
        plt.show(block=False)
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


def main():
    input_list = read_input_file("breakout_commands.txt")
    computer_test = Int_Computeromputer.IntComputer(control_paddle, insert_list)
    computer_test.run(input_list)
    insert_matrix(output)
    print(score)


main()
