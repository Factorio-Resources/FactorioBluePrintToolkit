from functions import *


def main() -> int:
    a = '''0eNqrVkrKKU0tKMrMK4lPys/PVrKqRogUK1lFx+ooZZak5ipZIYR1wQp1lBKTSzLLUuMz81JSK5SsDHSUylKLijPz85SsjCwMTcwtjczNLI0MLIyNamsBfkciqQ==
    '''
    recursively_undump_the_blueprint_book_into_files(undump(a),'../test')
    print(dump(recursively_dump_the_blueprint_book_into_files('../test/未命名蓝图薄')))
    return 0


if __name__ == '__main__':
    main()
