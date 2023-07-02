from functions import *
import sys


def main() -> int:
    # 命令输入
    command_parameters = []
    for i in sys.argv[1:]:
        command_parameters.append(i)
    # 先解析
    print(command_parameters)
    return 0


if __name__ == '__main__':
    main()
