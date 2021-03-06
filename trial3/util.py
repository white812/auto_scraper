__author__ = 'yingbozhan'


def obtain_namespace(root):
    namespace = dict()
    for element in root.findall(".//*"):
        for key, value in element.nsmap.iteritems():
            namespace[key] = value
    return namespace

def get_path(current_path, current_node):
    tag = current_node.tag
    tag = tag[tag.find("}")+1::]
    if current_node.prefix is None:
        return current_path+'/'+tag
    else:
        return current_path+'/'+current_node.prefix+":"+tag


def dfs_to_value(current_node, current_path, known_paths):
    for key in current_node.keys():
        if 'nil' in key: continue
        known_paths.add(current_path+'/@'+key)

    if len(current_node) == 0:
        known_paths.add(get_path(current_path,current_node))
    else:
        next_path = get_path(current_path,current_node)
        for next_node in current_node:
            dfs_to_value(next_node, next_path, known_paths)


def dfs_to_any(current_node, current_path, known_paths):
    for key in current_node.keys():
        if 'nil' in key: continue
        known_paths.add(current_path+'/@'+key)
    known_paths.add(get_path(current_path,current_node))
    if len(current_node) > 0:
        next_path = get_path(current_path,current_node)
        for next_node in current_node:
            dfs_to_any(next_node, next_path, known_paths)



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