__author__ = 'yingbozhan'

from lxml import etree
from test_data import *
from StringIO import StringIO
from scraper_template import *

# what to guess:
# 1. leg information (including leg_id)
# 2. quote information (child, adult, infant, price, tax)
# 3. mappings

# what may be known beforehand: from_place, to_place, from_date, to_date

# simplest form of guess

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


def get_path(current_path, current_node):
    tag = current_node.tag
    tag = tag[tag.find("}")+1::]
    if current_node.prefix is None:
        return current_path+'/'+tag
    else:
        return current_path+'/'+current_node.prefix+":"+tag


def dfs(current_node, current_path, known_paths):
    for key in current_node.keys():
        if 'nil' in key: continue
        known_paths.add(current_path+'/@'+key)

    if len(current_node) == 0:
        known_paths.add(get_path(current_path,current_node))
    else:
        next_path = get_path(current_path,current_node)
        for next_node in current_node:
            dfs(next_node, next_path, known_paths)


def dfs_meaningful_path(current_node, current_path, known_paths):
    for key in current_node.keys():
        if 'nil' in key: continue
        known_paths.add(current_path+'/@'+key)
    known_paths.add(get_path(current_path,current_node))
    if len(current_node) > 0:
        next_path = get_path(current_path,current_node)
        for next_node in current_node:
            dfs_meaningful_path(next_node, next_path, known_paths)


def init_guesses(paths):
    guesses = dict()
    for path in paths:
        guesses[path] = set()
    return guesses


def simple_guess(paths, guesses, simple_guess_dict):
    guesses_value_path_dict = dict()
    for path in paths:
        temp_path = path.lower()
        for key in simple_guess_dict:
            if key not in guesses_value_path_dict.keys(): guesses_value_path_dict[key] = set()
            for possible in simple_guess_dict[key]:
                if possible in temp_path:
                    guesses[path].add(key)
                    guesses_value_path_dict[key].add(path)

    return guesses, guesses_value_path_dict


def select_paths(guesses, component_infomration, paths, paths_all):
    all_possible_paths = set()
    total_set = set()
    for guess_set in guesses.values():
        total_set = guess_set.union(total_set)
    if not component_infomration.issubset(total_set): return all_possible_paths
    for path in paths_all:
        available_infomration = set()
        for temp_path in paths:
            if path in temp_path:
                available_infomration = guesses[temp_path].union(available_infomration)
        if component_infomration.issubset(available_infomration):
            all_possible_paths.add(path)
    return all_possible_paths


def generate_component_paths(guesses, paths, paths_all):
    return dict(
        price_paths=select_paths(guesses, price_information, paths, paths_all),
        segment_paths=select_paths(guesses, segment_information, paths, paths_all),
        quote_paths=select_paths(guesses, price_information.union(segment_information), paths, paths_all)
    )

def guess_best_path(paths):
    path_inclusion_counter = dict()
    for path in paths:
        counter = 0
        pos = path.find('/@')
        if pos>0: path = path[0:pos]
        for temp_path in paths:
            pos = temp_path.find('/@')
            if pos >0: temp_path = temp_path[0:pos]
            if temp_path in path:
                counter += 1
        if counter not in path_inclusion_counter:
            path_inclusion_counter[counter] = set()
        path_inclusion_counter[counter].add(path)

    best = len(paths)
    if best in path_inclusion_counter and len(path_inclusion_counter[best])==1:
        return list(path_inclusion_counter[best])[0]
    else:
        return path_inclusion_counter


def generate_best_component_paths(component_paths):
    result = {}
    best = True
    for key in component_paths.keys():
        result[key] = guess_best_path(component_paths[key])
        if type(result[key]) == set:
            best = False
    if best:
        return result
    else:
        return None


def filter_path(paths_all, segment_path):
    selected_path = set()
    for path in paths_all:
        if segment_path in path:
            selected_path.add(path)
    return selected_path


def verify_place_code(xpath, root, namespace):
    for value in root.xpath(xpath+'/text()', namespaces=namespace):
        if len(value)!=3 or any(char.isdigit() for char in value):
            return False
    return True

def get_xpath_for_place_code(xpath_codes, useful_path, root, segment_path, namespace):
    for path in xpath_codes:
        if verify_place_code(path, root, namespace):
            return path.replace(segment_path,'.')
    else:
        for path in useful_path:
            if verify_place_code(path, root, namespace):
                return path.replace(segment_path, '.')
    return None



def obtain_namespace(root):
    namespace = dict()
    for element in root.findall(".//*"):
        for key, value in element.nsmap.iteritems():
            namespace[key] = value
    return namespace


def generate_segment_code(guesses_value_path_dict, paths, segment_path, root, namespace):
    useful_path = filter_path(paths, segment_path)

    xpath_from_codes = guesses_value_path_dict['departure']
    xpath_to_codes = guesses_value_path_dict['arrival']

    xpath_from_code = get_xpath_for_place_code(xpath_from_codes, useful_path, root, segment_path, namespace)
    xpath_to_code = get_xpath_for_place_code(xpath_to_codes, useful_path, root, segment_path, namespace)

    if xpath_to_code is None or xpath_from_code is None:
        print '********************ERROR NOTES FOR XPATH TO PLACE NODE IN SEGMENT****************'

    xpath_for_datetimes = guesses_value_path_dict['date'].union(guesses_value_path_dict['time'])
    xpath_dates, xpath_times = get_xpath_for_datetime(xpath_for_datetimes, useful_path, root, segment_path, namespace)

    xpath_from_time, xpath_to_time = get_inline_xpath_for_datetime(xpath_from_code, xpath_to_code, xpath_dates, xpath_times, segment_path)

    xpath_to_carrier, xpath_to_flight_number = get_inline_xpath_flight_number(guesses_value_path_dict['flight_number'], useful_path, segment_path, root, namespace)

    print xpath_to_carrier, xpath_to_flight_number

def get_inline_xpath_flight_number(flight_number_paths, useful_path, segment_path, root, namespace):
    flight_number_path = set()
    for path in flight_number_paths:
        if verify_flight_number(path, root, namespace):
            flight_number_path.add(path)
    if len(flight_number_path) > 1:
        print '****************FIND MORE THAN ONE FLIGHT NUMBER******************************'
        return None, None
    if len(flight_number_path) == 0:
        for path in useful_path:
            if verify_flight_number(path, root, namespace):
                flight_number_path.add(path)
    if len(flight_number_path) != 1:
        print '****************FIND MORE THAN ONE FLIGHT NUMBER USEFUL******************************'
        return None

    if is_include_carrier(list(flight_number_path)[0], root, namespace):
        generate_inclusion_carrier_flight_number_xpath(list(flight_number_path)[0], segment_path)
    else:
        flight_carrier_path = set()
        for path in flight_number_paths:
            if path == flight_number_path: continue
            if verify_flight_carrier(path, root, namespace):
                flight_carrier_path.add(path)
        if len(flight_carrier_path) >1: return None, None
        if len(flight_carrier_path) == 0:
            for path in useful_path:
                if path == flight_number_path: continue
                if verify_flight_carrier(path, root, namespace):
                    flight_carrier_path.add(path)
        if len(flight_carrier_path) !=1: return None, None
        return inline_xpath_decoration(list(flight_carrier_path)[0]), inline_xpath_decoration(list(flight_number_path)[0])


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



def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer


def inline_xpath_decoration(path):
    return "single_segment_information.xpath('" + path + "')"


def get_inline_xpath_for_datetime(xpath_from_code, xpath_to_code, dates, times, segment_path):
    xpath_dates = []
    xpath_times = []
    for date in dates:
        xpath_dates.append(date.replace(segment_path, '.'))


    if times is None:
        if len(longestSubstringFinder(xpath_from_code, xpath_dates[0])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_dates[1]))>0:
            return inline_xpath_decoration(xpath_dates[0]), inline_xpath_decoration(xpath_dates[1])
        if len(longestSubstringFinder(xpath_from_code, xpath_dates[1])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_dates[0]))>0:
            return inline_xpath_decoration(xpath_dates[1]), inline_xpath_decoration(xpath_dates[0])
    else:
        for time in times:
            xpath_times.append(time.replace(segment_path, '.'))
        xpath_times = list(xpath_times)
        date_from_str = ''
        time_from_str = ''
        date_to_str = ''
        time_to_str = ''

        if len(longestSubstringFinder(xpath_from_code, xpath_dates[0])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_dates[1]))>0:
            date_from_str, date_to_str = inline_xpath_decoration(xpath_dates[0]), inline_xpath_decoration(xpath_dates[1])
        if len(longestSubstringFinder(xpath_from_code, xpath_dates[1])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_dates[0]))>0:
            date_from_str, date_to_str = inline_xpath_decoration(xpath_dates[1]), inline_xpath_decoration(xpath_dates[0])

        if len(longestSubstringFinder(xpath_from_code, xpath_times[0])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_times[1]))>0:
            time_from_str, time_to_str = inline_xpath_decoration(xpath_times[0]), inline_xpath_decoration(xpath_times[1])
        if len(longestSubstringFinder(xpath_from_code, xpath_times[1])) > 0 and \
            len(longestSubstringFinder(xpath_to_code, xpath_times[0]))>0:
            time_from_str, time_to_str = inline_xpath_decoration(xpath_times[1]), inline_xpath_decoration(xpath_times[0])

        if time_from_str == '' or time_to_str =='' or date_from_str=='' or date_to_str=='':
            return None, None
        else:
            return date_from_str+'+'+time_from_str, date_to_str+'+'+time_to_str


def guess_date_time(xpath, root, namespace):
    #possible results: date only, time only, date time, None.
    values = set()
    for value in root.xpath(xpath+'/text()', namespaces=namespace):
        values.add(''.join(x for x in value if x.isalpha() or x.isdigit()))

    date_guess = 0
    time_guess = 0
    datetime_guess = 0

    for value in values:
        if len(value) < 4: return 0 #not date/time

        #counting numeric/alpha
        alpha = 0
        numeric = 0
        for x in value:
            if x.isalpha(): alpha += 1
            else: numeric += 1

        if numeric == 0: return 0
        if alpha >=4: return 0

        if alpha<=2:
            if numeric >=8: datetime_guess +=1
            elif numeric>6: date_guess +=1
            else: time_guess+=1
        else:
            if numeric<=6: date_guess+=1
            else: datetime_guess +=1
    if max(date_guess, time_guess, datetime_guess)!=0:
        if time_guess == max(date_guess, time_guess, datetime_guess): return 1
        if date_guess == max(date_guess, time_guess, datetime_guess): return 2
        if datetime_guess == max(date_guess, time_guess, datetime_guess): return 3
    else:
        return 0


def get_xpath_for_datetime(xpath_for_datetimes, useful_path, root, segment_path, namespace):
    date_time_path_guess = [set(), set(), set(), set()]
    for xpath in xpath_for_datetimes:
        guess_value = guess_date_time(xpath, root, namespace)
        date_time_path_guess[guess_value].add(xpath)

    #todo complete time format guess
    #date time combined
    if len(date_time_path_guess[3]) == 2:
        return date_time_path_guess[3], None
    #date time split
    elif len(date_time_path_guess[1]==2) and len(date_time_path_guess[2])==2:
        return date_time_path_guess[2], date_time_path_guess[1]
    else:
        return None



def main():
    data = one_way_attribute_data
    root = etree.XML(data)
    tree = etree.parse(StringIO(data))
    paths = set()
    paths_all = set()
    namespace = obtain_namespace(root)
    dfs(root, '/',paths)
    dfs_meaningful_path(root, '/', paths_all)
    guesses, guesses_value_path_dict = simple_guess(paths, init_guesses(paths), simple_guess_dict)
    component_paths = generate_component_paths(guesses, paths, paths_all)
    best_component_path = generate_best_component_paths(component_paths)
    if best_component_path is None:
        print "NO SUPPORT FOR MULTI GUESS NOW"
        return
    generate_segment_code(guesses_value_path_dict, paths, best_component_path['segment_paths'], tree, namespace)


# suppose to return time format
# def finalize_settings_combined(date_time_guess, root, segment_path, namespace):
#     values_1 = []
#     values_2 = []
#     [xpath_1, xpath_2] = list(date_time_guess)
#     for value in root.xpath(xpath_1+'/text()', namespaces=namespace):
#         values_1.add(''.join(x for x in value if x.isalpha() or x.isdigit()))










main()