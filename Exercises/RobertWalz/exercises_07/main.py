from computer import Computer
import numpy as np


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


# memory = {key: element for (key, element) in enumerate(commands)}

def render(data):
    formatted_data = np.array(data).reshape(int(len(data)/3), 3)
    print(formatted_data)

def main():
    output_stream = []

    data = get_data()
    computer_instance = Computer(data, output_stream)
    result = computer_instance.run()
    render(output_stream)
    print(f"\nFinished execution with code: {result}")


main()



    