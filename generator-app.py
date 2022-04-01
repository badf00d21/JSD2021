import jinja2 as j2
from utils import *
import re




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

    def pascal_case_to_hython(m):
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        return pattern.sub('-', m.name).lower()

    def get_package_path(m, suffix=''):
        return PROJECT_PACKAGE_ROOT + '.generated.' + suffix.lower()

    def get_import_path(m, suffix=''):
        if (suffix != 'model'):
            return PROJECT_PACKAGE_ROOT + '.generated.' + suffix.lower() + '.' + m.name + suffix.capitalize()
        return PROJECT_PACKAGE_ROOT + '.generated.' + suffix.lower() + '.' + m.name

    j2_environment.filters['has_collection'] = has_collection
    j2_environment.filters['has_ref'] = has_ref
    j2_environment.filters['get_package_path'] = get_package_path
    j2_environment.filters['get_import_path'] = get_package_path

    build_gradle_template = j2_environment.get_template('templates/build.gradle.j2')
    model_template = j2_environment.get_template('templates/model.j2')
    repository_template = j2_environment.get_template('templates/repository.j2')
    spring_main_template = j2_environment.get_template('templates/main_spring.j2')
    sprint_security_template = j2_environment.get_template('templates/config/security_config.j2')
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

        with open(join(PROJECT_DIRECTORY_TREE['main'], 'Application.java'), 'w') as file:
            file.write(spring_main_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

        with open(join(PROJECT_DIRECTORY_TREE['config'], 'SecurityConfig.java'), 'w') as file:
            file.write(sprint_security_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

        with open(join(PROJECT_DIRECTORY_TREE['root'], 'build.gradle'), 'w') as file:
            file.write(build_gradle_template.render(projectName='ProjectName'))

        with open(join(PROJECT_DIRECTORY_TREE['model'], "%s.java" % m.name), 'w') as fileModel:
            fileModel.write(model_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

        if m.definitionType == 'define':
            with open(join(PROJECT_DIRECTORY_TREE['repository'], "%sRepository.java" % m.name), 'w') as fileRepository:
                    fileRepository.write(repository_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

