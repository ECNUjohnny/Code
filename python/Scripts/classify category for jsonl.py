from pathlib import Path
import json
import os
import matplotlib.pyplot as plt

RAW = r'D:\WorkSpace\Research\Innovation institute\Data\_catalog.jsonl'
OUT_DIR = r'D:\WorkSpace\Research\Innovation institute\Data'

categ = {}
freq = {}

def classify():
    with open(RAW, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            category = data['category']

            if not category in categ:
                file = os.path.join(OUT_DIR, f'{category}.jsonl')                
                categ[data['category']] = file
                freq[data['category']] = 1

            else:
                freq[data['category']] += 1

            with open(categ[data['category']], 'a', encoding='utf-8') as g:
                json_str = json.dumps(data, ensure_ascii=False)
                g.write(json_str + '\n')                


    table_data = []
    for cat, file_path in categ.items():
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            size_kb = round(size_bytes / 1024, 2)
            table_data.append([cat, freq[cat], f'{size_kb} KB'])

    visualize_table(table_data)


def visualize_table(data):
    fig, ax = plt.subplots(figsize=(8, len(data) * 0.5 + 1))
    ax.axis('tight')
    ax.axis('off')

    headers = ['Category', 'Total Counts', 'Size']

    table = ax.table(
        cellText=data,
        colLabels=headers,
        cellLoc='center',
        loc='center',
        colColours=['#f2f2f2'] * 3
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    plt.title('Category Overview')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    classify()