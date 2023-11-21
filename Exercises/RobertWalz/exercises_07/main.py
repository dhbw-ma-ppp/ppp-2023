from computer import Computer
import numpy as np
import matplotlib.pyplot as plt


def get_data() -> dict[int, int]:
    try:
        with open("data/breakout_commands.txt") as file:
            data = {key: int(line) for key, line in enumerate(file.readlines())}
    except FileNotFoundError:
        print("Please change your cwd to the base directory of the repository!")
        exit(0)
    except ValueError:
        print("The data has to be integer only!")
        exit(0)
    return data


def render(data):
    formatted_data = np.array(data).reshape(int(len(data) / 3), 3)
    indices = np.argsort(formatted_data[:, 2])
    temp = formatted_data[indices]
    pixel = np.array_split(temp, np.where(np.diff(temp[:, 2]) != 0)[0] + 1)

    # 0: empty tile
    plt.scatter(pixel[0][:, 0], pixel[0][:, 1], c="w", marker="s")
    # 1: wall. walls are indestructible
    plt.scatter(pixel[1][:, 0], pixel[1][:, 1], c="c", marker="s")
    # 2: block. blocks can be destroyed by the ball, marker="s"
    plt.scatter(pixel[2][:, 0], pixel[2][:, 1], c="g", marker="s")
    # 3: paddle. the paddle is indestructible
    plt.scatter(pixel[3][:, 0], pixel[3][:, 1], c="b", marker="s")
    # 4: ball. the ball moves diagonally and bounces off objects
    plt.scatter(pixel[4][:, 0], pixel[4][:, 1], c="r", marker="s")
    
    plt.gca().invert_yaxis() 
     
    plt.show()


def main():
    output_stream = []

    data = get_data()
    computer_instance = Computer(data, output_stream)
    result = computer_instance.run()
    render(output_stream)
    print(f"\nFinished execution with code: {result}")


main()
