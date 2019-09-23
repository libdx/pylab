#!/usr/bin/env python

import csv
import json

from pathlib import Path


def csv_file_to_json(file, output_dir, labels=None):
    """Converts CSV data file to JSON data file.

    :param file: path to CSV file.
    :type file: pathlib.Path
    :param output_dir: path to output directory where JSON file will be placed.
    :type output_dir: pathlib.Path
    :param labels: list of columns names.
    :type labels: list[str]
    """

    if labels is None:
        labels = []

    if output_dir is None:
        output_dir = file.parent

    with open(file) as f:
        reader = csv.DictReader(f, labels)
        contents = list(reader)

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    output_file = output_dir / file.with_suffix('.json').name
    with open(output_file, 'w') as f:
        json.dump(contents, f, indent=2)


def main():
    with open('data/metadata.json') as f:
        metadata = json.load(f)

    data_dir = Path('data')
    output_dir = Path('data') / 'json'

    for entry in metadata:
        filename = entry['filename']
        labels = entry['labels']
        csv_file = data_dir / filename
        csv_file_to_json(csv_file, output_dir, labels)


if __name__ == '__main__':
    main()
