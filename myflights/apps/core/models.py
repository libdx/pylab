from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField


class Airport(models.Model):
    """Represents real Airport.
    """

    name = models.CharField(_('Airport name'), max_length=255, null=True)
    city_name = models.CharField(_('City name'), max_length=255, null=True, blank=True)
    country = CountryField(_('Country'))
    iata = models.CharField(
        _('3-letter IATA code'), max_length=3, null=True, blank=True
    )
    icao = models.CharField(
        _('4-letter ICAO code'), max_length=4, null=True, blank=True
    )
    latitude = models.FloatField(_('Latitude'))
    longitude = models.FloatField(_('Longitude'))
    altitude = models.FloatField(_('Altitude (meters)'), null=True, blank=True)
    timezone_offset = models.FloatField(
        _('Offset from UTC in hours'), null=True, blank=True
    )
    timezone = models.CharField(
        _('Time zone name in tz (Olsom) format', max_length=100), null=True, blank=True
    )
    openflights_id = models.IntegerField(
        _('ID from OpenFlights database'), null=True, blank=True
    )

    def __str__(self):
        return f'{self.name} {self.country.name}/{self.city_name}'


class Airline(models.Model):
    """Represents operational and defunct Airline company.
    """

    name = models.CharField(_('Airline name'), max_length=255, null=True)
    alias = models.CharField(
        _('Short Airline alias', max_length=100), null=True, blank=True
    )
    iata = models.CharField(
        _('3-letter IATA code'), max_length=3, null=True, blank=True
    )
    icao = models.CharField(
        _('4-letter ICAO code'), max_length=4, null=True, blank=True
    )
    callsign = models.CharField(
        _('Airline callsign'), max_length=50, null=True, blak=True
    )
    country = CountryField(_('Country or territory where Airline is incorporated'))
    is_active = models.BooleanField(
        _('Is Airline operational or defunct'), default=True
    )
    openflights_id = models.IntegerField(
        _('ID from OpenFlights database'), null=True, blank=True
    )

    def __str__(self):
        return f'{self.name} {self.callsign}'


class Route(models.Model):
    """Represents routes between airports
    """

    airline = models.ForeignKey(
        Airline, related_name='routes', on_delete=models.SET_NULL, null=True, blank=True
    )
    origin_airport = models.ForeignKey(
        Airport, related_name='outgoing_routes', on_delete=models.CASCADE
    )
    destination_airport = models.ForeignKey(
        Airport, related_name='incoming_routes', on_delete=models.CASCADE
    )
    stops = models.IntegerField(_('Number of stops on route'), null=True, blank=True)
    equipment = models.CharField(_('3-letter codes for plane type'), max_length=100)


class Flight(models.Model):
    """Represents single flight along it's route
    """

    route = models.ForeignKey(Route, related_name='flights', on_delete=models.CASCADE)
    departure_date = models.DateTimeField(_('Departure date time in UTC'))
    arrival_date = models.DateTimeField(_('Arrival date time in UTC'))