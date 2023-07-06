# FactorioBluePrintToolkit
[![AGPLv3 License](https://img.shields.io/badge/license-AGPLv3-blue.svg?style=flat-square)](http://www.fsf.org)
#### 这是一个处理[异星工场](https://www.factorio.com/)的蓝图和蓝图书的软件
## 它可以做什么?
* 将蓝图书/蓝图的字符串转换成json(dict)方便编辑
* 将json(dict)形式的蓝图转换会蓝图字符串
* 递归解压一个蓝图书字符串，并且最终只保留蓝图作为文件,蓝图书加载成文件夹
* 递归打包一个蓝图文件夹回到蓝图书
## 使用

## 功能细节
> 你可以在[这里](https://wiki.factorio.com/Blueprint_string_format#:~:text=A%20blueprint%20string%20is%20a%20JSON%20representation%20of,currently%200%20%28for%20all%20Factorio%20versions%20through%201.1%29.)阅读到异星工场的蓝图说明
> ***
> 使用的nuitka的打包命令:`nuitka --standalone --mingw64 --show-memory --show-progress --follow-imports --remove-output --output-dir=../exe --onefile main.py`
* 解压蓝图/蓝图书字符串为json
  * 函数名: undump
  * 输入:要解压的字符串 输出:解压完成的json字符串
* 压缩蓝图/蓝图书json到字符串
  * 函数名:dump
  * 输入:要压缩的字典 输出:压缩完成后的蓝图字符串
  * 说明:异星工场的蓝图需要用zlib和base64,所以json字符串不能有空格。所以选择传入字典，里面用json.dumps()
* 递归解压蓝图书
  * 函数名:recursively_undump_the_blueprint_book_into_files
  * 输入:解压后的蓝图书json字符串 要解压的路径
  * 说明: 会在路径创建一个名字为蓝图书的名字的文件夹，并且依次解压，蓝图书会解压为文件夹，蓝图则解压成.txt文件(内部是蓝图字符串,方便点开导入)  并且会在每个文件夹下创建一个_intro_文件来存储属性  
  所有的_intro_文件都**不包含蓝图书名称** 决定蓝图书名称的是文件名 蓝图也一样  
  为了保证可以在windows中正常的创建,遵循下列替换规则(符号为半角->全角):  
  ```
  < -> ＜
  > -> ＞
  : -> ：
  " -> ＂
  / -> ／
  \ -> ＼
  | -> ｜
  ? -> ？
  * -> ＊
  删除末尾空格
  替换末尾的半角.为全角．

* 递归压缩蓝图书文件夹
  * 函数名:recursively_dump_the_blueprint_book_into_files
  * 输入:要压缩的蓝图文件夹的路径 输出:压缩完成后的字典
  * 说明: 以路径的文件夹开始往下递归 会尝试读取_intro_文件夹来加载配置内容,如果没有的话那么就按照下列规则替换:
  ```
  {
    "item": "blueprint-book",
    "active_index": 0,
    "label": 文件夹名称
  } 
    ```  
  所有的文件夹内的内容名称都以**文件名称**存储到返回值中而不是其真实名称(例如一个蓝图文件的蓝图代码叫做a,但是这个蓝图文件.txt名叫b,那么最终压缩完成你看到的蓝图名称还是b)
  当然,你也可以把你的蓝图书字符串放在其中的一个文件中，仍然会正常地加入字典中

