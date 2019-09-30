from django.test import TestCase

from .models import Airline, Airport, Route, Flight


class BaseTestCase(TestCase):
    def _create_airline(self, name='Abc Ltd.', country='AU'):
        airline = Airline.objects.create(
            name=name,
            alias='A',
            iata='xyz',
            icao='defg',
            callsign="ABC",
            country=country,
            is_active=True,
            openflights_id=1,
        )
        return airline

    def _create_airport(
        self, name='Abc Airport', country='AU', latitude=-28.001744, longitude=153.42844
    ):
        airport = Airport.objects.create(
            name=name,
            city_name='Abc',
            country=country,
            iata='xyz',
            icao='abcd',
            latitude=latitude,
            longitude=longitude,
            altitude=100,
            timezone_offset=10,
            timezone='Xyz/Abc',
            openflights_id=1,
        )
        return airport

    def _create_route(self, airline_name='Abc Ltd.', origin='A1', destination='A2'):
        origin_airport = self._create_airport(name=origin, latitude=100, longitude=100)
        destination_airport = self._create_airport(
            name=destination, latitude=50, longitude=50
        )
        airline = self._create_airline(name=airline_name)

        route = Route.objects.create(
            airline=airline,
            origin_airport=origin_airport,
            destination_airport=destination_airport,
            stops=2,
            equipment='abcd',
        )

        return route

    def _create_flight(self):
        import datetime

        from django.utils import timezone

        route = self._create_route()
        departure_date = timezone.now()
        arrival_date = departure_date + datetime.timedelta(hours=2)
        flight = Flight.objects.create(
            route=route, departure_date=departure_date, arrival_date=arrival_date
        )
        return flight


class AirlineTests(BaseTestCase):
    def test_create_airline(self):
        airline = self._create_airline()

        self.assertTrue(isinstance(airline, Airline))
        self.assertIn(airline.name, str(airline))
        self.assertIn(airline.callsign, str(airline))


class AirportTests(BaseTestCase):
    def test_create_airport(self):
        airport = self._create_airport()

        self.assertTrue(isinstance(airport, Airport))
        self.assertIn(airport.name, str(airport))
        self.assertIn(airport.country.name, str(airport))
        self.assertIn(airport.city_name, str(airport))


class RouteTests(BaseTestCase):
    def test_create_route(self):
        route = self._create_route()

        self.assertTrue(isinstance(route, Route))
        self.assertIn(str(route.origin_airport), str(route))
        self.assertIn(str(route.destination_airport), str(route))

    def test_back_references(self):
        route = self._create_route(
            airline_name='Abc Ltd.', origin='A1', destination='A2'
        )

        origin_airport = Airport.objects.get(name='A1')
        destination_airport = Airport.objects.get(name='A2')

        self.assertIn(route, origin_airport.outgoing_routes.all())
        self.assertIn(route, destination_airport.incoming_routes.all())

        airline = Airline.objects.get(name='Abc Ltd.')

        self.assertIn(route, airline.routes.all())


class FlightTests(BaseTestCase):
    def test_create_flight(self):
        flight = self._create_flight()

        self.assertTrue(isinstance(flight, Flight))
        self.assertIn(str(flight.route.origin_airport), str(flight))
        self.assertIn(str(flight.route.destination_airport), str(flight))
        self.assertIn(str(flight.departure_date), str(flight))
        self.assertIn(str(flight.arrival_date), str(flight))

    def test_back_references(self):
        flight = self._create_flight()

        route = Route.objects.get(id=1)

        self.assertIn(flight, route.flights.all())
