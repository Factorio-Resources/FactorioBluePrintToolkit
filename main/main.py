# -*- coding: utf-8 -*-
from functions import *
import fire


class Command(object):
    def undump(self, i, o):
        """
        Undump Factorio blueprint & blueprint book str to json
        """
        i = str(i)
        o = str(o)
        if not os.path.exists(i):
            return "\033[91mERROR: 未找到输入文件\033[0m"
        if not os.path.isfile(i):
            return "\033[91mERROR: 输入目标非文件\033[0m"
        with open(i, 'r', encoding='utf-8') as f:
            data = f.read()
        # noinspection PyBroadException
        try:
            data = undump(data)
        except Exception:
            return f"\033[91mERROR: 蓝图字符串错误\033[0m"
        # noinspection PyBroadException
        try:
            data = json.dumps(
                json.loads(data), indent=4, ensure_ascii=False
            )
            with open(o, 'w', encoding='utf-8') as f:
                f.write(data)
        except Exception as e:
            return f'\033[91mERROR: 保存json的时候出现错误: {e}\033[0m'
        return 'Finish'

    def dump(self, i, o):
        """
        Dump Factorio blueprint & blueprint book json to blueprint str
        """
        i = str(i)
        o = str(o)
        if not os.path.exists(i):
            return "\033[91mERROR: 未找到输入文件\033[0m"
        if not os.path.isfile(i):
            return "\033[91mERROR: 输入目标非文件\033[0m"
        with open(i, 'r', encoding='utf-8') as f:
            data = f.read()
        # noinspection PyBroadException
        try:
            data = dump(json.loads(data))
        except Exception:
            return f"\033[91mERROR: 蓝图json错误\033[0m"
        # noinspection PyBroadException
        try:
            with open(o, 'w', encoding='utf-8') as f:
                f.write(data)
        except Exception as e:
            return f'\033[91mERROR: 保存蓝图字符串时出现错误: {e}\033[0m'
        return 'Finish'

    def undump_blueprintBook_to_files(self, i, o):
        """
        undump Factorio blueprint book to blueprint files & folder
        """
        i = str(i)
        o = str(o)
        if not os.path.exists(i):
            return "\033[91mERROR: 未找到输入文件\033[0m"
        if not os.path.isfile(i):
            return "\033[91mERROR: 输入目标非文件\033[0m"
        with open(i, 'r', encoding='utf-8') as f:
            data = f.read()
        if not os.path.exists(o):
            return "\033[91mERROR: 未找到输出文件夹\033[0m"
        if not os.path.isdir(o):
            return "\033[91mERROR: 输出目标非文件夹\033[0m"
        # noinspection PyBroadException
        try:
            data = undump(data)
            recursively_undump_the_blueprint_book_into_files(data, o)
        except KeyError:
            return f'\033[91mERROR: 该文件不是蓝图书\033[0m'
        except Exception as e:
            return f'\033[91mERROR: 蓝图字符串错误: {e}\033[0m'
        return 'Finish'

    def dump_blueprintFolder_to_blueprintBook(self, i, o):
        """
        dump the folder and blueprint into a blue book
        """
        if not os.path.exists(i):
            return "\033[91mERROR: 未找到输入文件夹\033[0m"
        if not os.path.isdir(i):
            return "\033[91mERROR: 输入目标非文件夹\033[0m"
        # noinspection PyBroadException
        try:
            data = recursively_dump_the_blueprint_book_into_files(i)
        except Exception as e:
            return f'\033[91mERROR: 目标文件夹内部有错误的蓝图: \n{e}\033[0m'
        # noinspection PyBroadException
        try:
            data = dump(data)
        except Exception as e:
            return f"\033[91mERROR: {e}\033[0m"
        try:
            with open(o, 'w', encoding='utf-8') as f:
                f.write(data)
        except Exception as e:
            return f'\033[91mERROR: 保存蓝图字符串时出现错误: {e}\033[0m'
        return 'Finish'


if __name__ == '__main__':
    fire.Fire(Command)
