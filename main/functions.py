# 这里是具体功能的实现 可以直接进行调用
import base64
import zlib


def undump(undump_str: str) -> str:
    """
    解压异星工场的蓝图文件
    :param undump_str:要解压的字符串
    :return:返回解压完成后的字符串 要自己解析成字典
    """
    return zlib.decompress(
        base64.b64decode(undump_str[1:].encode('utf-8'))
    ).decode('utf-8')


def dump(dump_str: str) -> str:
    """
    压缩异星工场的蓝图文件
    :param dump_str: 要压缩的json字符串(没有缩进)
    :return: 压缩好后的蓝图文件
    """
    return f"0{base64.b64encode(zlib.compress(dump_str.encode('utf-8'), level=9)).decode('utf-8')}"


def recursively_undump_the_blueprint_book_into_files(undump_blueprint_book: str, path) -> None:
    """
    递归解压异星工场的蓝图书
    :param undump_blueprint_book:完成解压的蓝图书json字符串
    :param path:要解压到的路径
    :return:None
    """
    pass
