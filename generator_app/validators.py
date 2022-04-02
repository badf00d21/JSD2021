import re

BUILTIN_TYPES = ['int', 'String', 'Long', 'boolean']
DEFINED_TYPES = []
DRAFT_TYPES = []


def validate_naming(modelName=None, attName=None):
    pascal_case_regex = re.compile(r'([A-Z][a-z0-9]+){1,}')
    camel_case_regex = re.compile(r'[a-z]+((\d)|([A-Z0-9][a-z0-9]+))*([A-Z])?')

    if modelName and not pascal_case_regex.match(modelName):
        print('Definiton of the model must be in PascalCaseSyntax, yours is: ' + modelName)
        quit()

    if attName and not camel_case_regex.match(attName):
        print('Definiton of the attribute must be in camelCaseSyntax, yours is: ' + attName)
        quit()


def gather_defined_types(definitions):
    global DEFINED_TYPES
    global DRAFT_TYPES
    for d in definitions:
        if d.definitionType == 'define':
            DEFINED_TYPES.append(d.name)
        if d.definitionType == 'draft':
            DRAFT_TYPES.append(d.name)


def validate_types(definitions):
    gather_defined_types(definitions)

    for d in definitions:
        validate_naming(modelName=d.name)
        for a in d.attributes:
            if not a.collectionType:
                type_name = a.type.name
                relation_type = a.relationType
            else:
                type_name = a.collectionType.name
                relation_type = a.relationType
            validate_naming(attName=a.name)
            if type_name not in BUILTIN_TYPES and type_name not in DEFINED_TYPES and type_name not in DRAFT_TYPES:
                print('\n\nSemantic validation failed:')
                print('The type: \'' + type_name + '\' used in \'' + d.name + '\' does not exist.\nPlease make correction to your model.')
                quit()
            if relation_type == 'ref' and type_name not in DEFINED_TYPES:
                print('\n\nSemantic validation failed:')
                print('Type: ' + type_name + ' must be marked with \'define\' keyword.\nPlease make correction to your model.')
                quit()


def check_for_defined_properties(appProperties):
    defined_envs = []
    for env in appProperties.envModels:
        defined_envs.append(env.envName)
    if appProperties.selectedEnv not in defined_envs:
        print('\n\nSemantic validation failed, selected env: ' + appProperties.selectedEnv + ' in .application.properties is not defined.\nPlease make correction to your model.')
        quit()



def semantic_model_check(model):
    validate_types(model.defModel.definitions)
    check_for_defined_properties(model.applicationPropertiesModel)
