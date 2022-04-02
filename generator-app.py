import jinja2 as j2
from utils import *
import re


if __name__ == '__main__':

    mm = get_metamodel()
    library_model = mm.model_from_file('library-example-model.txt')

    PROJECT_GENERAL_INFO = prepare_env(library_model)
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

    def camel_case(m):
        return ''.join([m[:1].lower(), m[1:]])

    def get_package_path(m, suffix=''):
        return PROJECT_GENERAL_INFO['packageRoot'] + '.generated.' + suffix.lower()

    def get_import_path(m, suffix=''):
        if suffix != 'model':
            return PROJECT_GENERAL_INFO['packageRoot'] + '.generated.' + suffix.lower() + '.' + m.name + suffix.capitalize()
        return PROJECT_GENERAL_INFO['packageRoot'] + '.generated.' + suffix.lower() + '.' + m.name

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

    j2_environment.filters['has_collection'] = has_collection
    j2_environment.filters['has_ref'] = has_ref
    j2_environment.filters['get_package_path'] = get_package_path
    j2_environment.filters['get_import_path'] = get_package_path
    j2_environment.filters['camel_case'] = camel_case
    j2_environment.filters['pascal_case_to_hython'] = pascal_case_to_hython

    build_gradle_template = j2_environment.get_template('templates/build.gradle.j2')
    model_template = j2_environment.get_template('templates/model.j2')
    repository_template = j2_environment.get_template('templates/repository.j2')
    controller_template = j2_environment.get_template('templates/controller.j2')
    base_service_template = j2_environment.get_template('templates/base_service.j2')
    base_controller_template = j2_environment.get_template('templates/base_controller.j2')
    base_service_impl_template = j2_environment.get_template('templates/base_service_impl.j2')
    service_template = j2_environment.get_template('templates/service.j2')
    spring_main_template = j2_environment.get_template('templates/main_spring.j2')
    sprint_security_template = j2_environment.get_template('templates/config/security_config.j2')

    for m in library_model.defModel.definitions:
        with open(join(PROJECT_DIRECTORY_TREE['main'], 'Application.java'), 'w') as file:
            file.write(spring_main_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

        with open(join(PROJECT_DIRECTORY_TREE['service'], 'BaseService.java'), 'w') as file:
            file.write(base_service_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

        with open(join(PROJECT_DIRECTORY_TREE['service'], 'BaseServiceImpl.java'), 'w') as file:
            file.write(base_service_impl_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

        with open(join(PROJECT_DIRECTORY_TREE['controller'], 'BaseController.java'), 'w') as file:
            file.write(base_controller_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

        with open(join(PROJECT_DIRECTORY_TREE['config'], 'SecurityConfig.java'), 'w') as file:
            file.write(sprint_security_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

        with open(join(PROJECT_DIRECTORY_TREE['root'], 'build.gradle'), 'w') as file:
            file.write(build_gradle_template.render(projectName='ProjectName'))

        with open(join(PROJECT_DIRECTORY_TREE['model'], "%s.java" % m.name), 'w') as fileModel:
            fileModel.write(model_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

        if m.definitionType == 'define':
            with open(join(PROJECT_DIRECTORY_TREE['repository'], "%sRepository.java" % m.name), 'w') as fileRepository:
                    fileRepository.write(repository_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))
            with open(join(PROJECT_DIRECTORY_TREE['controller'], "%sController.java" % m.name), 'w') as file:
                    file.write(controller_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))
            with open(join(PROJECT_DIRECTORY_TREE['service'], "%sServiceImpl.java" % m.name), 'w') as file:
                file.write(service_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

