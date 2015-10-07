__author__ = 'yingbozhan'


class Node():
    parent = None
    key = None
    value = None
    children = None
    guess = []

    def __init__(self, level, **kwargs):
        self.level = level
        self.guess = []
        if 'key' in kwargs.keys():
            self.update_key(kwargs['key'])
        if 'value' in kwargs.keys():
            self.update_value(kwargs['value'])
        if 'parent' in kwargs.keys():
            self.update_parent(kwargs['parent'])
        if 'child' in kwargs.keys():
            self.add_children(kwargs['child'])

    def update_parent(self, parent):
        self.parent = parent

    def update_key(self, key):
        self.key = key

    def update_value(self, value):
        self.value = value

    def add_child(self, child):
        if self.children is None:
            self.children = []
        self.children.append(child)

    def add_children(self, children):
        if self.children is None:
            self.children = []
        self.children += children

    def add_guess(self, guess):
        self.guess.append(guess)

    def node_print(self, indent):
        print('level: ' + str(self.level))
        if self.key is not None: print('key: ' + str(self.key))
        if self.value is not None: print('value: ' + str(self.value))
        if self.children is not None and len(self.children) >= 1:
            print(" " * indent + "{")
            for child in self.children:
                child.node_print(indent + 4)
            print(" " * indent + "}")
