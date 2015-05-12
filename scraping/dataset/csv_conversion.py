import json
import csv

with open('dataset.json', 'r') as dataset_file:
    dataset = json.load(dataset_file)

with open('dataset.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, dataset[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(dataset)
