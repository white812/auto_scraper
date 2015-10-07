__author__ = 'yingbozhan'


from node import Node

def parse_json(json_data, next_level, nodes, parent_node):
    if type(json_data) == dict:
        new_nodes = []
        for key, value in json_data.iteritems():
            node = Node(next_level, key=key, parent=parent_node)
            if next_level == 1: parent_node.add_children(node)
            nodes.append(node)
            new_nodes.append(nodes)
            if type(value) == dict or type(value) == list:
                node.add_children(parse_json(value, next_level+1, nodes, node))
            else:
                node.update_value(value)
        return new_nodes
    elif type(json_data) == list:
        new_nodes = []
        for value in json_data:
            node = Node(next_level, parent=parent_node)
            if next_level == 1: parent_node.add_children(node)
            nodes.append(node)
            new_nodes.append(nodes)
            if type(value) == dict or type(value) == list:
                node.add_children(parse_json(value, next_level+1, nodes, node))
            else:
                node.update_value(value)
        return new_nodes
    else:
        node = Node(next_level, parent=parent_node, value=json_data)
        if next_level == 1: parent_node.add_child(node)
        nodes.append(node)
        return node
