__author__ = 'yingbozhan'


simple_guess_dict = dict(
    carrier=['carrier', 'operating'],
    date=['date'],
    time=['time'],
    price=['price'],
    currency=['currency'],
    cabin=['cabin'],
    departure=['departure'],
    arrival=['arrival'],
    flight_number=['number'],
)
segment_information = set(['arrival', 'flight_number', 'departure', 'time', 'date'])
price_information = set(['price', 'currency'])

