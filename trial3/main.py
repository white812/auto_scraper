__author__ = 'yingbozhan'

from lxml import etree
from test_data import *
from StringIO import StringIO
from util import *
from guess_by_tag import *
from constants import *
from guess_major_component import select_component_paths, generate_best_component_paths
from guess_segment import generate_segment_code
def main():
    data = one_way_attribute_data

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

    price_component_paths = select_component_paths(guesses, price_information, paths_to_value, paths_to_any),
    segment_component_paths = select_component_paths(guesses, segment_information, paths_to_value, paths_to_any),
    quote_component_paths = select_component_paths(guesses, price_information.union(segment_information), paths_to_value, paths_to_any)

    print('price_component_paths: '+price_component_paths)
    print('segment_component_paths: '+segment_component_paths)
    print('quote_component_paths: '+quote_component_paths)


    if not (price_information and segment_component_paths and quote_component_paths):
        #todo need to handle if major component path is not available
        return

    #following guess will be based on best component path
    has_best, price_paths_inclusion, segment_paths_inclusion, quote_paths_inclusion = \
        generate_best_component_paths(price_component_paths, segment_component_paths, quote_component_paths)

    print('price_paths_inclusion: '+price_paths_inclusion)
    print('segment_paths_inclusion: '+segment_paths_inclusion)
    print('quote_paths_inclusion: '+quote_paths_inclusion)


    if not has_best:
        print "NO SUPPORT FOR MULTI GUESS NOW"
        #todo handle multiple component paths guess
        return


    generate_segment_code(guesses_value_path_dict, paths_to_value, segment_paths_inclusion[0], tree, namespace)


main()