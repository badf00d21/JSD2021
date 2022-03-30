# author: badf00d21

from os.path import dirname, join
from textx.export import metamodel_export, model_export
from textx import metamodel_from_file
import os

CURRENT_DIR = dirname(__file__)
PROJECT_DIR = join(CURRENT_DIR, 'project') # TODO: from project get group, artifact and create paths
MODELS_DIR = join(PROJECT_DIR, 'models')
CONTROLLERS_DIR = join(PROJECT_DIR, 'controllers')
REPOSITORIES_DIR = join(PROJECT_DIR, 'repositories')
SERVICES_DIR = join(PROJECT_DIR, 'services')
SERVICES_IMPL_DIR = join(SERVICES_DIR, 'impl')
SERVICES_INTERFACES_DIR = join(SERVICES_DIR, 'interfaces')

def create_paths():
    if not os.path.exists(PROJECT_DIR):
        os.mkdir(PROJECT_DIR)
    if not os.path.exists(MODELS_DIR):
        os.mkdir(MODELS_DIR)
    if not os.path.exists(CONTROLLERS_DIR):
        os.mkdir(CONTROLLERS_DIR)
    if not os.path.exists(REPOSITORIES_DIR):
        os.mkdir(REPOSITORIES_DIR)
    if not os.path.exists(SERVICES_DIR):
        os.mkdir(SERVICES_DIR)
    if not os.path.exists(SERVICES_IMPL_DIR):
        os.mkdir(SERVICES_IMPL_DIR)
    if not os.path.exists(SERVICES_INTERFACES_DIR):
        os.mkdir(SERVICES_INTERFACES_DIR)


def prepare_env():
    create_paths()


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


if __name__ == '__main__':

    mm = get_metamodel()
    dot_folder = join(CURRENT_DIR, 'dotexport')
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)
    metamodel_export(mm, join(dot_folder, 'meta-model.dot'))

    model = mm.model_from_file('library-example-model.txt')
    model_export(model, join(dot_folder, 'model.dot'))

