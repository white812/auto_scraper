__author__ = 'yingbozhan'

def init_guesses(paths):
    guesses = dict()
    for path in paths:
        guesses[path] = set()
    return guesses

def simple_guess(paths, guesses, simple_guess_dict):
    guesses_value_path_dict = dict()
    for key in simple_guess_dict.keys(): guesses_value_path_dict[key] = set()

    for path in paths:
        temp_path = path.lower()
        for key in simple_guess_dict.keys():
            for possible in simple_guess_dict[key]:
                if possible in temp_path or temp_path in possible:
                    guesses[path].add(key)
                    guesses_value_path_dict[key].add(path)

    return guesses, guesses_value_path_dict

def complex_guess(paths, guesses, simple_guess_dict, guesses_value_path_dict, root, namespace):
    from guess_location import verify_place_code
    from guess_datetime import verify_date_time
    from guess_flight import verify_flight_number
    for path in paths:
        if verify_place_code(path, root, namespace):
            best_match(dict((key, simple_guess_dict[key]) for key in ['arrival','departure']), path, guesses, guesses_value_path_dict)
        elif verify_date_time(path, root, namespace):
            best_match(dict((key, simple_guess_dict[key]) for key in ['date','time']), path, guesses, guesses_value_path_dict)
        elif verify_flight_number(path, root, namespace):
            best_match(dict((key, simple_guess_dict[key]) for key in ['carrier','flight_number']), path, guesses, guesses_value_path_dict)
        best_match(simple_guess_dict, path, guesses, guesses_value_path_dict)
    return guesses, guesses_value_path_dict


def best_match(simple_guess_dict, path, guesses, guesses_value_path_dict):
    from util import longestSubstringFinder
    max_match = 0
    best_guess = None
    for key in simple_guess_dict.keys():
        for possible in simple_guess_dict[key]:
            match_len = len(longestSubstringFinder(path.split('/')[-1], possible))
            if match_len > max_match:
                best_guess = key
                max_match = match_len
    if max_match>0:
        guesses[path].add(best_guess)
        guesses_value_path_dict[best_guess].add(path)

