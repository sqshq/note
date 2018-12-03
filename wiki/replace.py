import os
import codecs

"""
Replace every pair of word for markdown files in given path
"""
keywords = {"http://larryim.cc":"https://techlarry.github.io", "http://larryim.cc/wiki/2017/10/30/":"https://techlarry.github.io/wiki/Leetcode/", "fct_label":"tab"}
Invalid_dir = ["extra_css", "extra_javascript", "custom_theme"]

def replace_keyword(path):
    """
    replace keyword for all markdown files
    """
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        # not a vaild file
        if (not is_valid_file(file_path)):
            continue
        # it is a directory
        if (os.path.isdir(file_path)):
            if filename not in Invalid_dir:
                replace_keyword(file_path)
        # it is a markdown file
        else:
            print(file_path)
            file_content = ""
            with codecs.open(file_path, mode='r', encoding="utf-8") as f:
                file_content = f.read()
            for to_replace_word, replace_word in keywords.items(): 
                file_content = file_content.replace(to_replace_word, replace_word)
            with codecs.open(file_path, mode='w', encoding="utf-8") as f:
                f.write(file_content)

def is_md_file(filename):
    return filename[-3:] == '.md'


def is_valid_file(path):
    """
    return true if given file is either markdown file or a directory
    """
    return is_md_file(path) or os.path.isdir(path)



if __name__ == "__main__":
    replace_keyword(os.path.join(os.getcwd()))
