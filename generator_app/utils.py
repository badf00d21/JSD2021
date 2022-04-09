# author: badf00d21
import os
from os.path import dirname, join
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from datetime import datetime
from distutils.dir_util import copy_tree

CURRENT_DIR = dirname(__file__)
PROJECT_DIRECTORY_TREE = {}
PROJECT_GENERAL_INFO = {}

def init_general_info(projectModel):
    global PROJECT_GENERAL_INFO
    groupId = projectModel.gradleBuildModel.groupId
    artifact = projectModel.gradleBuildModel.artifactId
    name = projectModel.gradleBuildModel.projectName
    version = '1.0.0'
    if projectModel.gradleBuildModel.appVersion != '':
        version = projectModel.gradleBuildModel.appVersion

    project_package_root = groupId + '.' + name.lower()
    PROJECT_GENERAL_INFO = {
        'author': 'JSD SpringBoot generator by Petar Makevic',
        'date': datetime.now().strftime('%d.%m.%y'),
        'packageRoot': project_package_root,
        'groupId': groupId,
        'artifactId': artifact,
        'name': name,
        'version': version
    }


def init_project_directory_tree(output_path):
    global PROJECT_DIRECTORY_TREE
    PROJECT_DIRECTORY_TREE['root'] = join(output_path, PROJECT_GENERAL_INFO['name'])
    PROJECT_DIRECTORY_TREE['main'] = join(PROJECT_DIRECTORY_TREE['root'], 'src/main/java/' + PROJECT_GENERAL_INFO['packageRoot'].replace('.', '/'))
    PROJECT_DIRECTORY_TREE['resources'] = join(PROJECT_DIRECTORY_TREE['root'], 'src/main/resources/')
    PROJECT_DIRECTORY_TREE['test'] = join(PROJECT_DIRECTORY_TREE['root'], 'src/test/java/' + PROJECT_GENERAL_INFO['packageRoot'].replace('.', '/'))
    PROJECT_DIRECTORY_TREE['generated'] = join(PROJECT_DIRECTORY_TREE['main'], 'generated')
    PROJECT_DIRECTORY_TREE['model'] = join(PROJECT_DIRECTORY_TREE['generated'], 'model')
    PROJECT_DIRECTORY_TREE['service_gen'] = join(PROJECT_DIRECTORY_TREE['generated'], 'service')
    PROJECT_DIRECTORY_TREE['service'] = join(PROJECT_DIRECTORY_TREE['main'], 'service')
    PROJECT_DIRECTORY_TREE['config'] = join(PROJECT_DIRECTORY_TREE['main'], 'config')
    PROJECT_DIRECTORY_TREE['repository'] = join(PROJECT_DIRECTORY_TREE['main'], 'repository')
    PROJECT_DIRECTORY_TREE['controller_gen'] = join(PROJECT_DIRECTORY_TREE['generated'], 'controller')
    PROJECT_DIRECTORY_TREE['controller'] = join(PROJECT_DIRECTORY_TREE['main'], 'controller')


def copy_static_files():
    from_directory = join(CURRENT_DIR, './static_files/gradle_wrapper')
    to_directory = PROJECT_DIRECTORY_TREE['root']
    copy_tree(from_directory, to_directory)


def prepare_env(projectModel, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print('Created directories on path: ' + output_path + ' for generating project & dotexport.')
    init_general_info(projectModel)
    init_project_directory_tree(output_path)
    copy_static_files()
    for key in PROJECT_DIRECTORY_TREE:
        if not os.path.exists(PROJECT_DIRECTORY_TREE[key]):
            os.makedirs(PROJECT_DIRECTORY_TREE[key])
            print('Generated project directory on path: ', PROJECT_DIRECTORY_TREE[key])
    return PROJECT_GENERAL_INFO


class BaseType(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


def get_metamodel(path_to_grammar):
    simple_types = {
        'int': BaseType(None, 'int'),
        'String': BaseType(None, 'String'),
        'Long': BaseType(None, 'Long'),
        'boolean': BaseType(None, 'boolean')
    }
    print('Loading metamodel_from_file: ' + path_to_grammar)
    metamodel = metamodel_from_file(path_to_grammar,
                                    classes=[BaseType],
                                    builtins=simple_types)
    return metamodel


def export_to_dot(mm, mff, path):
    dot_folder = join(path, 'dotexport')
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)
    metamodel_export(mm, join(dot_folder, 'meta-model.dot'))
    model_export(mff, join(dot_folder, 'model.dot'))
    print('.dot files generated in:' + dot_folder)

