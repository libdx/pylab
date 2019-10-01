from ..models import Airline, Airport, Route, Flight


def run():
    models = [Airline, Airport, Route, Flight]

    for model in models:
        all_objects = model.objects.all()
        all_objects.delete()
