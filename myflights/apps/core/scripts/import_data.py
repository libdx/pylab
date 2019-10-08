import sys
import json 
from django.core.exceptions import ValidationError
from abc import ABC, abstractproperty
from pathlib import Path

from ..models import Airline, Airport, Route


class BaseImporter(ABC):
    """Abstract class that provides interface and base functionality
    to import data from JSON to database.
    """
    Model = None
    batch_size = 100

    def __init__(self):
        """Initializes `BaseImporter` instance.
        """

        self.file = Path('data') / self.filename
        self.new_objects = []

    def _log(self, msg):
        """Naive log to strerr using built-in print.

        :param msg: message to be logged
        :type msg: str
        """

        print(f'[{self.Model}] {msg}', file=sys.stderr)

    @abstractproperty
    def filename(self):
        """Abstract property. Provide JSON filename in data directory to be imported.
        """
        pass

    def _materialize(self, item):
        """Override to substitute identifiers in `item` with model objects
        to satisfy relationship requirements if any.
        """
        return item

    def load(self):
        """Deserializes data from corresponding JSON file and creates model objects.
        This also calls `_materialize` where model object's relationships could be satisfied.
        """

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
        """Saves all created models using `bulk_create`.
        """

        self._log(f'Saving in batches=[{self.batch_size}]')

        self.Model.objects.bulk_create(self.new_objects, self.batch_size)


class AirlineImporter(BaseImporter):
    Model = Airline

    @property
    def filename(self):
        """Provides filename for JSON file containing Airlines data.
        """
        return 'airlines.json'


class AirportImporter(BaseImporter):
    Model = Airport

    @property
    def filename(self):
        """Provides filename for JSON file containing Airports data.
        """
        return 'airports.json'


class RouteImporter(BaseImporter):
    Model = Route

    @property
    def filename(self):
        """Provides filename for JSON file containing Routes data.
        """
        return 'routes.json'

    def _lookup_airport(self, openflights_id):
        """Queries Airport object by given openflights_id.
        Raises ValueError if object not found.

        :param openflights_id: id from OpenFlights dataset.
        :type openflights_id: int
        """
        try:
            return Airport.objects.get(openflights_id=openflights_id)
        except Airport.DoesNotExist:
            raise ValueError(
                f'Airport with openflights_id = {openflights_id} does not exist'
            )

    def _lookup_airline(self, openflights_id):
        """Queries Airline object by given openflights_id.
        Raises ValueError if object not found.

        :param openflights_id: id from OpenFlights dataset.
        :type openflights_id: int
        """
        try:
            return Airline.objects.get(openflights_id=openflights_id)
        except Airline.DoesNotExist:
            raise ValueError(
                f'Airline with openflights_id = {openflights_id} does not exist'
            )

    def _materialize(self, item):
        """Substitutes airports and airline IDs with actual objects
        to satisfy relationships in Route.
        """
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
