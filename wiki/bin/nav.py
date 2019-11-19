import os
import time
import codecs
import re

"""
给每个文件夹生成一个导航文件
"""

# escape these directories when scanning
INVALID_DIR = {'figures', 'custom_theme', 'tags', 'css', '爬虫', 'Mila', 'Prob',
               'Projects', '其他', 'Tags', 'cpj', 'CSE521'}

# top_categeory
TOP_CATEGORY = {'Java', 'Algorithm', 'OS', 'Big Data', 'Data Science', 'Miscellaneous', 'Leetcode'}

# escape these files when scanning
INVALID_FILES = {'index.md', '目录.md'}

# 当前时间
CURRTIME = "2017-07-07"
CURRTIMES = time.strftime("%Y-%m-%d", time.localtime())

# 配置文件
CONFIG_FILE = "mkdocs.yml"

# 文件开始格式
FILEMETA = """---
title: %s
toc: false
date: %s
---

"""


def get_wiki_site():
    cur_path = os.getcwd()
    if cur_path.endswith('/bin'):
        cur_path = cur_path[:-4]
    return cur_path


def is_md_file(filename):
    """
    Is the file a markdown file?
    """
    return filename[-3:] == '.md'


def is_hidden_file(filename):
    """
    return true if the given file is a hidden file
    """
    return filename.split("/")[-1].startswith(".")


def is_valid_file(path):
    """
    Return true if the  given file is either markdown file or a valid directory
    """
    if is_hidden_file(path):
        return False
    return is_md_file(path) or os.path.isdir(path)


def index(path):
    """
    给每个文件夹生成一个导航文件
    """

    # path对应的必须是个文件夹
    if not os.path.isdir(path):
        raise NameError("The path of Directory is INCORRECT.")
    # 处理文件夹下面的每一个文件
    items = []  # items, 文件名列表
    menus = []  # menus
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        # not a valid file
        if not is_valid_file(file_path):
            continue
        # it is a directory
        elif os.path.isdir(file_path) and filename not in INVALID_DIR:
            x = index(file_path)
            if x:  # valid content?
                (menu_content, meta_menu) = x
                menus.append((filename, menu_content, meta_menu))
        # it is a markdown file
        elif is_md_file(file_path) and filename not in INVALID_FILES:
            items.append(filename)

    # 生成一个导航文件
    if menus:  # 生成书的导航
        index_menus = create_index_menus(menus)
        meta_menuses = create_meta_menus(path, menus)
        if path == os.path.join(get_wiki_site(), 'docs'):  # 这个是总目录
            filename = '目录.md'
            index_menus = replace_space(index_menus)  # 把路径中的空格替换
            # 在配置文件mkdocs.yml中更新nav选项，以便生成正确的目录结构
            update_mkdocs(os.path.join(os.path.split(path)[0], CONFIG_FILE), meta_menuses)
        else:
            # 这个是每本书的目录
            filename = 'index.md'
        write_index_menus(os.path.join(path, filename), index_menus)
        return index_menus, meta_menuses
    elif items and len(items) >= 3:  # 生成每本书的章节导航，但需要章节数大于3
        index_items = create_index_items(items)
        write_index_items(path, index_items)
        # 产生每本书的元信息
        meta_menu = create_meta_items(path, items)
        return index_items, meta_menu


class Nav:
    """
    导航：可以是一本书，或者一个章节
    """
    def __init__(self, title, location):
        self.title = title
        self.location = location


class Item(Nav):
    """
    导航项目
    """
    def __str__(self):
        return self.to_nav(0)

    def to_nav(self, level):
        """
        选择第n级目录，并打印目录
        """
        return "    " * level + "- '" + self.title + "': '" + self.location + "'"


class Menu(Nav):
    """
    导航菜单
    """
    def __init__(self, title, location, items):
        super().__init__(title, location)
        self.items = items

    def __str__(self):
        return self.to_nav(0)

    def to_nav(self, level):
        """
        选择第n级目录，并打印目录
        """
        if isinstance(self.items[-1], Menu):  # 需要排序
            self.items = sorted(self.items, key=lambda x: x.title)
        rest = '\n'.join([item.to_nav(level + 1) for item in self.items])
        if level < 0:   # 这一级目录跳过
            return rest
        return "    " * level + "- '" + self.title + "': " + "\n" + rest


def update_mkdocs(path, meta_menuses):
    """
    在配置文件mkdocs.yml中更新nav选项
    """
    old_contents = []  # 列表每一项代表文件中的每一行
    with codecs.open(path, mode='r', encoding='utf-8') as f:
        old_contents = f.read()
    # 寻找到nav标签，并且删除
    try:
        start_pos_of_nav = old_contents.index("nav:")
    except:
        start_pos_of_nav = len(old_contents)
    contents = old_contents[0:start_pos_of_nav]
    contents += ("nav:" + '\n')
    new_contents = meta_menuses.to_nav(-1)
    # 移除多余空格
    with codecs.open(path, mode='w', encoding='utf-8') as f:
        f.write(contents + new_contents)


def replace_space(string):
    """
    将路径中的空格替换成%20
    """
    new_string = ""
    for line in string.split('\n'):
        match = re.search(r"\(.*\)", line)
        if match:
            revised = re.sub(r"\s", r"%20", match.group())
            line = re.sub(r"\(.*\)", revised, line)
        new_string += line + '\n'
    return new_string


def write_index_menus(path, contents):
    """
    把书本/课程导航写入文件
    """
    category = path.split(r'/')[-1]
    title = FILEMETA % ('Index', CURRTIME)
    with codecs.open(path, mode='w', encoding='utf-8') as f:
        f.write(title + contents)


def create_index_menus(menus):
    """
    创建菜单的导航
    """
    index_menus = []
    for menu_name, menu_content, meta_menu in menus:
        if menu_name in TOP_CATEGORY:
            title = '### %s \n\n' % menu_name
        else:
            title = '#### %s \n\n' % menu_name
        index_menus.append(title)
        index_menus.append(menu_content.replace('(', '(' + menu_name + '/'))
    return ''.join(index_menus)


def create_meta_menus(path, menus):
    """
    创建菜单的元信息
    """
    path = path.split("docs/")[-1]
    menuses = []
    for menu_name, menu_content, meta_menus in menus:
        menuses.append(meta_menus)

    meta_menus = Menu(path.split("/")[-1], path, menuses)
    return meta_menus


def write_index_items(path, contents):
    """
    把项目导航写入文件
    """
    menu = path.split(r'/')[-1]
    title = FILEMETA % ("Index", CURRTIME)
    with codecs.open(os.path.join(path, 'index.md'), mode='w', encoding='utf-8') as f:
        f.write(title + contents)


def create_index_items(items):
    """
    返回写入到导航文件中的内容，用于生成index.md文件
    items：项目列表，包含每一章名称以及路径
    """
    index_items = []
    items = sort_items(items)
    for item_name in items:
        index_items.append('* [%s](%s)\n' % (item_name.replace('.md', ''), item_name))
    index_items.append('\n')
    return ''.join(index_items)


def create_meta_items(path, items):
    """
    创建每本书的每个章节的元信息，用于生成左边的目录导航
    items：章节列表，包含每一章名称以及相对路径
    """
    meta_items = []
    items = sort_items(items)
    path = path.split("docs/")[1]
    for item_name in items:
        name = item_name.replace('.md', '')
        location = path + "/" + item_name
        meta_items.append(Item(name, location))
    meta_menu = Menu(path.split("/")[-1], path + "/index.md", meta_items)
    return meta_menu


def sort_items(items):
    """
    根据章节序号进行排序
    """
    digit_sort = []
    letter_sort = []
    for item_name in items:
        item_number = re.search(r'\d+', item_name)
        # 如果章节号存在，则依据章节号排序
        if item_number:
            digit_sort.append((int(item_number.group()), item_name))
        else:  # 否则根据字母排序
            letter_sort.append((item_name, item_name))
    letter_sort.sort()
    digit_sort.sort()
    # 字母在前面
    letter_sort.extend(digit_sort)
    return map(lambda x: x[1], letter_sort)


if __name__ == "__main__":
    index(os.path.join(get_wiki_site(), 'docs'))
