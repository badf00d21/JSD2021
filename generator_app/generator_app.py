import jinja2 as j2
from generator_app.utils import *
import re
import argparse
import generator_app.validators as validators
from pathlib import Path


def main():
    grammar_file = join(dirname(__file__), 'model_meta_model', 'grammar.tx')
    model_file = join(dirname(__file__), 'model_meta_model', 'library-example-model.txt')

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input-model-path", required=False,
                    help="Input model of grammar, if not provided 'library-example-model.txt' from repository will be used")
    ap.add_argument("-o", "--output-generated-path", required=False,
                    help="Output path for generated SpringBoot project & 'dotexport' directory")
    ap.add_argument("-s", "--show-grammar", required=False, default=False, action='store_true',
                    help="Prints textX grammar to stdout.")
    args = vars(ap.parse_args())

    if args['show_grammar']:
        with open(join(grammar_file), 'r') as f:
            print('\nGrammar of: ' + grammar_file + '\n\n--------------')
            print(f.read())
            print('\n\n--------------')

    output_path = ''
    if args['output_generated_path']:
        output_path = join(args['output_generated_path'])
    else:
        print('Please provide: -o --output-generated-path to generate project.')
        quit()
    if args['input_model_path']:
        print('Passed model file on path: ' + args['input_model_path'])
        model_file = join(args['input_model_path'])

    meta_model = get_metamodel(grammar_file)
    print('Loading model_from_file: ' + model_file)
    model = meta_model.model_from_file(model_file)
    validators.semantic_model_check(model)

    PROJECT_GENERAL_INFO = prepare_env(model, output_path)
    export_to_dot(meta_model, model, output_path)

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
            return PROJECT_GENERAL_INFO[
                       'packageRoot'] + '.generated.' + suffix.lower() + '.' + m.name + suffix.capitalize()
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
    app_properties_template = j2_environment.get_template('templates/application.properties.j2')
    app_properties_env_template = j2_environment.get_template('templates/application-env.properties.j2')
    model_template = j2_environment.get_template('templates/model.j2')
    repository_template = j2_environment.get_template('templates/repository.j2')
    controller_template = j2_environment.get_template('templates/controller.j2')
    base_service_template = j2_environment.get_template('templates/base_service.j2')
    base_controller_template = j2_environment.get_template('templates/base_controller.j2')
    base_service_impl_template = j2_environment.get_template('templates/base_service_impl.j2')
    service_template = j2_environment.get_template('templates/service.j2')
    spring_main_template = j2_environment.get_template('templates/main_spring.j2')
    sprint_security_template = j2_environment.get_template('templates/config/security_config.j2')

    with open(join(PROJECT_DIRECTORY_TREE['main'], 'Application.java'), 'w') as file:
        file.write(spring_main_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO, properties=None))

    with open(join(PROJECT_DIRECTORY_TREE['resources'], 'application.properties'), 'w') as file:
        file.write(app_properties_template.render(properties=model.applicationPropertiesModel,
                                                  projectGeneralInfo=PROJECT_GENERAL_INFO))

    for propEnv in model.applicationPropertiesModel.envModels:
        with open(join(PROJECT_DIRECTORY_TREE['resources'], 'application-' + propEnv.envName + '.properties'),
                  'w') as file:
            file.write(app_properties_env_template.render(env=propEnv,
                                                          projectGeneralInfo=PROJECT_GENERAL_INFO))

    with open(join(PROJECT_DIRECTORY_TREE['main'], 'Application.java'), 'w') as file:
        file.write(spring_main_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

    with open(join(PROJECT_DIRECTORY_TREE['service_gen'], 'BaseService.java'), 'w') as file:
        file.write(base_service_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

    with open(join(PROJECT_DIRECTORY_TREE['service_gen'], 'BaseServiceImpl.java'), 'w') as file:
        file.write(base_service_impl_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

    with open(join(PROJECT_DIRECTORY_TREE['controller_gen'], 'BaseController.java'), 'w') as file:
        file.write(base_controller_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

    with open(join(PROJECT_DIRECTORY_TREE['config'], 'SecurityConfig.java'), 'w') as file:
        file.write(sprint_security_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

    with open(join(PROJECT_DIRECTORY_TREE['root'], 'build.gradle'), 'w') as file:
        file.write(build_gradle_template.render(projectGeneralInfo=PROJECT_GENERAL_INFO))

    for m in model.defModel.definitions:
        with open(join(PROJECT_DIRECTORY_TREE['model'], "%s.java" % m.name), 'w') as fileModel:
            fileModel.write(model_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

        if m.definitionType == 'define':

            rep_path = join(PROJECT_DIRECTORY_TREE['repository'], "%sRepository.java" % m.name)
            if not Path(rep_path).is_file():
                with open(rep_path, 'w') as fileRepository:
                    fileRepository.write(repository_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

            contr_path = join(PROJECT_DIRECTORY_TREE['controller'], "%sController.java" % m.name)
            if not Path(contr_path).is_file():
                with open(contr_path, 'w') as file:
                    file.write(controller_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))

            service_path = join(PROJECT_DIRECTORY_TREE['service'], "%sServiceImpl.java" % m.name)
            if not Path(service_path).is_file():
                with open(service_path, 'w') as file:
                    file.write(service_template.render(model=m, projectGeneralInfo=PROJECT_GENERAL_INFO))
    print('\n\033[1m\033[92mWell done, your project and dotexport are geenrated on provided output path!\033[0m')


if __name__ == '__main__':
    main()
