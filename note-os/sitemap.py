import os
import sys
import codecs

def generate_sitemap(path1, path2):
    """
    append file2 to file1.
    :param file1: an xml file
    :param file2: an xml file
    """
    # read file1, escape the first and the second line
    with codecs.open(path2, mode='r', encoding='utf-8') as file:
        content2 = file.readlines()[2:]

    # add content to the end of file1
    with codecs.open(path1, mode='r', encoding='utf-8') as file:
        # read and remove last line
        content1 = file.readlines()[:-1]

    content1.extend(content2)
    with codecs.open(path1, mode='w', encoding='utf-8') as file:
        file.writelines(content1)



if __name__ == "__main__":
    path1 = "/Users/larry/techlarry.github.io/sitemap.xml"
    path2 = "/Users/larry/techlarry.github.io/note-os/sitemap.xml"
    docs = generate_sitemap(path1, path2)

