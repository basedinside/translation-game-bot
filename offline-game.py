from fnmatch import fnmatch
import pathlib
import os
import pandas as pd
import numpy as np



# This function returns YAML from my Obsidian note as one line
def parse_yaml(lines):

    t_yaml = list()
    # This is to count '---' lines (if there are two of theese, we should stop the cycle)
    t_count = 0

    for line in lines:
        if line.strip('\n\t') == '---':
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

# This function returns all files mathcing pattern from given root and subdirectories
def get_filepaths(root, pattern):
    filepaths = list()

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                filepaths.append(pathlib.PurePath(path, name))

    return filepaths

# This function returns only paths to notes with specified tags
def get_vokabel_filepaths(directory, tag_pattern):
    # directory = 'C:\Guts'
    # tag_pattern = '*flashcards*'
    
    filepaths = get_filepaths(directory, '*.md')
    vokabel_notes = list()

    for path in filepaths:
        with open(path, 'r', encoding='UTF-8') as stream:
            lines = stream.readlines()
            yaml = parse_yaml(lines)
            if fnmatch(yaml, tag_pattern):
                vokabel_notes.append(path)

    return vokabel_notes


# This function gives list of tuples with translations
def get_translations_from_note(path_to_note):
    words = list()
    pattern = '*:::*'

    with open(path_to_note, 'r', encoding='UTF-8') as stream:
        for line in stream.readlines():
            if fnmatch(line, pattern):
                # Remove all technical characters, than remove spaces
                t = tuple(map(lambda x: x.strip(), line.strip('\n\t').split(':::')))
                # Convert to Series
                row = pd.Series(t, index=['DE', 'EN/RU'])
                words.append(row)
    
    return pd.concat(words, axis=1).T


# This function returns exersices split in days
def create_exersice_dataframes(dataframes, n_days):
    df = pd.concat(dataframes, axis=0)
    df = df.sample(frac=1).reset_index(drop=True)
    days = np.array_split(df, n_days)

    # Write days to files
    for i in range(len(days)):
        days[i].to_csv(path_or_buf=f'./Day_{i}.csv', sep='\t')

    return days


def generate_exercises(directory, tag, n_days):
    dataframes = []
    for path in get_vokabel_filepaths(directory, tag):
        dataframes.append(get_translations_from_note(path))

    create_exersice_dataframes(dataframes, n_days)


generate_exercises('C:\Guts', '*flashcards*', 5)