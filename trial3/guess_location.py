__author__ = 'yingbozhan'

def verify_place_code(xpath, root, namespace):
    for value in root.xpath(xpath+'/text()', namespaces=namespace):
        if len(value)!=3 or any(char.isdigit() for char in value):
            return False
    return True

def get_xpath_for_place_code(xpath_codes, useful_path, root, segment_path, namespace):
    valid_xpaths_to_place = set()
    for path in xpath_codes:
        if verify_place_code(path, root, namespace):
            valid_xpaths_to_place.add(path.replace(segment_path,'.'))
    if len(valid_xpaths_to_place)>0: return valid_xpaths_to_place
    else:
        for path in useful_path:
            if verify_place_code(path, root, namespace):
               valid_xpaths_to_place.add(path.replace(segment_path,'.'))
        return valid_xpaths_to_place