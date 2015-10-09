__author__ = 'yingbozhan'


def select_component_paths(guesses, component_infomration, paths_to_value, paths_to_any):
    all_possible_component_paths = set()
    total_set = set()
    for guess_set in guesses.values():
        total_set = guess_set.union(total_set)
    if not component_infomration.issubset(total_set):
        print "Could not Identify Enough Information For Further Guesses"
        return None

    for path in paths_to_any:
        available_infomration = set()
        for temp_path in paths_to_value:
            if path in temp_path:
                available_infomration = guesses[temp_path].union(available_infomration)
        if component_infomration.issubset(available_infomration):
            all_possible_component_paths.add(path)
    return all_possible_component_paths


def guess_best_path(paths):
    path_inclusion_counter = dict()
    for i in range(0, len(paths)+1):
        path_inclusion_counter[i] = set()

    for path in paths:
        counter = 0
        pos = path.find('/@')
        if pos>0: path = path[0:pos]
        for temp_path in paths:
            pos = temp_path.find('/@')
            if pos >0: temp_path = temp_path[0:pos]
            if temp_path in path: counter += 1
        path_inclusion_counter[counter].add(path)

    return path_inclusion_counter


# def check_unique_best_path(paths, counter):
#     best = len(paths)
#     if best in counter and len(counter[best])==1:
#         return True
#     return False


def get_best_path(component_inclusions):
    keys = sorted(component_inclusions.keys(), reverse=True)
    for key in keys:
        if len(component_inclusions[key])==0: continue
        return list(component_inclusions[key])[0]





def generate_best_component_paths(component_paths):
    if component_paths is None: return None
    paths_inclusion = guess_best_path(component_paths)
    return paths_inclusion
