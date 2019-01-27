from bs4 import BeautifulSoup
import requests
import codecs
import sys
import os

def isMd(filename):
    if filename[-3:] == '.md':
        return True
    return False


def parse_tables_from_html(url, md_file):
    """
    parse tables from a html file
    convert it to a markdown(.md) file
    """
        
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    table_content = ""
    for table in soup.select('table'):
        table_content += process_table(table)
    with codecs.open(md_file, mode='w', encoding='utf-8') as file:
        file.write(table_content)

def process_table(table):
    tableMd = ""
    thead = table.select_one('thead')
    tbody = table.select_one('tbody')
    tfoot = table.select_one('tfoot')
    num_of_columns = len(thead.select('th'))
    # processing headerline
    header_items = thead.select('th')
    headerlineMd = '| ' # add headerline
    for th in header_items:
        headerlineMd += th.text + " | "
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
            rowMd += cell.text + ' | '
        tableMd += rowMd + '\n'
    return tableMd + '\n'

if __name__ == '__main__':
    len_of_argv = len(sys.argv)
    if len_of_argv < 2:
        print('Usage: python parseHTMLTable.py url [markdown-file]')
        exit()
    elif len_of_argv == 2:
        url = sys.argv[1]
        parse_tables_from_html(url, 'sample.md')
        print("Table is saved in sample.md.")
    elif len_of_argv == 3:
        url = sys.argv[1]
        md_file = sys.argv[2]
        parse_tables_from_html(url, md_file)
        print("Table is saved in " + md_file)


