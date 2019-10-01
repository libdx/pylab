import json

from django.core.exceptions import ValidationError
from abc import ABC, abstractproperty
from pathlib import Path

from ..models import Airline, Airport, Route


class BaseImporter(ABC):
    Model = None
    batch_size = 100

    def __init__(self, file=None):
        self._file = file
        self.new_objects = []

    def _log(self, msg):
        print(f'[{self.Model}] {msg}')

    @abstractproperty
    def filename_stem(self):
        pass

    @property
    def file(self):
        if self._file is None:
            return Path('data') / Path(self.filename_stem).with_suffix('.json')
        else:
            return self.__file

    def _materialize(self, item):
        return item

    def load(self):
        self._log(f'Loading data from file {self.file}')

        with open(self.file) as f:
            data = json.load(f)

        for item in data:
            try:
                new_object = self.Model(**self._materialize(item))
                new_object.clean_fields()
                self.new_objects.append(new_object)
            except ValidationError:
                self._log(f"{item} won't be imported due to Validation failure")
            except ValueError as e:
                self._log(f"{item} won't be imported due to {e}")

        self._log(f'Created {len(self.new_objects)} objects')

    def save(self):
        self._log(f'Saving in batches=[{self.batch_size}]')

        self.Model.objects.bulk_create(self.new_objects, self.batch_size)


class AirlineImporter(BaseImporter):
    Model = Airline

    @property
    def filename_stem(self):
        return 'airlines'


class AirportImporter(BaseImporter):
    Model = Airport

    @property
    def filename_stem(self):
        return 'airports'


class RouteImporter(BaseImporter):
    Model = Route

    @property
    def filename_stem(self):
        return 'routes'

    def _lookup_airport(self, openflights_id):
        try:
            return Airport.objects.get(openflights_id=openflights_id)
        except Airport.DoesNotExist:
            raise ValueError(
                f'Airport with openflights_id = {openflights_id} does not exist'
            )

    def _lookup_airline(self, openflights_id):
        try:
            return Airline.objects.get(openflights_id=openflights_id)
        except Airline.DoesNotExist:
            raise ValueError(
                f'Airline with openflights_id = {openflights_id} does not exist'
            )

    def _materialize(self, item):
        origin_airport_id = item['origin_airport']
        destination_airport_id = item['destination_airport']
        airline_id = item['airline']

        origin_airport = self._lookup_airport(openflights_id=origin_airport_id)
        destination_airport = self._lookup_airport(
            openflights_id=destination_airport_id
        )

        airline = self._lookup_airline(openflights_id=airline_id)

        item['origin_airport'] = origin_airport
        item['destination_airport'] = destination_airport
        item['airline'] = airline

        return item


def main():
    importers = [AirlineImporter(), AirportImporter(), RouteImporter()]

    for importer in importers:
        importer.load()
        importer.save()


def run():
    main()
