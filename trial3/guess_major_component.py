__author__ = 'yingbozhan'



def select_component_paths(guesses, component_infomration, paths_to_value, paths_to_any):
    all_possible_component_paths = set()
    total_set = set()
    for guess_set in guesses.values():
        total_set = guess_set.union(total_set)
    if not component_infomration.issubset(total_set):
        print "Could not Identify Enough Information For Further Guesses"
        return None, None, None

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

    best = len(paths)
    if best in path_inclusion_counter and len(path_inclusion_counter[best])==1:
        return list(path_inclusion_counter[best])[0]
    else:
        return list(path_inclusion_counter)


def generate_best_component_paths(price_component_paths, segment_component_paths, quote_component_paths):
    has_best = False
    price_paths_inclusion = guess_best_path(price_component_paths)
    segment_paths_inclusion = guess_best_path(segment_component_paths)
    quote_paths_inclusion = guess_best_path(quote_component_paths)

    if len(price_paths_inclusion)==1 and len(segment_paths_inclusion)==1 and len(quote_paths_inclusion)==1:
        has_best = True
    return has_best, price_paths_inclusion, segment_paths_inclusion, quote_paths_inclusion
