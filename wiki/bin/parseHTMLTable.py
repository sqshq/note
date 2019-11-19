from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import sys
import os
import codecs


def isMd(filename):
    if filename[-3:] == '.md':
        return True
    return False


def parse_tables_from_url(url, md_file):
    """
    parse tables from an url
    convert it to a markdown(.md) file
    """

    r = requests.get(url)
    parse_tables_from_html(r.text, md_file)


def parse_tables_from_html(html, md_file):
    """
    parse tables from a html file
    convert it to a markdown(.md) file
    """
    soup = BeautifulSoup(html, features="lxml")
    table_contents = ""
    for table in soup.select('table'):
        try:
            table_content = process_table(table)
            table_contents += table_content
        except:
            continue

    if not table_contents:
        print("NO VALID TABLE")
        return

    # write to the file
    with codecs.open(md_file, mode='w', encoding='utf-8') as file:
        file.write(table_contents)
    print("The Table is saved in" + md_file)


def process_table(table):
    tableMd = ""
    tbody = table.select_one('tbody')
    thead = table.select_one('thead')
    if not tbody:
        tbody = table
        thead = table.select_one('tr')
    if not thead:
        thead = table.select_one('tr')
    if not thead:
        thead = table.select_one('td')

    # processing headerline
    header_items = thead.select('th')
    if not header_items:
        header_items = thead.select('tr')
    if not header_items:
        header_items = thead.select('td')
    num_of_columns = len(header_items)
    headerlineMd = '| '  # add headerline
    for th in header_items:
        headerlineMd += th.text.replace("\n", " ") + " | "
    tableMd += headerlineMd + '\n'

    # add line mark
    line_mark = '|'
    for i in range(num_of_columns):
        line_mark += " --- |"
    tableMd += line_mark + '\n'

    # add content row
    for row in tbody.select('tr'):
        rowMd = "| "
        for cell in row.select('td'):
            rowMd += cell.text.replace("\n", " ").replace("\t", " ") + ' | '
        tableMd += rowMd + '\n'
    return tableMd + '\n'


def is_url(url):
    """
    判断给定字符串是不是URL
    :param url: 字符串
    :return: URL返回True，否则返回False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_html(filename):
    """
    判断文件是不是HTML文件
    :param file: 文件
    :return: HTML文件返回True，否则False
    """
    try:
        if filename[-5:] == ".html" or filename[-4:] == ".htm":
            return True
    except:
        return False
    return False

if __name__ == '__main__':
    len_of_argv = len(sys.argv)
    if len_of_argv < 2:
        print('Usage: python parseHTMLTable.py url | html-file  [markdown-file]')
        exit()
    elif len_of_argv == 2:
        url_or_file = sys.argv[1]
        if is_url(url_or_file):
            url = url_or_file
            parse_tables_from_url(url, 'sample.md')
        elif is_html(url_or_file):
            htmlfile = os.path.join(os.curdir, url_or_file)
            with codecs.open(htmlfile, mode='r', encoding='utf-8') as file:
                html = file.read()
            parse_tables_from_html(html, 'sample.md')
        else:
            print('Usage: python parseHTMLTable.py url | html-file  [markdown-file]')
            exit()

    elif len_of_argv == 3:
        url = sys.argv[1]
        md_file = sys.argv[2]
        parse_tables_from_url(url, md_file)
        print("The Table is saved in " + md_file)
