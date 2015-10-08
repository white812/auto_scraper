__author__ = 'yingbozhan'

from util import inline_xpath_decoration

def get_inline_xpath_flight_number(flight_number_paths, useful_path, segment_path, root, namespace):
    flight_number_verified_paths = set()
    for path in flight_number_paths:
        if verify_flight_number(path, root, namespace):
            flight_number_verified_paths.add(path)

    if len(flight_number_verified_paths) == 0:
        for path in useful_path:
            if verify_flight_number(path, root, namespace):
                flight_number_verified_paths.add(path)

    possible_xpath = []
    for flight_number_path in flight_number_verified_paths:
        if is_include_carrier(flight_number_path, root, namespace):
            possible_xpath.append(generate_inclusion_carrier_flight_number_xpath(flight_number_path, segment_path))
        else:
            flight_carrier_paths = set()
            for path in flight_number_paths:
                if path in flight_number_verified_paths: continue
                if verify_flight_carrier(path, root, namespace):
                    flight_carrier_paths.add(path)
            if len(flight_carrier_paths) == 0:
                for path in useful_path:
                    if path in flight_number_verified_paths: continue
                    if verify_flight_carrier(path, root, namespace):
                        flight_carrier_paths.add(path)
            for flight_carrier_path in flight_carrier_paths:
                possible_xpath.append((inline_xpath_decoration(flight_carrier_path), inline_xpath_decoration(flight_number_path)))
    return possible_xpath


def generate_inclusion_carrier_flight_number_xpath(flight_number_path, segment_path):
    return inline_xpath_decoration(flight_number_path.replace(segment_path, '.'))+"[0:2]",\
           inline_xpath_decoration(flight_number_path.replace(segment_path, '.'))


def verify_flight_number(xpath, root, namespace):
    values = set()
    for value in root.xpath(xpath+'/text()', namespaces=namespace):
        values.add(''.join(x for x in value if x.isalpha() or x.isdigit()))
    for value in values:
        if len(value) <=1 or len(value)>=7: return False

        #counting numeric/alpha
        alpha = 0
        numeric = 0
        for x in value:
            if x.isalpha(): alpha += 1
            else: numeric += 1

        if alpha >=3: return False
        if numeric >=5: return False

    return True


def verify_flight_carrier(xpath, root, namespace):
    values = set()
    for value in root.xpath(xpath+'/text()', namespaces=namespace):
        values.add(''.join(x for x in value if x.isalpha() or x.isdigit()))

    for value in values:
        if len(value) !=2: return False
    return True


def is_include_carrier(xpath, root, namespace):
    values = set()
    for value in root.xpath(xpath+'/text()', namespaces=namespace):
        values.add(''.join(x for x in value if x.isalpha() or x.isdigit()))
    for value in values:
        if len(value) <=3 or len(value)>=7: return False
        if value.isdigit(): return False

    return True