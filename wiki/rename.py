import os
import codecs

"""
Rename markdown files, to keep filename consistent with title of the article
"""

# escape these directories when scanning
Invalid_dir = {'custom_theme', 'tags', 'css', 'figures'}
Invlaid_files = {'index.md'}


def is_md_file(filename):
    """
    Is file a markdown file?
    """
    return filename[-3:] == '.md'


def is_valid_file(path):
    """
    return true if given file is either markdown file or a directory
    """
    return is_md_file(path) or os.path.isdir(path)

def rename_files(path):
    """
    Rename markdown files.
    """
    # path对应的必须是个文件夹
    if not os.path.isdir(path):
         raise NameError
    # 处理文件夹下面的每一个文件
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        # not a vaild file
        if (not is_valid_file(file_path)):
            continue
        # it is a directory
        if (os.path.isdir(file_path)):
            if filename not in Invalid_dir:
                rename_files(file_path)
        # it is a markdown file
        else:
            # invalid markdown file
            if filename in Invlaid_files:
                continue
            title = extract_title(file_path)
            if title and len(title) > 2: # have title ? a valid title ?
                if filename == title + '.md': # filename is consistent with title
                    continue
                # otherwise rename filename (title.md)
                new_file_path = construct_new_title(path, title)
                print("Rename: %s  ->  %s" % (filename, title))
                os.rename(file_path, new_file_path)

    return 

def construct_new_title(path, title):
    """
    构建新的markdown文件名
    """
    return os.path.join(path, title + '.md') # 加上md后缀


def extract_title(path):
    """
    从markdown文件中提取文章的题目信息
    题目的格式为 title: 要提取的题目
    """
    with codecs.open(path, mode='r', encoding="utf-8") as f:
        # only read first 10 lines
        for i in range(10):
            line = f.readline()
            tokens = line.split(':')
            may_be_title = tokens[0].strip()
            if may_be_title == 'title': # it is a title
                return tokens[1].strip()
    return None

if __name__ == "__main__":
    tags = rename_files(os.getcwd())