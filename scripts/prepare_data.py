import json
import pandas as pd
import numpy as np

from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from django_countries import countries


def meter_from_feet(feet):
    """Converts feet to meters.

    :param feet: value in feet
    :type feet: float
    :returns: value in meters
    :rtype: float
    """
    ratio = 1 / 3.28084
    return feet * ratio


def country_code_by_name(name):
    """Converts given country name to corresponding ISO-3166 alpha-2 country code.

    :param name: human readable country name
    :type name: str
    :returns: ISO-3166 alpha-2 country code
    :rtype: str
    """

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
    """Abstract class that provides interface to load,
    clean up and convert pre-fetched historical flights data.
    """

    def __init__(self, data_dir=Path('data')):
        """Initializes DataPurger instance.

        :param data_dir: path to directory with CSV data files. Default is './data'
        :type data_dir: pathlib.Path
        """
        self.data_dir = data_dir
        self.dataframe = None
        self.all_metadata = {}

        metadata_file = self.data_dir / 'metadata.json'
        with open(metadata_file) as f:
            self.all_metadata = json.load(f)

    def _data_file_with_suffix(self, suffix):
        """Makes corresponding to metadata path with given suffix

        :param suffix: file's suffix with leading dot (like '.csv', '.json').
        :type suffix: str
        :returns: path to file with given suffix
        :rtype: pathlib.Path
        """
        filename = self.metadata['filename']
        file = self.data_dir / Path(filename).with_suffix(suffix)
        return file

    @abstractproperty
    def metadata_key(self):
        """Abstract property. Provide corresponding dictionary key for metadata in subclasses.

        :returns: predefined metadata key
        :rtype: str
        """
        pass

    @property
    def csv_file(self):
        """Makes corresponding to metadata path with '.csv' suffix.

        :returns: path to file with '.csv' suffix
        :rtype: pathlib.Path
        """
        return self._data_file_with_suffix('.csv')

    @property
    def json_file(self):
        """Makes corresponding to metadata path with '.json' suffix.

        :returns: path to file with '.json' suffix
        :rtype: pathlib.Path
        """
        return self._data_file_with_suffix('.json')

    @property
    def metadata(self):
        """Returns sub-dictionary from metadata under `metadata_key`.

        :returns: sub-dictionary from metadata
        :rtype: Dict[str, Any]
        """
        return self.all_metadata[self.metadata_key]

    @abstractmethod
    def cleanup(self):
        """Abstract method. Place preparing, cleaning up and normalizing data in sublcasses.
        """
        pass

    def load(self):
        """Loads DataFrame from corresponding by metadata file.
        """
        labels = self.metadata['labels']
        self.dataframe = pd.read_csv(self.csv_file, header=None, names=labels)

    def write(self):
        """Write current state of DataFrame to corresponding by metadata json file.
        """
        string = self.dataframe.to_json(orient='records')
        data = json.loads(string)
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)


class AirlineDataPurger(DataPurger):
    """Takes care of Airlines related historical data.
    """

    @property
    def metadata_key(self):
        """Key to be used to get sub-dictionary from metadata corresponding to Airlines.
        """
        return 'airline'

    def cleanup(self):
        """Cleans up and prepares Airlines data.
        """
        df = self.dataframe

        df = df.replace(['\\N', '-'], np.nan)
        df = df.dropna(subset=['country'])
        df['country'] = df['country'].apply(country_code_by_name)
        df = df.dropna(subset=['country'])
        df['is_active'] = df['is_active'].replace(['Y'], True).replace(['N'], False)

        self.dataframe = df


class RouteDataPurger(DataPurger):
    """Takes care of Routes related historical data.
    """

    @property
    def metadata_key(self):
        """Key to be used to get sub-dictionary from metadata corresponding to Routes.
        """
        return 'route'

    def cleanup(self):
        """Cleans up and prepares Routes data.
        """
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
    """Takes care of Airports related historical data.
    """

    @property
    def metadata_key(self):
        """Key to be used to get sub-dictionary from metadata corresponding to Airports.
        """
        return 'airport'

    def cleanup(self):
        """Cleans up and prepares Airports data.
        """
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
