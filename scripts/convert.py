#!/usr/bin/env python

import csv
import json
import os


def csv_file_to_json(dir_path, filename, output_dir_path, labels):
    """Converts CSV data file to JSON data file.

    :param dir_path: path to directory containing CSV file.
    :type dir_path: str
    :param filename: CSV file name.
    :type filename: str
    :param output_dir_path: output directory where JSON file will be placed.
    :type output_dir_path: str
    :param labels: list of columns names.
    :type labels: list[str]
    """

    labels = [] if labels is None else labels
    output_dir_path = dir_path if output_dir_path is None else output_dir_path

    input_path = os.path.join(dir_path, filename)

    with open(input_path) as f:
        reader = csv.DictReader(f, labels)
        contents = list(reader)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    output_filename = '{}.json'.format(os.path.splitext(filename)[0])
    output_path = os.path.join(output_dir_path, output_filename)
    with open(output_path, 'w') as f:
        json.dump(contents, f, indent=2)


def main():
    with open('data/metadata.json') as f:
        metadata = json.load(f)


    output_dir_path = os.path.join('data', 'json')
    for entry in metadata:
        filename = entry['filename']
        labels = entry['labels']
        csv_file_to_json('data', filename, output_dir_path, labels)


if __name__ == '__main__':
    main()

