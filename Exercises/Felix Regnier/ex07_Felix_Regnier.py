import computer_atreju
from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path

fig, ax = plt.subplots()
ax.set_axis_off()

output_collector_data = []
breakout_arr = np.zeros((23,43), dtype=int)
breakout_path = Path(__file__).parent.parent.parent / 'data' / 'breakout_commands.txt'
command_arr = []
with open(breakout_path, 'r') as input_file:
    while (input_line := input_file.readline()) != '':
        command_arr.append(int(input_line))

  
def input_setter():
    pass

def output_collector(output_value) -> None:
    output_collector_data.append(output_value)

computer1 = computer_atreju.IntComputer(input_setter, output_collector)
computer1.run(command_arr)


#def update_world():
for index in range(0,len(output_collector_data),3):
    breakout_arr[output_collector_data[index+1]][output_collector_data[index]] = output_collector_data[index+2]
#        if output_collector_data[index+2] == 3:
#            paddle_x = output_collector_data[index]
#        elif output_collector_data[index+2] == 4:
#            ball_x = output_collector_data[index]
#        if output_collector_data[index] < 0:
#            score = output_collector_data[index+2]
 
print(breakout_arr)
plt.imshow(breakout_arr, cmap="rainbow")
plt.pause(10)
plt.draw()