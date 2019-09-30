from django.contrib import admin

from .models import Airline, Airport, Route, Flight

admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Flight)
