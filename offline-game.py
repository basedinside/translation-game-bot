from fnmatch import fnmatch
import pathlib
import yaml
import os


# This function returns YAML from my Obsidian note as one line
def parse_yaml(lines):

    t_yaml = list()
    # This is to count '---' lines (if there are two of theese, we should stop the cycle)
    t_count = 0

    for line in lines:
        if line.strip('\n').strip('\t') == '---':
            t_count += 1
            continue
        t_yaml.append(line)
        if t_count == 2:
            break
    # Remove empty strings in list
    # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
    # yaml = list(filter(None, '|'.join(t_yaml).replace('\n', '').replace('\t', '').split('|')))
    yaml = '|'.join(t_yaml).replace('\n', '').replace('\t', '')
    
    return yaml

def get_filepaths(root, pattern):
    filepaths = list()

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                filepaths.append(pathlib.PurePath(path, name)) #os.path.join(path, name)) / pathlib.PurePath(path, name)

    return filepaths


filepaths = get_filepaths('C:\Guts', '*.md')
tag = '*flashcards*'

for path in filepaths:
    with open(path, 'r', encoding='UTF-8') as stream:
        lines = stream.readlines()
        yaml = parse_yaml(lines)
        if fnmatch(yaml, tag):
            print(path)

  