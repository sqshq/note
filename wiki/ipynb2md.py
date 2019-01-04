"""
把Jupyter NoteBook转化为MarkDown
"""

import codecs
import os
import re
import json


def convert_ipynb_to_markdown(path):
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        if os.path.isdir(filename) and file[0] != '.':
            convert_ipynb_to_markdown(filename)
        elif is_ipynb(filename):
            json_format = ''
            with codecs.open(filename, mode='r', encoding='utf-8') as ipynb_file:
                json_format = json.load(ipynb_file)
            markdown_format = process_ipynb(json_format)
            with codecs.open(re.sub(r'.ipynb', r'.md', filename), mode='w', encoding='utf-8') as md_file:
                md_file.write(title(file) + markdown_format)

def title(filename):
    """
    生成markdown title
    """
    return '''---\ntitle: %s\n---\n''' % filename.split('.')[0]
    

def is_ipynb(filename):
    """
    所给文件是不是Jupyter notebook
    """
    if not os.path.isfile(filename):
        return False
    if filename.split('.')[-1] == 'ipynb':
        return True
    return False


def process_ipynb(file_content):
    """
    The file content of ipynb file, output a string with markdown format
    """
    # Jupyter Notebook所使用的编程语言
    language = file_content['metadata']['kernelspec']['language']
    beginingCodeBlock = '\n```%s\n' % language
    beginingOutputBlock = '\n```%s\n' % language
    tail = '```\n'
    markdown_content = []
    for cell in file_content['cells']:
        cell_type = cell['cell_type']
        if  cell_type == 'markdown':
            markdown_text =  ''.join(cell['source'])
            markdown_content.append('\n' + markdown_text)
        elif cell_type == 'code':
            outputs = cell['outputs']
            if not outputs or not outputs[0]:
                continue
            output = outputs[0]
            if 'text' in output:
                text = ''.join(output['text'])
                if text[-1:] == '\n':
                    markdown_content.append(beginingCodeBlock + text + tail)
                else:
                    markdown_content.append(beginingCodeBlock + text + '\n' + tail)

            if 'data' in output:
                data = ''.join(output['data']['text/plain'])
                if data[-1:] == '\n':
                    markdown_content.append(beginingOutputBlock + data + tail)
                else:
                    markdown_content.append(beginingOutputBlock + data + '\n' + tail)
    return ''.join(markdown_content)

if __name__ == '__main__':
    convert_ipynb_to_markdown(os.getcwd())
