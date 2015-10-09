__author__ = 'yingbozhan'


def get_data(filepath):
    import os
    script_dir = os.path.dirname(__file__)
    f = open(os.path.join(script_dir, filepath), 'r')
    content = f.read()
    f.close()
    return content

ybtr_oneway = get_data('ybtr_oneway.xml')


