#!/usr/bin/env python

import csv
import json
import os


# TODO: rename to emphasize that func does operate on files
def csv_to_json(dir_path, filename, output_dir_path, labels=None):
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

    labels = labels if labels else []

    input_path = os.path.join(dir_path, filename)

    with open(input_path) as f:
        reader = csv.DictReader(f, labels)
        contents = list(reader)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    output_filename = '{}'.format(os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir_path, output_filename)
    with open(output_path, 'w') as f:
        json.dump(contents, f, indent=2)


def main():
    # TODO: move to separate file
    metadata = [
        {
            'filename': 'airports.csv',
            'labels': [
                'id',
                'name',
                'city',
                'country',
                'iata',
                'icao',
                'latitude',
                'longitude',
                'altitude',
                'timezone_offset',
                'dst',
                'timezone',
                'type',
                'source',
            ],
        },
        {
            'filename': 'airlines.csv',
            'labels': [
                'id',
                'name',
                'alias',
                'iata',
                'icao',
                'callsign',
                'country',
                'active',
            ],
        },
        {
            'filename': 'routes.csv',
            'labels': [
                'airline',
                'airline_id',
                'source_airport',
                'source_airport_id',
                'destination_airport',
                'destination_airport_id',
                'codeshare',
                'stops',
                'equipment',
            ],
        },
    ]

    output_dir_path = os.path.join('data', 'json')
    for entry in metadata:
        filename = entry['filename']
        labels = entry['labels']
        csv_to_json('data', filename, output_dir_path, labels=labels)


if __name__ == '__main__':
    main()

