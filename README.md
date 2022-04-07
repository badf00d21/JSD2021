# JSD2021
Predmetni projekat iz ispita JSD

## Spring Boot Rest API generation

- DSL example for generating Spring Boot API
- Generate models, controllers, services, repositories 
- Output code is Gradle project, you can specify `build.gradle`
- You can also specify different environments(Spring profiles) and common properties for `application.yml`
- Supported databse is MongoDB


###### Technology
python 3.6+ with jinja template engine and textX


###### Requirements
 - Python 3.6+
 - JRE 1.8+
 - Connection to **mongod** instance - remote or local


###### About Grammar

Grammar is defined in textX.
- Model definition starts with keyword **define** if model is going to be mapped into db collection, or **draft** if not, followed by the model name (which will be the same in Java class) and ' (' **attributes** ' )' *see the example below
- Each model must contain at least one **attribute**.
- Attributes posses type which can be builtin(boolean, int, Long, String): ```genre of String ``` or defined type: ```dimensions of BookDimension```.
- Attributes of defined types can reference to another object (collection) in DB using keyword ```ref``` which will produce **@DBRef annotation in Java class** (similar to the case of foreign keys in the relational model), model that will be referenced must be marked with **define** keyword: ```createdBy ref Librarian```
- Attributes of defined types that don't reference to another collection: ```dimensions of BookDimension```, they must reference model marked with ```draft``` keyword and will be serialized as nested JSON objects in DB.
- Types can also be collections: ```allItems ref [InventoryItem]``` (mapped to Java List).
- Gradle: TODO
- .properties: TODO


###### About Generator

Code generation is going to be implemented **Jinja** template language.
As a final result, the generator will produce a **SpringBoot** project, ready for usage with the generated **mongodb** scheme.
The usual application layers characteristic of this technology will be generated: **model, repository, service, controller**.
It will functionally support standard **CRUD** operations on all models marked with ```defined``` keyword.
Since the frontend does not exist, a **swagger** library will be included for presentation purposes.
Also, in order to save the amount of code and better readability, the lombok library will be used by default, model (constructors, getters, setters, to string).
The Java Model classes will be **public** by default and the attributes by convention will be **private**.
The **Gradle Wrapper** will also be included by default, to reduce installation requirements.


###### Example

```
application (
    contextPath is /api-v1
    selectedEnv is dev
    environment dev (
        dbUri is mongodb://127.0.0.1:27017
        db is LibraryDB_dev
    )
    environment test (
        dbUri is mongodb://147.27.5.11:1090
        db is LibraryDB_test
    )
    environment prod (
        dbUri is mongodb://211.67.8.0:8899
        db is LibraryDB_prod
    )
)

gradle (
    groupId is com.badf00d21
    artifactId is spring-boot-generated-app
    projectName is SpringBootMongoGenerated
)

define Library (
    name of String
    state of String
    city of String
    postalCode of String
    type of String
    isPublic of boolean
    isSchool of boolean
    isUniversity of boolean
)

define Librarian (
    firstName of String
    lastName of String
    age of int
    idNumber of String
    worksIn ref Library
    roles of [String]
)

define Record (
    type of String
    title of String
    authors of String
    genre of String
    publisher of [String]
    pubYear of int
    pubPlace of String
    dimensions of BookDimension
    createdBy ref Librarian
    lastModifiedBy ref Librarian
    allItems ref [InventoryItem]
)

draft BookDimension (
    height of Long
    width of Long
)

define InventoryItem (
    inventoryNumber of String
    signatures of String
    record ref Record
    isBorrowed of boolean
)
```


