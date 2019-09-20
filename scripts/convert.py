#!/usr/bin/env python

import csv
import json
import os


def csv_to_json(dir_path, filename, output_dir_path=None, labels=[]):
    """Converts CSV data file to JSON data file

    dir_path -- path to directory containing CSV file
    filename -- CSV file name
    output_dir_path -- output directory where JSON file will be placed
    """
    if output_dir_path is None:
        return

    input_path = os.path.join(dir_path, filename)

    with open(input_path) as f:
        reader = csv.DictReader(f, labels)
        contents = [row for row in reader]

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    output_filename, _ = os.path.splitext(filename)
    output_filename += '.json'
    output_path = os.path.join(output_dir_path, output_filename)
    with open(output_path, 'w') as f:
        json.dump(contents, f, indent=2)


def main():
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
        csv_to_json(
            'data', filename, output_dir_path=output_dir_path, labels=labels
        )


if __name__ == '__main__':
    main()
