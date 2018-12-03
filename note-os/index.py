import os
import yaml
import sys
import codecs
import re

NO_INDEX = set(['Books', 'Home', 'Topics', 'Contents'])


def load_mkdocs():
    filename = '/Users/larry/note-os/mkdocs.yml'
    with codecs.open(filename, mode='r', encoding='utf-8') as f:
        return yaml.load(f.read())


def make_index(docs):
    categories = docs['nav']
    for category in categories:
        for category_name, category_content in category.items():
            if category_name in NO_INDEX:
                continue
            contents = []
            for book in category_content:
                for book_name, book_content in book.items():
                    if book_name in NO_INDEX:
                        continue
                    book_path = category_name + '/' + book_name
                    contents.append(write_book(book_path, book_name, book_content))
            write_category(category_name, category_name, ''.join(contents))

def write_category(path, category, contents):
    path = os.path.join('docs', path.lower(), 'index.md')
    title = '### **%s**' % category
    document = '\n'.join([title, contents])
    with codecs.open(path, mode='w', encoding="utf-8") as f:
        f.write(re.sub(r'.md', '', document))


def write_book(path, book, pages):
    path = os.path.join('docs', path.lower(), 'index.md')
    title = '### **%s**' % book
    small_title = '### %s' % book
    contents_without_book = '\n'.join(map(map_page_remove_book, pages)) 
    contents_with_book = '\n'.join(map(map_page_with_book, pages)) 
    document = '\n\n'.join([title, contents_without_book])
    with codecs.open(path, mode='w', encoding="utf-8") as f:
        f.write(document)
    return ''.join(['\n', small_title, '\n', contents_with_book, '\n'])


def map_page_remove_book(page):
    """
    {'Chapter 1: title ': 'physics/geodynamics/ch1.md'} => '[Chapter 1: title](ch1.md)'
    """
    for key, value in page.items():
        if key != "Contents":
            return '* [%s](%s)' % (key, value.split("/")[-1])
        else:
            return ""

def map_page_with_book(page):
    """
    {'Chapter 1: title ': 'physics/geodynamics/ch1.md'} => '[Chapter 1: title](geodynamics/ch1.md)'
    """
    for key, value in page.items():
        if key != "Contents":
            return '* [%s](%s)' % (key, value[re.search(r'/', value).end():])
        else:
            return ""


if __name__ == "__main__":
    docs = load_mkdocs()
    make_index(docs)

