import os
import shutil


TARGET = r'D:\WorkSpace\Research\Innovation institute\Data\photos'
SOURCE = r'D:\WorkSpace\Research\Innovation institute\Data\scenes'

def extract_photos():

    with os.scandir(SOURCE) as entries:    
        for entry in entries:
            if not entry.is_dir():
                continue

            with os.scandir(entry.path) as sentries:
                for sentry in sentries:
                    if os.path.splitext(sentry.name)[1].lower() in ['.png', '.jpg']:
                        shutil.copy(sentry.path, TARGET)

if __name__ == '__main__':
    extract_photos()

