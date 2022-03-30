import jinja2 as j2
from utils import *
from datetime import datetime



# TODO scpecify by model
GROUP = 'com.badf00d21'
ARTEFACT = 'projectname'

PROJECT_PACKAGE_ROOT = GROUP + '.' + ARTEFACT
PROJECT_GENERAL_INFO = {
    'author': 'JSD SpringBoot generator by Petar Makevic',
    'date': datetime.now().strftime('%d.%m.%y'),
    'packageRoot': PROJECT_PACKAGE_ROOT
}

if __name__ == '__main__':
    mm = get_metamodel()
    library_model = mm.model_from_file('library-example-model.txt')

    j2_environment = j2.Environment(
        loader=j2.FileSystemLoader(CURRENT_DIR),
        trim_blocks=True,
        lstrip_blocks=True)

    def has_collection(m):
        return len(list(filter(lambda a: a.collectionType, m.attributes))) > 0

    def has_ref(m):
        return len(list(filter(lambda a: a.relationType == 'ref', m.attributes))) > 0

    def get_package_path(m, suffix=''):
        if (suffix != 'model') :
            return PROJECT_PACKAGE_ROOT + '.' + suffix.lower() + '.' + m.name + suffix.capitalize()
        return PROJECT_PACKAGE_ROOT + '.' + suffix.lower() + '.' + m.name

    j2_environment.filters['has_collection'] = has_collection
    j2_environment.filters['has_ref'] = has_ref
    j2_environment.filters['get_package_path'] = get_package_path

    model_template = j2_environment.get_template('templates/model.j2')
    repository_template = j2_environment.get_template('templates/repository.j2')

    def javatype(s):  # refactor
        """
        Maps type names from PrimitiveType to Java.
        """
        return {
            'int': 'int',
            'String': 'String',
            'Long': 'Long',
            'boolean': 'boolean'
        }.get(s.name, s.name)

    prepare_env()

    for m in library_model.defModel.definitions:
        with open(join(MODELS_DIR, "%sModel.java" % m.name), 'w') as fileModel:
            fileModel.write(model_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

        if m.definitionType == 'define':
            with open(join(REPOSITORIES_DIR, "%sRepository.java" % m.name), 'w') as fileRepository:
                    fileRepository.write(repository_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

