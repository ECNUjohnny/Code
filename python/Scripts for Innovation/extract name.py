import os
from tqdm import tqdm

SOURCE = r'D:\WorkSpace\Research\Open-Moss\Data\Video Gen\usable scenes'
SOURCE1 = r'D:\WorkSpace\Research\Open-Moss\Data\Video Gen\not usable scenes'
FILE = r'D:\WorkSpace\Research\Open-Moss\Data\Video Gen'

def modify_name(folder):
    with os.scandir(folder) as entries:
        for entry in entries:
            old_name = entry.name
            new_name = old_name[old_name.find('_') + 1:]
            new_name = new_name[:new_name.find('_')] + '.png' 
            os.rename(entry.path, os.path.join(os.path.dirname(entry.path), new_name))

def extract_name():
    file = os.path.join(FILE, 'lists.txt')
    with open(file, 'a', encoding='utf-8') as f:
        with os.scandir(SOURCE) as entries:
            for entry in tqdm(entries, desc='name', ncols=100):
                line = os.path.splitext(entry.name)[0]
                f.write(line + '\n')


if __name__ == '__main__':
    extract_name()