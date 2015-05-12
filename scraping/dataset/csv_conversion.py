import json
import csv

with open('dataset.json', 'r') as dataset_file:
    dataset = json.load(dataset_file)

with open('dataset.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, dataset[0].keys())
    dict_writer.writeheader()

    for row in dataset:
        # to allow lexical sorting
        if 'Forår' in row['semester']:
            row['semester'] = row['semester'].replace('Forår ', '') + 'a'
        if 'Efterår' in row['semester']:
            row['semester'] = row['semester'].replace('Efterår ', '') + 'b'

        dict_writer.writerow(row)
