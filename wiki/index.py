import os
import codecs

Invalid_tags = []
Invalid_dir = ['custom_theme', 'tags', 'css']


def remove_invalid_tags(tags_map):
    """
    remove invalid tags
    """
    for tag in Invalid_tags:
        if tag in tags_map:
            del tags_map[tag]


def build_tags(path):
    """
    build tags for all markdown files
    """
    all_tags = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        # not a vaild file
        if (not is_valid_file(file_path)):
            continue
        # it is a directory
        if (os.path.isdir(file_path)):
            if filename in Invalid_dir:
                all_tags.extend(build_tags(file_path))
        # it is a markdown file
        else:
            tags = extract_tags(file_path)
            if tags:
                all_tags.append(tuple((file_path, tags)))
    return all_tags

def build_index_of_tags(tags):
    """
    build index of tags: map tags to files
    """
    tags_map = {}
    for file, tags in tags:
        for tag in tags:
            if tag in tags_map:
                tags_map[tag].append(file)
            else:
                tags_map[tag] = [file]
    return tags_map

def write_tag(path, tags):
    """
    write tags to file
    """
    tags_map = build_index_of_tags(tags);
    remove_invalid_tags(tags_map)
    for tag in tags_map:
        with codecs.open(os.path.join(path, tag) + '.md', mode='w', encoding="utf-8") as f:
            f.write(process_tag_info(tags_map[tag]))

def process_tag_info(tag_info):
    """
    process tag info, transform it to a string
    """
    result = []
    for filepath in tag_info:
        title = os.path.basename(filepath);
        relateive_path = os.path.join(os.getcwd(), 'docs/')
        url = filepath.replace(relateive_path, '../../').replace(' ', '%20').replace('.md', '')
        result.append("* [" + title + "](" + url + ")\n")
    result.sort()
    return ''.join(result)


def extract_tags(path):
    """
    extract tags from markdown files
    """
    tags = []
    with codecs.open(path, mode='r', encoding="utf-8") as f:
        for i in range(10): # search for first 10 lines
            line = f.readline()
            tokens = line.split(':')
            may_be_tag = tokens[0].strip()
            if may_be_tag == 'tags' or  may_be_tag == 'tag': # is a tag or tags
                tags_to_split = tokens[1].strip('\n ').strip('[]')
                tags = [tag.strip() for tag in tags_to_split.split(',')]
    return tags


def is_md_file(filename):
    return filename[-3:] == '.md'


def is_valid_file(path):
    """
    return true if given file is either markdown file or a directory
    """
    return is_md_file(path) or os.path.isdir(path)



if __name__ == "__main__":
    tags = build_tags(os.path.join(os.getcwd(), 'docs'))
    write_tag(os.path.join(os.getcwd(), 'docs/tags'), tags)
