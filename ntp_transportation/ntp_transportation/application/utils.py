from enum import Enum

import requests


class RoleEnum(Enum):
    ADMIN = "Admin"
    REGISTERED_USER = "Registered User"
    NONE = "None"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


def calculate_distance(source, destination):
    api_key = 'AIzaSyAIJCoIXnAfnAIM-XYrTnmzr8ya5pPehdQ'

    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    r = requests.get(url + 'origins=' + source +
                     '&destinations=' + destination +
                     '&key=' + api_key)

    x = r.json()
    distance = x['rows'][0]['elements'][0]['distance']['text']
    return float(distance.split(" ")[0].replace(',', ''))
