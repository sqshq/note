import os
import codecs
import re

"""
给每个文件夹生成一个导航文件
"""

# escape these directories when scanning
Invalid_dir = {'custom_theme', 'tags', 'css', '爬虫', 'Mila', 'Prob',
	 'Projects', 'Java多线程', 'Leetcode', 'Miscellaneous', 'Tags', 'cpj', 'CSE521'}
# top_categeory

top_categeory = {'Java', 'Algorithm', 'OS', 'Big Data'}

# to remove
path_to_remove = r"/Users/larry/techlarry/wiki/docs/"

# escape these files when scanning
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

def reindex(path):
    """
    给每个文件夹生成一个导航文件
    """
    # path对应的必须是个文件夹
    if not os.path.isdir(path):
         raise NameError
    # 处理文件夹下面的每一个文件
    chapters = [] # chapters, (文件名, 路径)元组
    books = [] # books
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        # not a vaild file
        if (not is_valid_file(file_path)):
            continue
        # it is a directory
        if (os.path.isdir(file_path)):
            if filename not in Invalid_dir:
            	book_content = reindex(file_path)
            	if book_content:
            		books.append((filename, book_content))
        # it is a markdown file
        else:
            if filename not in Invlaid_files:
                chapters.append((filename, filename))

    # 生成一个导航文件
    if books:
        index_books = create_index_books(path, books)
        write_index_books(path, index_books)
        return index_books

    elif chapters and len(chapters) > 3:
        index_chapters = create_index_chapters(path, chapters)
        write_index_chapters(path, index_chapters)
        return index_chapters

def write_index_books(path, contents):
    """
    把书本/课程导航写入文件
    """
    category = path.split(r'/')[-1]
    title = '### %s \n\n' % category
    with codecs.open(os.path.join(path, 'index.md'), mode='w', encoding='utf-8') as f:
        f.write(title + contents)

def create_index_books(path, books):
    index_books = []
    for book_name, book_content in books:
        if book_name in top_categeory:
            title = '### %s \n\n' % book_name
        else:
            title = '#### %s \n\n' % book_name
        index_books.append(title)
        index_books.append(book_content.replace('(', '(' + book_name.replace(' ', '%20') + '/'))
    return ''.join(index_books)


def  write_index_chapters(path, contents):
    """
    把章节导航写入文件
    """
    book = path.split(r'/')[-1]
    title = '### %s \n\n' % book
    print(contents)
    with codecs.open(os.path.join(path, 'index.md'), mode='w', encoding='utf-8') as f:
        f.write(title + contents)


def create_index_chapters(path, chapters):
    """
    返回写入到导航文件中的内容
    chapters：章节列表，包含每一章名称以及路径
    """
    index_chapters = []
    chapters = sort_chapters(chapters)
    for afile in chapters:
        chapter_name, chapter_path =  afile[0], afile[1] 
        index_chapters.append('* [%s](%s) \n' % (chapter_name.replace('.md', ''), chapter_path.replace(' ', '%20').replace('.md', '')))
    index_chapters.append('\n')
    return ''.join(index_chapters)

def sort_chapters(chapters):
    """
    根据章节序号进行排序
    """
    to_sort = []
    for afile in chapters:
        chapter_name =  afile[0]
        chapter_number = re.findall(r'\d+', chapter_name)
        # 如果章节号存在，则依据章节号排序
        if chapter_number:
            to_sort.append((int(chapter_number[0]), afile))
        else:
            return chapters
    to_sort.sort()
    return map(lambda x: x[1], to_sort)

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
    reindex(os.path.join(os.getcwd(), 'docs'))

