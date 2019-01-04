import os
import codecs
import re

"""
给每个文件夹生成一个导航文件
"""

# escape these directories when scanning
INVALID_DIR = {'figures', 'custom_theme', 'tags', 'css', '爬虫', 'Mila', 'Prob',
               'Projects', 'Java多线程', '其他', 'Leetcode', 'Miscellaneous', 'Tags', 'cpj', 'CSE521'}

# top_categeory
TOP_CATEGORY = {'Java', 'Algorithm', 'OS', 'Big Data'}

# escape these files when scanning
INVALID_FILES = {'index.md'}


def is_md_file(filename):
	"""
    Is file a markdown file?
    """
	return filename[-3:] == '.md'


def is_valid_file(path):
	"""
	Return true if given file is either markdown file or a directory
	"""
	return is_md_file(path) or os.path.isdir(path)


def reindex(path):
	"""
	给每个文件夹生成一个导航文件
	"""
	# path对应的必须是个文件夹
	if not os.path.isdir(path):
		raise NameError("The path of Directory is INCORRECT.")
	# 处理文件夹下面的每一个文件
	chapters = []  # chapters, 文件名列表
	books = []  # books
	for filename in os.listdir(path):
		file_path = os.path.join(path, filename)
		# not a valid file
		if not is_valid_file(file_path):
			continue
		# it is a directory
		elif os.path.isdir(file_path) and filename not in INVALID_DIR:
			book_content = reindex(file_path)
			if book_content:  # valid content?
				books.append((filename, book_content))
		# it is a markdown file
		elif is_md_file(file_path) and filename not in INVALID_FILES:
			chapters.append(filename)

	# 生成一个导航文件
	if books:  # 生成书的导航
		index_books = create_index_books(books)
		if path == os.path.join(os.getcwd(), 'docs'):
			filename = '目录.md'
		else:
			filename = 'index.md'
		write_index_books(os.path.join(path, filename), index_books)
		return index_books

	elif chapters and len(chapters) > 3:  # 生成每本书的章节导航
		index_chapters = create_index_chapters(chapters)
		write_index_chapters(path, index_chapters)
		return index_chapters


def write_index_books(path, contents):
	"""
	把书本/课程导航写入文件
	"""
	category = path.split(r'/')[-1]
	title = '### %s \n\n' % category
	with codecs.open(path, mode='w', encoding='utf-8') as f:
		f.write(title + contents)


def create_index_books(books):
	index_books = []
	for book_name, book_content in books:
		if book_name in TOP_CATEGORY:
			title = '### %s \n\n' % book_name
		else:
			title = '#### %s \n\n' % book_name
		index_books.append(title)
		index_books.append(book_content.replace('(', '(' + book_name + '/'))
	return ''.join(index_books)


def write_index_chapters(path, contents):
	"""
	把章节导航写入文件
	"""
	book = path.split(r'/')[-1]
	title = '### %s \n\n' % book
	with codecs.open(os.path.join(path, 'index.md'), mode='w', encoding='utf-8') as f:
		f.write(title + contents)


def create_index_chapters(chapters):
	"""
	返回写入到导航文件中的内容
	chapters：章节列表，包含每一章名称以及路径
	"""
	index_chapters = []
	chapters = sort_chapters(chapters)
	for chapter_name in chapters:
		index_chapters.append('* [%s](%s)\n' % (chapter_name.replace('.md', ''), chapter_name))
	index_chapters.append('\n')
	return ''.join(index_chapters)


def sort_chapters(chapters):
	"""
	根据章节序号进行排序
	"""
	digit_sort = []
	letter_sort = []
	for chapter_name in chapters:
		chapter_number = re.search(r'\d+', chapter_name)
		# 如果章节号存在，则依据章节号排序
		if chapter_number:
			digit_sort.append((int(chapter_number.group()), chapter_name))
		else:  # 否则根据字母排序
			letter_sort.append((chapter_name, chapter_name))
	letter_sort.sort()
	digit_sort.sort()
	# 字母在前面
	letter_sort.extend(digit_sort)
	return map(lambda x: x[1], letter_sort)


if __name__ == "__main__":
	reindex(os.path.join(os.getcwd(), 'docs'))
