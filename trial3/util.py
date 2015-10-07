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