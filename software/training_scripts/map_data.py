import csv
import os

CURR_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(CURR_FOLDER, '../data')
INPUT_FILE = os.path.join(DATA_FOLDER, 'newer_clean_data.csv')
OUTPUT_FILE = os.path.join(DATA_FOLDER, 'newer_mapped_data.csv')

def map_range(row):
  return list(map(lambda x: (int(x) * (2**8 - 1) // (2**12 - 1)) - 50, row))

if __name__ == '__main__':
    mapped_data = []
    with open(INPUT_FILE) as csvfile:
        og_csv = csv.reader(csvfile, delimiter=',', quotechar='|')
        clean_row = []
        for row in og_csv:
            mapped_row = map_range(row[1:])
            mapped_row = [row[0]] + mapped_row
            mapped_data.append(mapped_row)
    # print(mapped_data)
    with open(OUTPUT_FILE, 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(mapped_data)