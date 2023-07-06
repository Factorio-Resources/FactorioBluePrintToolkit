# 这里是具体功能的实现 可以直接进行调用
# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
import json
from zlib import compress, decompress
import os


def undump(undump_str: str) -> str:
    """
    解压异星工场的蓝图文件
    :param undump_str:要解压的字符串
    :return:返回解压完成后的字符串 要自己解析成字典
    """
    return decompress(
        b64decode(undump_str[1:].encode('utf-8'))
    ).decode('utf-8')


def dump(dump_dict: dict) -> str:
    """
    压缩异星工场的蓝图文件
    :param dump_dict: 要压缩的字典
    :return: 压缩好后的蓝图字符串
    """
    return f"0{b64encode(compress(json.dumps(dump_dict, indent=None).encode('utf-8'), level=9)).decode('utf-8')}"


def recursively_undump_the_blueprint_book_into_files(undump_blueprint_book: str, path) -> None:
    """
    递归解压异星工场的蓝图书到文件 会在path创建一个要解压的蓝图书的文件夹
    :param undump_blueprint_book:完成解压的蓝图书json字符串
    :param path:要解压到的路径
    :return:None
    """

    # 重复调用用的,在递归函数中处理for循环创建内容的时候的指令
    def process_item(item, item_type, default_label, folder_path):
        del item['index']
        item[item_type].setdefault("label", default_label)
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']  # 在 Windows 中不能用于文件名的字符
        fullwidth_chars = ['＜', '＞', '：', '＂', '／', '＼', '｜', '？', '＊']  # 对应的全角字符
        for invalid_char, fullwidth_char in zip(invalid_chars, fullwidth_chars):  # 替换无效字符
            item[item_type]['label'] = item[item_type]['label'].replace(invalid_char, fullwidth_char)
        item[item_type]['label'] = item[item_type]['label'].rstrip()  # 删除末尾空格
        if item[item_type]['label'] and item[item_type]['label'][-1] == '.':  # 将末尾的半角 . 替换为全角 ．
            item[item_type]['label'] = item[item_type]['label'][:-1] + '．'

        file_path = os.path.join(folder_path, item[item_type]['label'])
        e = 0
        while os.path.exists(f'{file_path}.txt'):
            e += 1
            file_path = os.path.join(folder_path, f"{item[item_type]['label']}({e})")
        with open(f"{file_path}.txt", 'w', encoding='utf-8') as f:
            f.write(dump(item))

    # 递归用的函数
    def recursive_blueprint_book(blueprint_book: dict, now_path) -> None:
        # blueprint_book 一定是蓝图书 所以直接创建文件夹
        blueprint_book = blueprint_book['blueprint_book']
        blueprint_book.setdefault("label", "未命名蓝图薄")
        # 替换蓝图文件为合法的
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']  # 在 Windows 中不能用于文件名的字符
        fullwidth_chars = ['＜', '＞', '：', '＂', '／', '＼', '｜', '？', '＊']  # 对应的全角字符
        for invalid_char, fullwidth_char in zip(invalid_chars, fullwidth_chars):  # 替换无效字符
            blueprint_book['label'] = blueprint_book['label'].replace(invalid_char, fullwidth_char)
        blueprint_book['label'] = blueprint_book['label'].rstrip()  # 删除末尾空格
        if blueprint_book['label'] and blueprint_book['label'][-1] == '.':  # 将末尾的半角 . 替换为全角 ．
            blueprint_book['label'] = blueprint_book['label'][:-1] + '．'

        folder_name = blueprint_book['label']
        folder_path = os.path.join(now_path, blueprint_book['label'] if 'label' in blueprint_book else '未命名蓝图书')
        i = 0
        while os.path.exists(folder_path):
            i += 1
            folder_path = os.path.join(now_path, f'{folder_name}({i})')
        blueprint_book['label'] = folder_name if i == 0 else f'{folder_name}({i})'
        os.mkdir(folder_path)
        # 创建_intro_蓝图说明文件
        with open(f"{folder_path}/_intro_", 'w', encoding='utf-8') as f:
            f.write(json.dumps({k: v for k, v in blueprint_book.items() if k != 'blueprints' and k != 'label'},
                               ensure_ascii=False, indent=4))
        # 开始遍历
        for i in blueprint_book['blueprints']:
            if 'blueprint_book' in i:
                recursive_blueprint_book(i, folder_path)
            elif 'blueprint' in i:
                process_item(i, 'blueprint', "未命名蓝图", folder_path)
            elif 'upgrade_planner' in i:
                process_item(i, 'upgrade_planner', "未命名绿图", folder_path)
            elif 'deconstruction_planner' in i:
                process_item(i, 'deconstruction_planner', "未命名红图", folder_path)
        return

    undump_blueprint_book = json.loads(undump_blueprint_book)
    recursive_blueprint_book(undump_blueprint_book, path)
    return


def recursively_dump_the_blueprint_book_into_files(path: str) -> dict:
    """
    递归压缩异星工场的蓝图文件夹/文件到蓝图字典
    :param path:要压缩的蓝图文件夹
    :return:压缩好的蓝图字典
    """
    index = 0
    # 先初始化当前的文件夹的蓝图书 然后把return给弄回来
    return_dict = {
        "blueprints": []
    }
    # 判断blueprint-book的其他属性 由于一定是文件夹所以就不管特判
    if os.path.exists(os.path.join(path, '_intro_')) and os.path.getsize(os.path.join(path, '_intro_')) != 0:
        with open(os.path.join(path, '_intro_'), 'r', encoding='utf-8') as f:
            return_dict.update(json.loads(f.read()))
        return_dict.update({"label": os.path.basename(path)})
    else:
        return_dict.update(
            {
                "item": "blueprint-book",
                "active_index": 0,
                "label": os.path.basename(path)
            })
    # 遍历 并且开始递归
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and os.path.basename(item_path) == '_intro_':
            continue  # intro之前加过了 不需要管了
        elif os.path.isdir(item_path):
            a = recursively_dump_the_blueprint_book_into_files(item_path)
            a.update({"index": index})
            return_dict['blueprints'].append(a)
            index += 1
        else:
            try:
                with open(item_path, 'r', encoding='utf-8') as f:
                    a = json.loads(undump(f.read()))
                    a['index'] = index
                    unknown_key = [key for key in a.keys() if key != 'index'][0]
                    a[unknown_key]['label'] = os.path.splitext(os.path.basename(item_path))[0]
                    return_dict['blueprints'].append(a)
            except Exception as e:
                raise Exception(f"Error Blueprint: '{os.path.abspath(item_path)}' \nERROR:{str(e)}")
            index += 1

    return {
        "blueprint_book": return_dict
    }
