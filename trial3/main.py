__author__ = 'yingbozhan'

from lxml import etree
from test_data import *
from StringIO import StringIO
from util import *
from guess_by_tag import *
from constants import *
from guess_major_component import select_component_paths, generate_best_component_paths, get_best_path
from guess_segment import generate_segment_code
from pprint import pprint
from test_file_data.test_website_data import *
def main():
    data = ybtr_oneway

    root = etree.XML(data)
    tree = etree.parse(StringIO(data))

    paths_to_value = set()
    paths_to_any = set()
    namespace = obtain_namespace(root)

    dfs_to_value(root, '/',paths_to_value)
    dfs_to_any(root, '/', paths_to_any)

    # guess is path_value_dict
    guesses = init_guesses(paths_to_value)
    guesses, guesses_value_path_dict = simple_guess(paths_to_value, guesses, simple_guess_dict)

    price_component_paths = select_component_paths(guesses, price_information, paths_to_value, paths_to_any)
    segment_component_paths = select_component_paths(guesses, segment_information, paths_to_value, paths_to_any)
    quote_component_paths = select_component_paths(guesses, price_information.union(segment_information), paths_to_value, paths_to_any)

    pprint('price_component_paths: ')
    pprint(price_component_paths)
    pprint('segment_component_paths: ')
    pprint(segment_component_paths)
    pprint('quote_component_paths: ')
    pprint(quote_component_paths)


    if not (price_component_paths and segment_component_paths and quote_component_paths):
        #re-run simple guess
        guesses, guesses_value_path_dict = complex_guess(paths_to_value, guesses, simple_guess_dict, guesses_value_path_dict, tree, namespace)
        price_component_paths = select_component_paths(guesses, price_information, paths_to_value, paths_to_any)
        segment_component_paths = select_component_paths(guesses, segment_information, paths_to_value, paths_to_any)
        quote_component_paths = select_component_paths(guesses, price_information.union(segment_information), paths_to_value, paths_to_any)

        pprint('price_component_paths: ')
        pprint(price_component_paths)
        pprint('segment_component_paths: ')
        pprint(segment_component_paths)
        pprint('quote_component_paths: ')
        pprint(quote_component_paths)
        # if not (price_component_paths and segment_component_paths and quote_component_paths):
        #     return

    #following guess will be based on best component path
    price_paths_inclusion = None
    segment_paths_inclusion = None
    quote_paths_inclusion = None

    price_paths_inclusion = generate_best_component_paths(price_component_paths)
    segment_paths_inclusion = generate_best_component_paths(segment_component_paths)
    quote_paths_inclusion = generate_best_component_paths(quote_component_paths)

    pprint('price_paths_inclusion: ')
    pprint(price_paths_inclusion)
    pprint('segment_paths_inclusion: ')
    pprint(segment_paths_inclusion)
    pprint('quote_paths_inclusion: ')
    pprint(quote_paths_inclusion)



    best_segment_path = get_best_path(segment_paths_inclusion)

    generate_segment_code(guesses_value_path_dict, paths_to_value, best_segment_path, tree, namespace)


main()