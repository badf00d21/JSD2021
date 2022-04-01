# author: badf00d21

from os.path import dirname, join
from textx import metamodel_from_file
import os
from datetime import datetime
from distutils.dir_util import copy_tree

CURRENT_DIR = dirname(__file__)
# TODO scpecify by model
GROUP = 'com.badf00d21'
ARTEFACT = 'projectname'

PROJECT_PACKAGE_ROOT = GROUP + '.' + ARTEFACT
PROJECT_GENERAL_INFO = {
    'author': 'JSD SpringBoot generator by Petar Makevic',
    'date': datetime.now().strftime('%d.%m.%y'),
    'packageRoot': PROJECT_PACKAGE_ROOT
}

PROJECT_DIRECTORY_TREE = {}


def init_project_directory_tree():
    PROJECT_DIRECTORY_TREE['root'] = join(CURRENT_DIR, 'GeneratedProject')
    PROJECT_DIRECTORY_TREE['main'] = join(PROJECT_DIRECTORY_TREE['root'], 'src/main/java/' + PROJECT_GENERAL_INFO['packageRoot'])
    PROJECT_DIRECTORY_TREE['resources'] = join(PROJECT_DIRECTORY_TREE['root'], 'src/main/resources/' + PROJECT_GENERAL_INFO['packageRoot'])
    PROJECT_DIRECTORY_TREE['test'] = join(PROJECT_DIRECTORY_TREE['root'], 'src/test/java/com.badf00d21.project')
    PROJECT_DIRECTORY_TREE['generated'] = join(PROJECT_DIRECTORY_TREE['main'], 'generated')
    PROJECT_DIRECTORY_TREE['model'] = join(PROJECT_DIRECTORY_TREE['generated'], 'model')
    PROJECT_DIRECTORY_TREE['service'] = join(PROJECT_DIRECTORY_TREE['generated'], 'service')
    PROJECT_DIRECTORY_TREE['config'] = join(PROJECT_DIRECTORY_TREE['generated'], 'config')
    PROJECT_DIRECTORY_TREE['repository'] = join(PROJECT_DIRECTORY_TREE['generated'], 'repository')
    PROJECT_DIRECTORY_TREE['controller'] = join(PROJECT_DIRECTORY_TREE['generated'], 'controller')


def copy_static_files():
    from_directory = './static_files/gradle_wrapper'
    to_directory = PROJECT_DIRECTORY_TREE['root']
    copy_tree(from_directory, to_directory)


if __name__ == '__main__':
    init_project_directory_tree()
    for key in PROJECT_DIRECTORY_TREE:
        if not os.path.exists(PROJECT_DIRECTORY_TREE[key]):
            os.makedirs(PROJECT_DIRECTORY_TREE[key])
            print('Generated project directory on path: ', PROJECT_DIRECTORY_TREE[key])


def prepare_env():
    init_project_directory_tree()
    copy_static_files()
    for key in PROJECT_DIRECTORY_TREE:
        if not os.path.exists(PROJECT_DIRECTORY_TREE[key]):
            os.makedirs(PROJECT_DIRECTORY_TREE[key])
            print('Generated project directory on path: ', PROJECT_DIRECTORY_TREE[key])


class BaseType(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


def get_metamodel():
    simple_types = {
        'int': BaseType(None, 'int'),
        'String': BaseType(None, 'String'),
        'Long': BaseType(None, 'Long'),
        'boolean': BaseType(None, 'boolean')
    }
    metamodel = metamodel_from_file('grammar.tx',
                                    classes=[BaseType],
                                    builtins=simple_types)

    return metamodel


# if __name__ == '__main__':
#
#     mm = get_metamodel()
#     dot_folder = join(CURRENT_DIR, 'dotexport')
#     if not os.path.exists(dot_folder):
#         os.mkdir(dot_folder)
#     metamodel_export(mm, join(dot_folder, 'meta-model.dot'))
#
#     model = mm.model_from_file('library-example-model.txt')
#     model_export(model, join(dot_folder, 'model.dot'))

