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
                if possible in temp_path:
                    guesses[path].add(key)
                    guesses_value_path_dict[key].add(path)

    return guesses, guesses_value_path_dict