import json
import pandas as pd
import numpy as np

from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from django_countries import countries


def meter_from_feet(feet):
    ratio = 1 / 3.28084
    return feet * ratio


def country_code_by_name(name):
    if name is None:
        return None
    elif name == 'United States':
        return 'US'
    elif name == "Cote d'Ivoire":
        return 'CI'
    else:
        code = countries.by_name(name)
        return code if code else None


class DataPurger(ABC):
    def __init__(self, data_dir=Path('data')):
        self.data_dir = data_dir
        self.dataframe = None
        self.all_metadata = {}

        metadata_file = self.data_dir / 'metadata.json'
        with open(metadata_file) as f:
            self.all_metadata = json.load(f)

    def _data_file_with_suffix(self, suffix):
        filename = self.metadata['filename']
        file = self.data_dir / Path(filename).with_suffix(suffix)
        return file

    @abstractproperty
    def metadata_key(self):
        pass

    @property
    def csv_file(self):
        return self._data_file_with_suffix('.csv')

    @property
    def json_file(self):
        return self._data_file_with_suffix('.json')

    @property
    def metadata(self):
        return self.all_metadata[self.metadata_key]

    @abstractmethod
    def cleanup(self):
        pass

    def load(self):
        labels = self.metadata['labels']
        self.dataframe = pd.read_csv(self.csv_file, header=None, names=labels)

    def write(self):
        string = self.dataframe.to_json(orient='records')
        data = json.loads(string)
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)


class AirlineDataPurger(DataPurger):
    @property
    def metadata_key(self):
        return 'airline'

    def cleanup(self):
        df = self.dataframe

        df = df.replace(['\\N', '-'], np.nan)
        df = df.dropna(subset=['country'])
        df['country'] = df['country'].apply(country_code_by_name)
        df = df.dropna(subset=['country'])
        df['is_active'] = df['is_active'].replace(['Y'], True).replace(['N'], False)

        self.dataframe = df


class RouteDataPurger(DataPurger):
    @property
    def metadata_key(self):
        return 'route'

    def cleanup(self):
        df = self.dataframe

        df = df.replace(['\\N'], np.nan)
        df = df.dropna()

        del df['airline']
        del df['origin_airport']
        del df['destination_airport']
        del df['codeshare']

        df = df.rename({'origin_airport_id': 'origin_airport'}, axis=1)
        df = df.rename({'destination_airport_id': 'destination_airport'}, axis=1)
        df = df.rename({'airline_id': 'airline'}, axis=1)

        self.dataframe = df


class AirportDataPurger(DataPurger):
    @property
    def metadata_key(self):
        return 'airport'

    def cleanup(self):
        df = self.dataframe

        df['altitude'] = df['altitude'].apply(meter_from_feet)
        df['country'] = df['country'].apply(country_code_by_name)
        df = df.dropna()

        df = df.replace(['\\N'], np.nan)

        del df['dst']
        del df['type']
        del df['source']

        self.dataframe = df


def main():
    purgers = [AirlineDataPurger(), RouteDataPurger(), AirportDataPurger()]

    for purger in purgers:
        purger.load()
        purger.cleanup()
        purger.write()


def run():
    main()
