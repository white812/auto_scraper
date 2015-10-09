__author__ = 'yingbozhan'

from guess_location import get_xpath_for_place_code
from guess_datetime import get_xpath_for_datetime, get_inline_xpath_for_datetime
from guess_flight import get_inline_xpath_flight_number
from pprint import pprint


def generate_segment_code(guesses_value_path_dict, paths_to_any, segment_path, root, namespace):
    useful_path = filter_path(paths_to_any, segment_path)

    xpath_from_codes = guesses_value_path_dict['departure']
    xpath_to_codes = guesses_value_path_dict['arrival']

    xpath_from_code = get_xpath_for_place_code(xpath_from_codes, useful_path, root, segment_path, namespace)
    xpath_to_code = get_xpath_for_place_code(xpath_to_codes, useful_path, root, segment_path, namespace)

    print 'xpath_from_code: '
    pprint(xpath_from_code)
    print 'xpath_to_code: '
    pprint(xpath_to_code)

    #todo time format guess
    xpath_for_datetimes = guesses_value_path_dict['date'].union(guesses_value_path_dict['time'])
    xpath_dates, xpath_times = get_xpath_for_datetime(xpath_for_datetimes, useful_path, root, segment_path, namespace)
    xpath_from_time, xpath_to_time = get_inline_xpath_for_datetime(list(xpath_from_code)[0], list(xpath_to_code)[0], xpath_dates, xpath_times, segment_path)

    print 'xpath_from_time: '
    pprint(xpath_from_time)
    print 'xpath_to_time: '
    pprint(xpath_to_time)

    carrier_flight_paths = get_inline_xpath_flight_number(guesses_value_path_dict['flight_number'], useful_path, segment_path, root, namespace)

    print 'carrier_flight_paths: '
    pprint(carrier_flight_paths)


def filter_path(paths_to_any, segment_path):
    selected_path = set()
    for path in paths_to_any:
        if segment_path in path: selected_path.add(path)
    return selected_path